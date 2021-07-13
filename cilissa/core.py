import logging
from typing import List, Mapping, Union

import numpy as np

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImageCollection, ImagePair
from cilissa.metrics import Metric


class ImageAnalyzer:
    """
    ImageAnalyzer analyzes :class:`cilissa.images.ImagePair` and :class:`cilissa.images.ImageCollection`
    using multiple metrics.

    ImageAnalyzer should be given instances of metrics with configured attributes.
    """

    def __init__(self, metrics: List[Metric] = []) -> None:
        self._metrics = metrics

    def add(self, metric: Metric) -> None:
        self._metrics.append(metric)

    def remove(self, metric_name: str) -> None:
        """
        Removal is done by either using the instance's verbose_name or the class name
        """
        for i, metric in enumerate(self._metrics):
            if metric_name == (metric.verbose_name or metric.get_metric_name()):
                del self._metrics[i]

    def replace(self, metrics: List[Metric]) -> None:
        self._metrics = metrics

    def analyze(self, images: Union[ImagePair, ImageCollection]) -> Mapping[str, Union[float, np.float64]]:
        """
        Runs every metric passed to the analyzer on an :class:`cilissa.images.ImagePair`
        Images need to be of equal shape.
        """
        if isinstance(images, ImagePair):
            return self._use_metrics_on_pair(images)
        elif isinstance(images, ImageCollection):
            results = []
            while not ImageCollection.empty():
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
        for metric in self._metrics:
            name = metric.verbose_name if metric.verbose_name else metric.get_metric_name()
            result = metric.analyze(image_pair)

            results[name] = result

        return results


class ImageTransformer:
    pass
