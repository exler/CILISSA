from typing import Callable

import numpy as np


def get_max_pixel_value(dtype: np.dtype) -> int:
    if dtype == np.uint8:
        return 255
    elif dtype == np.uint16:
        return 65535
    elif dtype == np.uint32:
        return 2147483647
    elif np.issubdtype(dtype, np.floating):
        return 1
    else:
        raise ValueError(f"Cannot get max pixel value for dtype {dtype}")


def apply_to_channels(im1: np.ndarray, im2: np.ndarray, func: Callable, channels_num: int) -> float:
    results = np.empty(channels_num)
    for channel in range(channels_num):
        channel_result = func(im1[:, :, channel], im2[:, :, channel])
        results[channel] = channel_result

    return np.mean(np.nan_to_num(results))


def crop_array(array: np.ndarray, crop_width: int) -> np.ndarray:
    """
    Crop input `array` by `crop_width` in every dimension
    """
    array = np.array(array, copy=False)

    crops = [[crop_width, crop_width]] * array.ndim
    slices = tuple(slice(a, array.shape[i] - b) for i, (a, b) in enumerate(crops))
    cropped = array[slices]

    return cropped
