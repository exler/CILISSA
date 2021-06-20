import os

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
        self._image = cv2.imread(image_path)

        if self._image is None:
            raise IOError(f"Cannot open image path: `{self.path}`")

    def display(self) -> None:
        """
        Displays loaded image until user presses ESCAPE or closes window manually
        """
        if self._image is not None:
            cv2.imshow(self.name, self._image)
            while cv2.getWindowProperty(self.name, 0) >= 0:
                k = cv2.waitKey(0)
                if k == 27:  # ESCAPE key
                    cv2.destroyWindow(self.name)

    def as_float(self) -> np.ndarray:
        """
        Converts the image to :data:`np.ndarray` of floats
        """
        float_type = np.result_type(self._image, np.float32)
        image = np.asarray(self._image, dtype=float_type)
        return image


class ImagePair:
    """
    A pair of 2 :class:`cilissa.images.Image`. Analysis is performed using this class.
    """

    first: Image
    second: Image

    def __init__(self, base_image: Image, test_image: Image) -> None:
        self.first = base_image
        self.second = test_image

    def __getitem__(self, key: int) -> Image:
        if key == 0:
            return self.first
        elif key == 1:
            return self.second
        else:
            raise IndexError

    def __setitem__(self, key: int, value: Image) -> None:
        if key == 0:
            self.first = value
        elif key == 1:
            self.second = value
        else:
            raise IndexError

    def as_floats(self) -> np.ndarray:
        """
        Returns a tuple with both images as :data:`np.ndarray` of floats
        """
        return (self.first.as_float(), self.second.as_float())


class ImageCollection:
    """
    A collection of one or more :class:`cillisa.images.ImagePair`.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass
