import hashlib
import numpy as np
from PIL import Image


def imread(path: str) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    return np.array(img)


def imwrite(path: str, img: np.ndarray) -> None:
    Image.fromarray(img).save(path)


def image_id(img: np.ndarray) -> str:
    raw = np.ascontiguousarray(img).tobytes()
    digest = hashlib.md5(raw).hexdigest()[:8]
    if digest[0].isdigit():
        digest = chr(ord("g") + int(digest[0])) + digest[1:]
    return digest
