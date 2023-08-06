import os
import warnings

import cv2
import numpy as np
import patchify
import torch
import torchvision


def image_to_patches(image: np.array, step_size: int) -> np.array:
    """Creates 64x64 subimages from original image with given stride (step_size)"""

    # Calculate padding size
    padded_shape = image.shape[0] + step_size - image.shape[0] % step_size, image.shape[1] + step_size - image.shape[1] % step_size
    # Add reflective padding
    padded_image = np.pad(image, step_size, mode='reflect')[step_size:step_size + padded_shape[0], step_size:step_size + padded_shape[1]]

    return patchify.patchify(padded_image, (64, 64), step=step_size)


def patches_to_tensor(patches: np.array):
    """Turn array of patches into tensor ready to be used by a PyTorch model"""

    # Flatten second dimension
    flat_patches = patches.reshape(patches.shape[0] * patches.shape[1], 64, 64)
    # Convert range 0-255 to 0-1
    flat_patches = flat_patches.astype(np.float32) / 255
    # Add channel dimension
    return torch.tensor(flat_patches, dtype=torch.float).unsqueeze(0).swapaxes(0, 1)


def tensor_to_patches(tensor: torch.tensor, patches_shape: tuple):
    """Turn tensor of patches into 2D array of patches of given shape"""

    # Remove channel dimension from tensor, convert to array
    flat_patches = tensor.swapaxes(0, 1).squeeze(0).detach().cpu().numpy()
    # Reshape into desired shape
    patches = flat_patches.reshape(patches_shape[0], patches_shape[1], 64, 64)
    # Convert from 0-1 to 0-255
    return (patches.clip(0, 1) * 255).astype(np.uint8)


def patches_to_image(patches: np.array, image_shape: tuple, step_size: int):
    """Reconstruct image from 2D array of patches"""

    # Patches might include padding due to stride and original image size mismatch, calculate the padded image shape
    padded_shape = image_shape[0] + step_size - image_shape[0] % step_size, image_shape[1] + step_size - image_shape[1] % step_size
    padded_image = patchify.unpatchify(patches, padded_shape)
    # Remove padding
    return padded_image[:image_shape[0], :image_shape[1]]


def scale_image(image: np.ndarray, factor: float, mode: int = -666) -> np.ndarray:
    """Return image scaled by factor"""

    # Compute resized shape
    scaled_shape = (int(image.shape[1] * factor), int(image.shape[0] * factor))

    if mode == -666:
        if factor < 1:
            mode = cv2.INTER_AREA
        else:
            mode = cv2.INTER_LINEAR

    return cv2.resize(image, scaled_shape, interpolation=mode)


class SRCNN(torch.nn.Module):
    def __init__(self, weights: str = '', use_cuda: bool = True):
        super(SRCNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 64, kernel_size=9, stride=(1, 1), padding=(2, 2), padding_mode='reflect')
        self.conv2 = torch.nn.Conv2d(64, 32, kernel_size=1, stride=(1, 1), padding=(2, 2), padding_mode='reflect')
        self.conv3 = torch.nn.Conv2d(32, 1, kernel_size=5, stride=(1, 1), padding=(2, 2), padding_mode='reflect')

        if weights:
            if os.path.isfile(weights):
                self.load_state_dict(torch.load(weights))
            else:
                warnings.warn('File with pretrained weights does not exist, initialized empty model.')
        else:
            warnings.warn('No weights loaded, initialized empty model. You can find pretrained weights for download at https://github.com/bohundan/treadscan-SRCNN/tree/master/pretrained_models')

        self.device = 'cuda' if torch.cuda.is_available() and use_cuda else 'cpu'
        self.to(self.device)

        if use_cuda and self.device == 'cpu':
            warnings.warn('Using CPU, CUDA is not available.')

    def forward(self, x):
        x = torch.nn.functional.relu(self.conv1(x))
        x = torch.nn.functional.relu(self.conv2(x))
        x = self.conv3(x)
        return x

    def upsample(self, image: np.array, factor: int = 4, batch_size: int = 100) -> np.array:
        """Upscale image by factor, specify smaller batch_size so conserve memory"""

        if len(image.shape) != 2:
            warnings.warn('You are attempting to upsample a color image. This model is suited for upsampling only grayscale images. To convert your image from for example BGR to grayscale, use cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY).')
            return image

        with torch.no_grad():
            # Prepare image
            upscaled_image = scale_image(image, factor)
            patches = image_to_patches(upscaled_image, 64)
            tensors = patches_to_tensor(patches).split(batch_size)

            # Upscale it (in batches)
            outputs = []
            for batch in tensors:
                output = self(batch.to(self.device))
                outputs.append(output.detach().cpu())

            # Reconstruct it
            outputs = torch.cat(outputs)
            output_patches = tensor_to_patches(outputs, (patches.shape[0], patches.shape[1]))
            output_image = patches_to_image(output_patches, upscaled_image.shape, 64)

            return output_image
