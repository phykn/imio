import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError


def imread(path: str | Path) -> np.ndarray:
    try:
        return np.array(Image.open(path).convert("RGB"))
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found at path: {path}")
    except UnidentifiedImageError:
        raise ValueError(f"Cannot identify image file: {path}")


def imwrite(
    path: str | Path,
    img: np.ndarray,
    **kwargs,
) -> None:
    try:
        Image.fromarray(img).save(path, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Error saving image to {path}: {e}")


def get_id(img: np.ndarray) -> str:
    raw = np.ascontiguousarray(img).tobytes()

    digest = hashlib.md5(raw).hexdigest()[:8]

    if digest[0].isdigit():
        digest = chr(ord("g") + int(digest[0])) + digest[1:]

    return digest
