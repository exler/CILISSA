import logging
from abc import ABC
from typing import Any, Optional


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
