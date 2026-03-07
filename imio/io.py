import hashlib
import numpy as np

from PIL import Image


def imread(
    path: str,
) -> np.ndarray:
    """Read an image from the given path.

    Args:
        path: Path to the image file.

    Returns:
        Image as a numpy array in RGB format.
    """
    img = Image.open(path).convert("RGB")
    return np.array(img)


def imwrite(
    path: str,
    img: np.ndarray,
) -> None:
    """Save an image to the given path.

    Args:
        path: Destination path for the image file.
        img: Image to save as a numpy array.
    """
    Image.fromarray(img).save(path)


def get_id(
    img: np.ndarray,
) -> str:
    """Generate a unique ID for an image.

    Args:
        img: Image as a numpy array.

    Returns:
        Generated unique ID string.
    """
    raw = np.ascontiguousarray(img).tobytes()
    digest = hashlib.md5(raw).hexdigest()[:8]
    if digest[0].isdigit():
        digest = chr(ord("g") + int(digest[0])) + digest[1:]
    return digest
