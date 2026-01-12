import numpy as np
from typing import Any

def cal_background(image: np.ndarray | None, mask: np.ndarray, method= "mean") ->(np.floating[Any] | None) :
    if image is None:
        raise ValueError("image is None")
    if method == "mean":
        return np.mean(image[mask])

    elif method == "median":
        return np.median(image[mask])

    else:
        raise RuntimeError("cal_background() requires method= 'mean' or 'median'")

def cal_background_noise(image: np.ndarray | None, mask: np.ndarray) -> np.floating[Any]:
    if image is None:
        raise ValueError("image is None")
    return np.std(image[mask])

def subtract_background(
    data: np.ndarray | None,
    background: np.floating[Any] | None,
) -> np.ndarray:
    if data is None or background is None:
        raise ValueError("Invalid input")

    return data - background
