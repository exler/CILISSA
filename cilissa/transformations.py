import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, Union

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
    def transform(self, replace: bool = True) -> Union[Image, None]:
        raise NotImplementedError("Transformations must implement the `transform` method")


class Blur(Transformation):
    pass


class Sharpen(Transformation):
    pass


class Brightness(Transformation):
    pass


class Translation(Transformation):
    pass


class Stretch(Transformation):
    pass


def get_all_transformations() -> Dict[str, Type[Transformation]]:
    subclasses = Transformation.__subclasses__()
    transformations = {}
    for transformation in subclasses:
        transformations[transformation.get_transformation_name()] = transformation

    return transformations
