# TreadSRCNN

[![PyPI version](https://badge.fury.io/py/treadSRCNN.svg)](https://badge.fury.io/py/treadSRCNN)
[![Downloads](https://pepy.tech/badge/treadsrcnn)](https://pepy.tech/project/treadsrcnn)

This package provides [SRCNN](https://arxiv.org/abs/1501.00092) model implemented in PyTorch. This model is only intended for use on __grayscale images__, and was created as an extension to [treadscan](https://github.com/bohundan/treadscan).

[Treadscan](https://github.com/bohundan/treadscan) is a Python package containing computer vision tools for extracting tire treads. Sometimes, the scanned treads are in lower quality, because a vehicle hasn't stopped in the correct position, or the camera was out of focus. Applying upsampling to these images might help mitigate these issues.

Example of occurence of lower resolution tire treads (vehicles stopped far away, in the other lane):
![Treadscan tire segmentation](https://github.com/bohundan/treadscan-SRCNN/raw/main/paper_src/media/treadscan.gif)

Quick summary of this project is contained in [this paper](https://github.com/bohundan/treadscan-SRCNN/blob/main/paper.pdf) in the root of the repository. It was made as semestral work for Computational Intelligence Methods course at FIT CTU.

## Example usage

```python
import cv2
from treadSRCNN import SRCNN

low_resolution_image = cv2.imread('low_resolution_image.png', cv2.IMREAD_GRAYSCALE)

# Pretrained models can be found in https://github.com/bohundan/treadscan-SRCNN/tree/main/pretrained_models
srcnn = SRCNN('pretrained_weights.pth')

# Factor determines the upscaling factor
# The higher the batch_size, the more memory is consumed during upsampling 
# (my 6GiB VRAM GPU can do around 500 batch_size comfortably)
upsampled_image = srcnn.upsample(low_resolution_image, factor=4, batch_size=100)
```

## Upsampling preview

There is some tradeoff between sharper image and added noise.
<div align="center">
  <p>
    <img src="https://raw.githubusercontent.com/bohundan/treadscan-SRCNN/main/paper_src/media/upscaled-original.jpg" title="Original" height=500/>
    <img src="https://raw.githubusercontent.com/bohundan/treadscan-SRCNN/main/paper_src/media/upscaled-250epochs.jpg" title="Upsampled" height=500/>
  </p>
</div>
