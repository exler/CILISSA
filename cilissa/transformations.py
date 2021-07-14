import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, Union

import cv2
import numpy as np

from cilissa.images import Image


class Transformation(ABC):
    """
    Base class for creating new transformations to use in the program.

    All transformations must implement the `transform` method.
    """

    name: str = ""

    def __init__(self, verbose_name: Optional[str] = None, **kwargs: Any) -> None:
        self.verbose_name = verbose_name

        for k in kwargs.keys():
            logging.info(f"Discarding unexpected keyword argument: {k}")

    def __str__(self) -> str:
        return f"Transformation: {self.verbose_name or self.name}"

    @classmethod
    def get_transformation_name(cls) -> str:
        return cls.name

    @abstractmethod
    def transform(self, image: Image, inplace: bool = False) -> Union[Image, None]:
        raise NotImplementedError("Transformations must implement the `transform` method")


class Blur(Transformation):
    pass


class Sharpen(Transformation):
    pass


class Linear(Transformation):
    """
    Changes brightness of the image with a simple linear transformation.

    g(x) = a * f(x) + b, where `a` controls contrast and `b` controls brightness

    Brightness refers to the overall lightness or darkness of the image.
    Increasing the brightness every pixel in the frame gets lighter.

    Contrast is the difference in brightness between objects in the image.
    Increasing the contrast makes light areas lighter and dark area in the frame becomes much darker.

    Args:
        - contrast (int/float/None):
        Value by which to change the contrast. 1 and None is the original image.
        A float from interval (0, 1) reduces the contrast. Values above 1 increase the contrast.
        - brightness (int/float/None):
        Value by which to change the brightness. 0 and None is the original image.
        Negative values reduce the brightness. Positive values increase the brightness.

    References:
        - https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
    """

    def __init__(
        self, contrast: Optional[Union[int, float]] = None, brightness: Optional[Union[int, float]] = None
    ) -> None:
        self.contrast = contrast
        self.brightness = brightness

    def transform(self, image: Image, inplace: bool = False) -> Union[Image, None]:
        im = image.as_int()
        new_im = cv2.convertScaleAbs(im, alpha=self.contrast, beta=self.brightness)

        if inplace:
            image.replace(new_im)
        else:
            return new_im


class Translation(Transformation):
    pass


class Stretch(Transformation):
    """
    Histogram stretch
    """

    pass


def get_all_transformations() -> Dict[str, Type[Transformation]]:
    subclasses = Transformation.__subclasses__()
    transformations = {}
    for transformation in subclasses:
        transformations[transformation.get_transformation_name()] = transformation

    return transformations
