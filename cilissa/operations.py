import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Union

import numpy as np

from cilissa.images import Image, ImagePair


class ImageOperation(ABC):
    name: str = ""

    def __init__(self, verbose_name: Optional[str] = None, **kwargs: Any) -> None:
        self.verbose_name = verbose_name

        for k in kwargs.keys():
            logging.info(f"Discarding unexpected keyword argument: {k}")

    def __str__(self) -> str:
        return self.verbose_name or self.name

    @classmethod
    def get_class_name(cls) -> str:
        return cls.name


class Transformation(ImageOperation, ABC):
    """
    Base class for creating new transformations to use in the program.

    All transformations must implement the `transform` method.
    """

    @abstractmethod
    def transform(self, image: Image) -> Image:
        raise NotImplementedError("Transformations must implement the `transform` method")


class Metric(ImageOperation, ABC):
    """
    Base class for creating new metrics to use in the program.

    All metrics must implement the `analyze` method.
    """

    @abstractmethod
    def analyze(self, image_pair: ImagePair) -> Union[float, np.float64]:
        raise NotImplementedError("Metrics must implement the `analyze` method")
