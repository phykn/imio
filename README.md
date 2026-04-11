# imrw
Minimal image I/O library for Python.

## Features
- Read/Write images via `Pillow` & `numpy`.
- Clean and simple interface.
- `imread` returns a `uint8` numpy array preserving the source mode: `H x W` for grayscale, `H x W x 3` for RGB, `H x W x 4` for RGBA. Other PIL modes fall back to RGB.
- `imwrite` expects a `uint8` array with shape `H x W`, `H x W x 1`, `H x W x 3`, or `H x W x 4`.

## Quick Start
```bash
pip install imrw
```

```python
from imrw import imread, imwrite

image = imread("input.png")
imwrite("output.png", image)
```
