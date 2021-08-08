import logging
from typing import Any, Callable, List, Optional, Tuple, Type, Union

import numpy as np

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImageCollection, ImagePair
from cilissa.operations import ImageOperation, Metric, Transformation


class OrderedQueue:
    """
    Simple synchronous FIFO queue that can be reordered.

    Implements a subset of :type:`queue.Queue` operations.

    Implements additional `get_order` and `change_order` methods to manage the queue's order.
    """

    queue: List[Any] = []

    def __init__(self, items: List[Any] = []) -> None:
        self.clear()
        for item in items:
            self.push(item)

    @property
    def is_empty(self) -> bool:
        return not self.queue

    def push(self, item: Any) -> None:
        self.queue.append(item)

    def pop(self, index: Optional[int] = None) -> Any:
        if index:
            return self.queue.pop(index)

        return self.queue.pop(0)

    def get_order(self) -> List[Tuple[int, Any]]:
        return [(index, element) for index, element in enumerate(self.queue)]

    def change_order(self, a: int, b: int) -> None:
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

    def clear(self) -> None:
        self.queue = []


class OperationsQueue(OrderedQueue):
    def run(self, images: Union[ImagePair, ImageCollection], **kwargs: Any) -> Any:
        if isinstance(images, ImagePair):
            return self._use_operations_on_pair(images)
        elif isinstance(images, ImageCollection):
            results = []
            while not images.empty():
                res = self._use_operations_on_pair(images.get(block=True))
                results.append(res)

            return results
        else:
            raise TypeError("Objects must be of type ImagePair, ImageCollection")

    def _get_function_for_operation(self, operation: Type[ImageOperation]) -> Callable:
        if isinstance(operation, Metric):
            return self._use_metric_on_pair
        elif isinstance(operation, Transformation):
            return self._use_transformation_on_image
        else:
            raise TypeError("Operations must be of type Metric, Transformation")

    def _use_operations_on_pair(self, image_pair: ImagePair) -> Any:
        results = []
        while not self.is_empty:
            operation = self.pop()
            func = self._get_function_for_operation(operation)
            result = func(operation, image_pair)
            if result is not None:
                results.append(result)

        return results

    def _use_metric_on_pair(self, metric: Metric, image_pair: ImagePair) -> Union[float, np.float64]:
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        if not image_pair.matching_dtype:
            logging.warn(
                "Input images have mismatched data types. Metrics relying on data range will use original image's type."
            )

        return metric.analyze(image_pair)

    def _use_transformation_on_image(self, transformation: Transformation, image_pair: ImagePair) -> None:
        new_im = transformation.transform(image_pair.A)
        image_pair.A.from_array(new_im.im)
