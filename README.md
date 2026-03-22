# imio

A simple and robust image I/O and hashing utility library.

## Features
- Minimal dependencies (`numpy` and `Pillow` only).
- Consistently reads any image format (including RGBA, Grayscale, etc.) as an `RGB` numpy array.
- Generates a deterministic, unique 8-character ID based on pixel values. The generated ID is guaranteed to start with an alphabetic character.
- **Robust typed API**: Native support for both `str` and `pathlib.Path` objects.
- **Clear Error Handling**: Throws clear and descriptive exceptions when images are missing (`FileNotFoundError`) or corrupted (`UnidentifiedImageError`).
- **Flexible output options**: Easily pass underlying Pillow `**kwargs` (such as `quality`, `optimize`) directly when saving an image.

## Installation

You can install the package directly from the source code:

```bash
pip install .
```

## Usage

```python
from pathlib import Path

import imio

# 1. Read an image from either a string or a Path object
# Always returns an RGB numpy array
img = imio.imread("path/to/image.png")
print(img.shape)  # e.g., (H, W, 3)

# 2. Generate a unique image ID 
uid = imio.get_id(img)
print(uid)  # e.g., 'g8f2d5a3' (8-character hash starting with a letter)

# 3. Write an image with extended saving options
img_mod = img // 2  # Darken the image (numpy array broadcasting)
output_path = Path("path/to/output.jpg")
imio.imwrite(output_path, img_mod, quality=95, optimize=True)
```
