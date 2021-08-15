import logging
from typing import Any, Callable, Type, Union

from cilissa.classes import AnalysisResult, OrderedList
from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImageCollection, ImagePair
from cilissa.operations import ImageOperation, Metric, Transformation


class OperationsList(OrderedList):
    def run(self, images: Union[ImagePair, ImageCollection]) -> Any:
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

    def _get_function_for_operation(self, operation: Type[ImageOperation]) -> Callable:
        if isinstance(operation, Metric):
            return self._use_metric
        elif isinstance(operation, Transformation):
            return self._use_transformation
        else:
            raise TypeError("Operations must be of type: Metric, Transformation")

    def _use_operations_on_pair(self, image_pair: ImagePair) -> Any:
        results = []
        for operation in self:
            func = self._get_function_for_operation(operation)
            result = func(operation, image_pair)
            if result is not None:
                results.append(result)

        return results

    def _use_metric(self, metric: Metric, image_pair: ImagePair) -> AnalysisResult:
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        if not image_pair.matching_dtype:
            logging.warn(
                "Input images have mismatched data types. Metrics relying on data range will use original image's type."
            )

        return metric.analyze(image_pair)

    def _use_transformation(self, transformation: Transformation, image_pair: ImagePair) -> None:
        new_im = transformation.transform(image_pair.A)
        image_pair.A.from_array(new_im.im)
