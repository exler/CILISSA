from abc import ABC, abstractmethod
from typing import Any, List, Type, Union

from cilissa.classes import OrderedList, Parameterized
from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.results import AnalysisResult, Result, TransformationResult


class ImageOperation(Parameterized, ABC):
    """
    Base class for all operations that can be performed on an image.

    Display name and name used in various dicts is deduced from the class name.
    """

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_display_name(cls) -> str:
        return cls.get_class_name().upper()

    @abstractmethod
    def run(self, image_pair: ImagePair) -> Result:
        raise NotImplementedError("All ImageOperation subclasses must implement the `run` method")

    @abstractmethod
    def get_result_type(self) -> Type[Result]:
        raise NotImplementedError("All ImageOperation subclasses must implement the `get_result_type` method")

    def generate_result(self, **kwargs: Any) -> Result:
        result_type = self.get_result_type()
        return result_type(
            name=self.get_display_name(),
            parameters=self.get_parameters_dict(),
            **kwargs,
        )  # type: ignore


class OperationsList(OrderedList):
    def run_all(self, images: Union[ImagePair, ImageCollection], keep_changes: bool = False) -> Any:
        if isinstance(images, ImagePair):
            pair_copy = images.copy()
            res = self._use_operations_on_pair(pair_copy)

            if keep_changes:
                images = pair_copy

            return res

        elif isinstance(images, ImageCollection):
            results = []
            for index, pair in enumerate(images):
                pair_copy = pair.copy()
                res = self._use_operations_on_pair(pair_copy)
                results.append(res)

                if keep_changes:
                    images[index] = pair_copy

            return results
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

    def get_result_type(self) -> Type[Result]:
        return TransformationResult

    @abstractmethod
    def transform(self, image: Image) -> Image:
        pass

    def run(self, image_pair: ImagePair) -> Result:
        image = image_pair[1]
        transformed_image = self.transform(image)
        image_pair[1] = transformed_image
        return self.generate_result(value=transformed_image)


class Metric(ImageOperation, ABC):
    """
    Base class for creating new metrics to use in the program.
    """

    def get_result_type(self) -> Type[Result]:
        return AnalysisResult

    @abstractmethod
    def analyze(self, image_pair: ImagePair) -> float:
        pass

    def run(self, image_pair: ImagePair) -> Result:
        value = self.analyze(image_pair)
        return self.generate_result(value=value)
