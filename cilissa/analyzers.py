from typing import Any, Dict, List, Type

import numpy as np

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImagePair
from cilissa.metrics import Metric


class ImageAnalyzer:
    """ """

    def __init__(self, metrics: List[Type[Metric]]) -> None:
        self._metrics = metrics

    def analyze_pair(self, image_pair: ImagePair) -> Dict[str, Any]:
        """
        Runs every metric passed to the analyzer on an :class:`cilissa.images.ImagePair`
        Images need to be of equal shape.
        """
        if not image_pair.matching_shape:
            raise ShapesNotEqual("Images must be of equal size to analyze")

        results: Dict[str, np.float64] = {}
        for metric in self._metrics:
            name = metric.get_metric_name()
            result = metric.analyze(image_pair)

            results[name] = result

        return results
