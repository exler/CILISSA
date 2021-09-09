from typing import Tuple

import numpy as np


def crop_array(array: np.ndarray, crop_width: int) -> np.ndarray:
    """
    Crop input `array` by `crop_width` in every dimension
    """
    array = np.array(array, copy=False)

    crops = [[crop_width, crop_width]] * array.ndim
    slices = tuple(slice(a, array.shape[i] - b) for i, (a, b) in enumerate(crops))
    cropped = array[slices]

    return cropped


def sliding_window(array: np.ndarray, window_size: Tuple[int, int]) -> np.ndarray:
    for y in range(0, array.shape[0]):
        for x in range(0, array.shape[1]):
            yield (array[y : y + window_size[1], x : x + window_size[0]])
