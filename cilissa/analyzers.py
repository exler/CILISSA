import logging
from typing import Dict, List, Optional, Type

import numpy as np

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImagePair
from cilissa.metrics import Metric


class ImageAnalyzer:
    """
    ImageAnalyzer analyzes :class:`cilissa.images.ImagePair` and :class:`cilissa.images.ImageCollection`
    using multiple metrics.

    ImageAnalyzer should be given instances of metrics with configured attributes.
    """

    def __init__(self, metrics: Optional[List[Type[Metric]]] = None) -> None:
        self._metrics = metrics

    def add_metric(self, metric: Type[Metric]) -> None:
        self._metrics.append(metric)

    def remove_metric(self, metric_name: str) -> None:
        """
        Removal is done by either using the instance's verbose_name or the class name
        """
        for i, metric in enumerate(self._metrics):
            if metric_name == (metric.verbose_name or metric.get_metric_name()):
                del self._metrics[i]

    def replace_metrics(self, metrics: List[Type[Metric]]) -> None:
        self._metrics = metrics

    def analyze_pair(self, image_pair: ImagePair) -> Dict[str, np.float64]:
        """
        Runs every metric passed to the analyzer on an :class:`cilissa.images.ImagePair`
        Images need to be of equal shape.
        """
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        if not image_pair.matching_dtype:
            logging.warn(
                "Input images have mismatched data types. Metrics relying on data range will use original image's type."
            )

        results: Dict[str, np.float64] = {}
        for metric in self._metrics:
            name = metric.verbose_name if metric.verbose_name else metric.get_metric_name()
            result = metric.analyze(image_pair)

            results[name] = result

        return results
