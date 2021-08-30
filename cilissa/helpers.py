from typing import Union

import numpy as np


def clamp(
    value: Union[int, float, np.number],
    smallest: Union[int, float, np.number],
    largest: Union[int, float, np.number],
) -> Union[int, float, np.number]:
    return np.maximum(smallest, np.minimum(value, largest))


def crop_array(array: np.ndarray, crop_width: int) -> np.ndarray:
    """
    Crop input `array` by `crop_width` in every dimension
    """
    array = np.array(array, copy=False)

    crops = [[crop_width, crop_width]] * array.ndim
    slices = tuple(slice(a, array.shape[i] - b) for i, (a, b) in enumerate(crops))
    cropped = array[slices]

    return cropped
