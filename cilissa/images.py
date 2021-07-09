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

    def __init__(self, image_path: str) -> None:
        self.path = image_path
        self.name = os.path.basename(self.path)
        self.im = cv2.imread(image_path)

        if self.im is None:
            raise IOError(f"Cannot open image path: `{self.path}`")

    @property
    def channels_num(self) -> Optional[int]:
        # 2D array is a grayscale image, 3D array gives the number of channels
        return None if self.ndim == 2 else self.shape[-1]

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

    orig: Image
    comp: Image

    def __init__(self, orig_image: Image, comp_image: Image) -> None:
        self.orig = orig_image
        self.comp = comp_image

    def __getitem__(self, key: int) -> Image:
        if key == 0:
            return self.orig
        elif key == 1:
            return self.comp
        else:
            raise IndexError

    def __setitem__(self, key: int, value: Image) -> None:
        if key == 0:
            self.orig = value
        elif key == 1:
            self.comp = value
        else:
            raise IndexError

    @property
    def matching_shape(self) -> bool:
        return self.orig.im.shape == self.comp.im.shape

    @property
    def matching_dtype(self) -> bool:
        return self.orig.im.dtype == self.comp.im.dtype

    def as_floats(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns a tuple with both images as :data:`np.ndarray` of floats
        """
        return (self.orig.as_float(), self.comp.as_float())


class ImageCollection:
    """
    A collection of one or more :class:`cillisa.images.ImagePair`.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass
