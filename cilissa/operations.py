import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Union

import numpy as np

from cilissa.classes import AnalysisResult
from cilissa.images import Image, ImagePair


class ImageOperation(ABC):
    name: str = ""

    def __init__(self, **kwargs: Any) -> None:
        for k in kwargs.keys():
            logging.info(f"Discarding unexpected keyword argument: {k}")

    def __str__(self) -> str:
        return self.get_class_name()

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
    def analyze(self, image_pair: ImagePair) -> AnalysisResult:
        raise NotImplementedError("Metrics must implement the `analyze` method")

    def get_parameters_dict(self) -> Dict[str, Any]:
        d = vars(self)
        return d

    def generate_result(self, value: Union[float, np.float64]) -> AnalysisResult:
        return AnalysisResult(name=str(self), parameters=self.get_parameters_dict(), value=value)
