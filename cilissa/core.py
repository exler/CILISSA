import logging
from abc import ABC, abstractmethod
from queue import PriorityQueue
from typing import Any, List, Mapping, Optional, Tuple, Union

import numpy as np

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.metrics import Metric
from cilissa.operations import ImageOperation
from cilissa.transformations import Transformation


class OperationsHandler(ABC):
    operations: List[ImageOperation] = []

    def __init__(self, operations: List[ImageOperation] = []) -> None:
        for op in operations:
            self.push(op)

    def push(self, operation: ImageOperation) -> None:
        self.operations.append(operation)

    def pop(self, operation_name: str) -> Union[None, ImageOperation]:
        """
        Popping is done by either using the instance's verbose_name or the class name
        """
        for i, op in enumerate(self.operations):
            if operation_name == (op.verbose_name or op.get_class_name()):
                return self.operations.pop(i)

        return None

    def clear(self) -> None:
        self.operations = []


class ImageAnalyzer(OperationsHandler):
    """
    ImageAnalyzer analyzes :class:`cilissa.images.ImagePair` and :class:`cilissa.images.ImageCollection`
    using multiple metrics.

    ImageAnalyzer should be given instances of metrics with configured attributes.
    """

    def analyze(self, images: Union[ImagePair, ImageCollection]) -> Any:
        """
        Runs every metric passed to the analyzer on an :class:`cilissa.images.ImagePair`
        Images need to be of equal shape.
        """
        if isinstance(images, ImagePair):
            return self._use_metrics_on_pair(images)
        elif isinstance(images, ImageCollection):
            results = []
            while not images.empty():
                res = self._use_metrics_on_pair(images.get(block=True))
                results.append(res)
            return results
        else:
            raise TypeError("ImageAnalyzer can only be used on objects of type ImagePair, ImageCollection")

    def _use_metrics_on_pair(self, image_pair: ImagePair) -> Mapping[str, Union[float, np.float64]]:
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        if not image_pair.matching_dtype:
            logging.warn(
                "Input images have mismatched data types. Metrics relying on data range will use original image's type."
            )

        results = {}
        for metric in self.operations:
            name = metric.verbose_name if metric.verbose_name else metric.get_class_name()
            results[name] = metric.analyze(image_pair)  # type: ignore

        return results


class ImageTransformer(OperationsHandler):
    """
    ImageAnalyzer analyzes :class:`cilissa.images.ImagePair` and :class:`cilissa.images.ImageCollection`
    using multiple metrics.

    ImageTransformer should be given instances of metrics with configured attributes.
    """

    def transform(
        self, target: Union[Image, ImagePair, ImageCollection], inplace: bool = False
    ) -> Union[None, Image, ImagePair, ImageCollection]:
        if isinstance(target, Image):
            return self._use_transformations_on_image(target, inplace=inplace)
        elif isinstance(target, ImagePair):
            return self._use_transformations_on_image(target.A, inplace=inplace)
        elif isinstance(target, ImageCollection):
            results = []
            while not target.empty():
                res = self._use_transformations_on_image(target.get(block=True).A, inplace=inplace)
                results.append(res)

            if not inplace:
                return ImageCollection(results)
            return None
        else:
            raise TypeError("ImageTransformer can only be used on objects of type Image, ImagePair, ImageCollection")

    def _use_transformations_on_image(self, image: Image, inplace: bool = False) -> Union[None, Image]:
        new_im = image
        for transformation in self.operations:
            new_im = transformation.transform(new_im)  # type: ignore

        if inplace:
            image.from_array(new_im.im)
            return None
        else:
            return new_im
