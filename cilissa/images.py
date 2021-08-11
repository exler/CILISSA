from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Tuple, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np

from cilissa.classes import OrderedList


class Image:
    """
    `np.ndarray` wrapper, a core structure in CILISSA
    """

    path: str
    name: str

    def __init__(self, image: Optional[Union[Path, str, np.ndarray]]) -> None:
        if isinstance(image, Path) or isinstance(image, str):
            self.load(image)
        elif isinstance(image, np.ndarray):
            self.from_array(image)
        else:
            raise TypeError("Cannot create an Image from given object")

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Image):
            comparison = self.im == o.im
        elif isinstance(o, np.ndarray):
            comparison = self.im == o
        else:
            raise TypeError(f"Cannot compare object of type Image and {type(o)}")

        return comparison.all()

    @property
    def channels_num(self) -> int:
        # 2D array is a grayscale image, 3D array gives the number of channels
        return 1 if self.im.ndim == 2 else self.im.shape[-1]

    def get_thumbnail(self, width: int, height: int) -> np.ndarray:
        maxsize = (width, height)
        return cv2.resize(self.im, maxsize, interpolation=cv2.INTER_AREA)

    def from_array(self, image_array: np.ndarray) -> None:
        """
        Replaces the underlying image array with given `np.ndarray`
        """
        self.path = ""
        self.name = "Image loaded from array"
        self.im = image_array

    def load(self, image_path: Union[Path, str]) -> None:
        """
        Loads the image from given path

        Uses cv2.imdecode instead of cv2.imread to handle unicode characters in path
        Args:
            - image_path (Path/str): Path where the image is located.
        """
        self.path = str(image_path)
        self.name = os.path.basename(self.path)

        self.im = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), cv2.IMREAD_ANYCOLOR)
        if self.im is None:
            raise IOError(f"Cannot open image path: `{self.path}`")

    def save(self, save_path: Union[Path, str] = "") -> None:
        """
        Saves the image

        Args:
            - save_path (Path/str/None):
            Path to save the image at. Must contain the filename with extension.
            If empty string, then will save to the path the image was loaded from (if available)
        """
        if save_path:
            self.path = str(save_path)

        if self.path:
            cv2.imwrite(self.path, self.im)
        else:
            logging.error("No save path supplied!")

    def copy(self) -> Image:
        """
        Copies and returns the image
        """
        image = Image(self.im)
        image.name = self.name
        return image

    def display_image(self) -> None:
        """
        Displays loaded image until user presses ESCAPE or closes window manually
        """
        if self.im is not None:
            cv2.imshow(self.name, self.im)
            while cv2.getWindowProperty(self.name, 0) >= 0:
                k = cv2.waitKey(0)
                if k == 27:  # ESCAPE key
                    cv2.destroyWindow(self.name)
                    break

    def display_histogram(self) -> None:
        """
        Displays grayscale histogram of the loaded image
        """
        plt.figure()
        title = self.name
        xlim = 0

        if self.channels_num == 1:
            title += " - grayscale histogram"
            xlim = 1

            histogram, bin_edges = np.histogram(self.im, bins=256, range=(0, 1))
            plt.plot(bin_edges[0:-1], histogram)
        elif self.channels_num == 3:
            title += " - RGB histogram"
            xlim = 256

            colors = ("red", "green", "blue")
            for channel_id, color in enumerate(colors):
                histogram, bin_edges = np.histogram(self.im[:, :, channel_id], bins=256, range=(0, 256))
                plt.plot(bin_edges[0:-1], histogram, color=color)
        else:
            logging.warn(f"Cannot display histogram of image with {self.channels_num} channels!")
            return

        plt.title(title)
        plt.xlim([0, xlim])
        plt.xlabel("Color value")
        plt.ylabel("Pixel count")
        plt.show()

    def as_int(self) -> np.ndarray:
        """
        Converts the image to :data:`np.ndarray` of ints
        """
        int_type = np.result_type(self.im, np.uint8)
        image = np.asarray(self.im, dtype=int_type)
        return image

    def as_float(self) -> np.ndarray:
        """
        Converts the image to :data:`np.ndarray` of floats
        """
        float_type = np.result_type(self.im, np.float32)
        image = np.asarray(self.im, dtype=float_type)
        return image

    def __str__(self) -> str:
        return f"Image(name={self.name})"


class ImagePair:
    """
    A pair of 2 :class:`cilissa.images.Image`. Analysis is performed using this class.

    If any of the attributes in the image pair are mismatched, the attribute of the reference image
    will be used if necessary.

    Attributes:
        ref (:class:`cilissa.images.Image`): Reference image against which quality is measured
        A (:class:`cilissa.images.Image`): Image whose quality is to be measured
    """

    ref: Image
    A: Image

    def __init__(self, ref_image: Image, A_image: Image) -> None:
        self.ref = ref_image
        self.A = A_image

    def __getitem__(self, key: int) -> Image:
        if key == 0:
            return self.ref
        elif key == 1:
            return self.A
        else:
            raise IndexError

    def __setitem__(self, key: int, value: Image) -> None:
        if key == 0:
            self.ref = value
        elif key == 1:
            self.A = value
        else:
            raise IndexError

    @property
    def matching_shape(self) -> bool:
        return self.ref.im.shape == self.A.im.shape

    @property
    def matching_dtype(self) -> bool:
        return self.ref.im.dtype == self.A.im.dtype

    def as_floats(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns a tuple with both images as :data:`np.ndarray` of floats
        """
        return (self.ref.as_float(), self.A.as_float())


class ImageCollection(OrderedList):
    """
    A collection of one or more :class:`cillisa.images.ImagePair`.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass
