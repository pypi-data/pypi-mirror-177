import numpy as np

def normalize_image(array: np.ndarray) -> np.ndarray:
    array = array.astype(np.uint16)

    normalized = (array.astype(np.uint16) - array.min()) * 255.0 / (array.max() - array.min())
    return normalized

