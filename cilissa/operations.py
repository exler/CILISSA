from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from typing import Any, List, Type, Union

from cilissa.classes import OrderedList, Parameterized
from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.results import Result


class ImageOperation(Parameterized, ABC):
    """
    Base class for all operations that can be performed on an image.

    Display name and name used in various dicts is deduced from the class name.
    """

    @classmethod
    def get_subclasses(cls) -> List[Type[ImageOperation]]:
        subclasses = []

        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            subclasses.extend(subclass.get_subclasses())

        return subclasses

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_display_name(cls) -> str:
        return cls.get_class_name().upper()

    @abstractmethod
    def run(self, image_pair: ImagePair) -> Result:
        raise NotImplementedError("All ImageOperation subclasses must implement the `run` method")

    def generate_result(self, **kwargs: Any) -> Result:
        return Result(name=self.get_display_name(), parameters=deepcopy(self.get_parameters_dict()), **kwargs)


class OperationsList(OrderedList):
    def run_all(self, images: Union[ImagePair, ImageCollection]) -> Any:
        if isinstance(images, ImagePair):
            pair_copy = images.copy()
            res = self._use_operations_on_pair(pair_copy)
            return res

        elif isinstance(images, ImageCollection):
            with ThreadPoolExecutor(max_workers=None) as executor:
                futures = {
                    executor.submit(self._use_operations_on_pair, pair.copy()): index
                    for index, pair in images.get_order()
                }

                results = {}
                for future in as_completed(futures):
                    results[futures[future]] = future.result()

            # Sort results to their original order
            return [result[1] for result in sorted(results.items())]
        else:
            raise TypeError("Objects must be of type: ImagePair, ImageCollection")

    def _use_operations_on_pair(self, image_pair: ImagePair) -> List[Result]:
        results = []
        for operation in self:
            result = operation.run(image_pair)
            if result is not None:
                results.append(result)

        return results


class Transformation(ImageOperation, ABC):
    """
    Base class for creating new transformations to use in the program.
    """

    @classmethod
    def get_display_name(cls) -> str:
        return cls.get_class_name().capitalize()

    @abstractmethod
    def transform(self, image: Image) -> Image:
        pass

    def run(self, image_pair: ImagePair) -> Result:
        image = image_pair[1]
        transformed_image = self.transform(image)
        image_pair[1] = transformed_image
        return self.generate_result(type=Transformation, value=transformed_image)


class Metric(ImageOperation, ABC):
    """
    Base class for creating new metrics to use in the program.
    """

    @abstractmethod
    def analyze(self, image_pair: ImagePair) -> float:
        pass

    def run(self, image_pair: ImagePair) -> Result:
        value = self.analyze(image_pair)
        return self.generate_result(type=Metric, value=value)
