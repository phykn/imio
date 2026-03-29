# imio

Minimal image I/O + deterministic image ID.

## Install
```bash
pip install .
```

## API
- `imread(path) -> np.ndarray` (RGB)
- `imwrite(path, img, **kwargs) -> None`
- `get_id(img) -> str` (8 chars, deterministic)

## Example
```python
import imio

img = imio.imread("input.png")
uid = imio.get_id(img)
imio.imwrite("output.jpg", img, quality=95)
```
