import os
from typing import Optional, Tuple

import cv2
import numpy as np


class Image:
    """
    Image wrapper to work with CILISSA
    """

    path: str
    name: str
    dtype: np.dtype
    ndim: int
    shape: tuple

    def __init__(self, image_path: str) -> None:
        self.path = image_path
        self.name = os.path.basename(self.path)
        self.im = cv2.imread(image_path)

        self.dtype = self.im.dtype
        self.ndim = self.im.ndim
        self.shape = self.im.shape

        if self.im is None:
            raise IOError(f"Cannot open image path: `{self.path}`")

    def display(self) -> None:
        """
        Displays loaded image until user presses ESCAPE or closes window manually
        """
        if self.im is not None:
            cv2.imshow(self.name, self.im)
            while cv2.getWindowProperty(self.name, 0) >= 0:
                k = cv2.waitKey(0)
                if k == 27:  # ESCAPE key
                    cv2.destroyWindow(self.name)

    @property
    def max(self) -> int:
        return np.max(self.im)

    @property
    def min(self) -> int:
        return np.min(self.im)

    @property
    def channels_num(self) -> Optional[int]:
        # 2D array is a grayscale image, 3D array gives the number of channels
        return None if self.ndim == 2 else self.shape[-1]

    def as_float(self) -> np.ndarray:
        """
        Converts the image to :data:`np.ndarray` of floats
        """
        float_type = np.result_type(self.im, np.float32)
        image = np.asarray(self.im, dtype=float_type)
        return image


class ImagePair:
    """
    A pair of 2 :class:`cilissa.images.Image`. Analysis is performed using this class.
    """

    base: Image
    test: Image

    def __init__(self, base_image: Image, test_image: Image) -> None:
        self.base = base_image
        self.test = test_image

    def __getitem__(self, key: int) -> Image:
        if key == 0:
            return self.base
        elif key == 1:
            return self.test
        else:
            raise IndexError

    def __setitem__(self, key: int, value: Image) -> None:
        if key == 0:
            self.base = value
        elif key == 1:
            self.test = value
        else:
            raise IndexError

    @property
    def matching_shape(self) -> bool:
        return self.base.shape == self.test.shape

    @property
    def matching_dtype(self) -> bool:
        return self.base.dtype == self.test.dtype

    def as_floats(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns a tuple with both images as :data:`np.ndarray` of floats
        """
        return (self.base.as_float(), self.test.as_float())


class ImageCollection:
    """
    A collection of one or more :class:`cillisa.images.ImagePair`.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass