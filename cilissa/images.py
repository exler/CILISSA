import logging
import os
from pathlib import Path
from queue import Queue
from typing import Tuple, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np


class Image:
    """
    Image wrapper to work with CILISSA
    """

    path: str
    name: str

    def __init__(self, image_path: Union[Path, str]) -> None:
        self.load(image_path)

    @property
    def channels_num(self) -> int:
        # 2D array is a grayscale image, 3D array gives the number of channels
        return 1 if self.im.ndim == 2 else self.im.shape[-1]

    def load(self, image_path: Union[Path, str]) -> None:
        """
        Loads the image from given path

        Args:
            - image_path (Path/str): Path where the image is located.
        """
        self.path = str(image_path)
        self.name = os.path.basename(self.path)

        self.im = cv2.imread(self.path)
        if self.im is None:
            raise IOError(f"Cannot open image path: `{self.path}`")

    def save(self, save_path: Union[Path, str]) -> None:
        """
        Saves the image

        Args:
            - save_path (Path/str): Path to save the image at.
            Must contain the filename with extension.
        """
        cv2.imwrite(save_path, self.im)

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

    def show_histogram(self) -> None:
        """
        Shows grayscale histogram of the loaded image
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


class ImageCollection(Queue):
    """
    A collection of one or more :class:`cillisa.images.ImagePair`, implemented as a FIFO queue.

    Operations performed on :class:`cillisa.images.ImagePair` can be applied to the whole collection.
    """

    pass
