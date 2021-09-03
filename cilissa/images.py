from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Tuple, Type, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np

from cilissa.classes import OrderedList
from cilissa.exceptions import NotOnImageError
from cilissa.roi import ROI


class Image:
    """
    `np.ndarray` wrapper, a core structure in CILISSA
    """

    path: str = ""
    name: str = ""
    im: np.ndarray

    def __init__(self, image: Union[Path, str, np.ndarray], name: Optional[str] = None) -> None:
        if name:
            self.name = name

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

    def crop(self, sl: Tuple[slice, slice]) -> Image:
        im = self.im[sl] if sl else self.im
        return Image(np.ascontiguousarray(im), name=self.name)

    @property
    def width(self) -> int:
        return self.im.shape[1]

    @property
    def height(self) -> int:
        return self.im.shape[0]

    @property
    def channels_num(self) -> int:
        # 2D array is a grayscale image, 3D array gives the number of channels
        return 1 if self.im.ndim == 2 else self.im.shape[-1]

    def get_resized(self, width: Optional[int] = None, height: Optional[int] = None) -> Image:
        if width and height:
            maxsize = (width, height)
        elif width:
            maxsize = (width, int((self.width / width) * self.height))
        elif height:
            maxsize = (int((self.height / height) * self.width), height)
        else:
            return self
        return Image(cv2.resize(self.im, maxsize, interpolation=cv2.INTER_AREA), name=self.name)

    def from_array(self, image_array: np.ndarray, at: Optional[Tuple[slice, slice]] = None) -> None:
        """
        Replaces the underlying image array with given `np.ndarray`
        """
        self.path = self.path or ""
        self.name = self.name or "Image loaded from array"

        if at:
            self.im[at] = image_array
        else:
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
        return Image(self.im, name=self.name)

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

    def check_if_on_image(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        if x and (x < 0 or x > self.width):
            return False

        if y and (y < 0 or y > self.height):
            return False

        return True

    def _as(self, data_type: Type) -> np.ndarray:
        np_type = np.result_type(self.im, data_type)
        image = np.asarray(self.im, dtype=np_type)
        return image

    def as_int(self) -> np.ndarray:
        """Converts the image to :data:`np.ndarray` of ints"""
        return self._as(np.uint8)

    def as_float(self) -> np.ndarray:
        """Converts the image to :data:`np.ndarray` of floats"""
        return self._as(np.float32)

    def __str__(self) -> str:
        return f"Image(name={self.name})"


class ImagePair:
    """
    A pair of 2 :class:`cilissa.images.Image`. Analysis is performed using this class.

    If any of the attributes in the image pair are mismatched, the attribute of the reference image
    will be used if necessary.

    Attributes:
        im1 (:class:`cilissa.images.Image`): Reference image against which quality is measured
        im2 (:class:`cilissa.images.Image`): Image whose quality is to be measured
    """

    im1: Image
    im2: Image

    roi: Union[ROI, None] = None

    def __init__(self, reference_image: Image, compared_image: Image) -> None:
        self.im1 = reference_image
        self.im2 = compared_image

    def __getitem__(self, key: int) -> Image:
        if key == 0:
            im = self.im1
        elif key == 1:
            im = self.im2
        else:
            raise IndexError

        slices = self._get_roi_slices()
        if slices:
            return im.crop(slices)

        return im

    def __setitem__(self, key: int, image: Image) -> None:
        if key == 0:
            self.im1.from_array(image.im, at=self._get_roi_slices())
        elif key == 1:
            self.im2.from_array(image.im, at=self._get_roi_slices())
        else:
            raise IndexError

    def get_full_image(self, key: int) -> np.ndarray:
        im = getattr(self, f"im{key + 1}", None)
        if im:
            return im
        raise IndexError

    def set_roi(self, roi: ROI) -> None:
        if not self.im1.check_if_on_image(roi.x0, roi.y0) or not self.im1.check_if_on_image(roi.x1, roi.y1):
            raise NotOnImageError
        self.roi = roi

    def _get_roi_slices(self) -> Optional[Tuple[slice, slice]]:
        return self.roi.slices if self.roi else None

    @property
    def matching_shape(self) -> bool:
        return self.im1.im.shape == self.im2.im.shape

    @property
    def matching_dtype(self) -> bool:
        return self.im1.im.dtype == self.im2.im.dtype

    def as_floats(self) -> Tuple[np.ndarray, np.ndarray]:
        """Returns a tuple with both images as :data:`np.ndarray` of floats"""
        return (self[0].as_float(), self[1].as_float())


class ImageCollection(OrderedList):
    """
    A collection of one or more :class:`cillisa.images.ImagePair`.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass
