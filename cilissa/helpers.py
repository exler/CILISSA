import numpy as np


def crop_array(array: np.ndarray, crop_width: int) -> np.ndarray:
    """
    Crop input `array` by `crop_width` from both sides
    """
    array = np.array(array, copy=False)

    crops = [[crop_width, crop_width] * array.ndim]
    slices = tuple(slice(a, array.shape[i] - b) for i, (a, b) in enumerate(crops))
    cropped = array[slices]

    return cropped
