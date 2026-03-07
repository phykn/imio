# imio

A simple and robust image I/O and hashing utility library.

## Features
- Minimal dependencies (`numpy` and `Pillow` only).
- Consistently reads any image format (including RGBA, Grayscale, etc.) as an `RGB` numpy array.
- Generates a deterministic, unique 8-character ID based on pixel values. The generated ID is guaranteed to start with an alphabetic character.

## Installation

You can install the package directly from the source code:

```bash
pip install .
```

For development (editable mode):
```bash
pip install -e .
```

## Usage

```python
import numpy as np
import imio

# 1. Read an image (always returns an RGB numpy array)
img = imio.imread("path/to/image.png")
print(img.shape)  # e.g., (H, W, 3)

# 2. Generate a unique image ID 
uid = imio.get_id(img)
print(uid)  # e.g., 'g8f2d5a3' (8-character hash starting with a letter)

# 3. Write an image
img_mod = img // 2  # Darken the image
imio.imwrite("path/to/output.jpg", img_mod)
```
