import logging
from abc import ABC, abstractmethod
from typing import Any, List, Type, Union

from cilissa.classes import OrderedList, Parameterized
from cilissa.exceptions import ShapesNotEqual
from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.results import AnalysisResult, Result, TransformationResult


class ImageOperation(Parameterized, ABC):
    name: str = ""

    def __str__(self) -> str:
        return self.get_class_name()

    @classmethod
    def get_class_name(cls) -> str:
        return cls.name

    @abstractmethod
    def run(self, image_pair: ImagePair) -> Result:
        raise NotImplementedError("All ImageOperation subclasses must implement the `run` method")

    @abstractmethod
    def get_result_type(self) -> Type[Result]:
        raise NotImplementedError("All ImageOperation subclasses must implement the `get_result_type` method")

    def generate_result(self, **kwargs: Any) -> Result:
        result_type = self.get_result_type()
        return result_type(name=str(self), parameters=self.get_parameters_dict(), **kwargs)  # type: ignore


class OperationsList(OrderedList):
    def run_all(self, images: Union[ImagePair, ImageCollection]) -> Any:
        if isinstance(images, ImagePair):
            return self._use_operations_on_pair(images)
        elif isinstance(images, ImageCollection):
            results = []
            for pair in images:
                res = self._use_operations_on_pair(pair)
                results.append(res)

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

    def get_result_type(self) -> Type[Result]:
        return TransformationResult

    @abstractmethod
    def transform(self, image: Image) -> Image:
        pass

    def run(self, image_pair: ImagePair) -> Result:
        image = image_pair[1]
        transformed_image = self.transform(image)
        image_pair[1] = transformed_image
        return self.generate_result(before=image, after=transformed_image)


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
        self.validate(image_pair)
        value = self.analyze(image_pair)
        return self.generate_result(value=value)

    def validate(self, image_pair: ImagePair) -> None:
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        if not image_pair.matching_dtype:
            logging.warn("Images have mismatched data types. Metrics will use reference image's type")
