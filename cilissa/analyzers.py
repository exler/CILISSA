from typing import Any, Dict, List, Type

import numpy as np

from cilissa.images import ImagePair
from cilissa.metrics import Metric


class ImageAnalyzer:
    """ """

    def __init__(self, metrics: List[Type[Metric]]) -> None:
        self._metrics = metrics

    def analyze_pair(self, image_pair: ImagePair) -> Dict[str, Any]:
        """
        Runs every metric passed to the analyzer on an :class:`cilissa.images.ImagePair`
        """
        results: Dict[str, np.float64] = {}
        for metric in self._metrics:
            m = metric(image_pair)
            name = m.get_metric_name()
            result = m.analyze()

            results[name] = result

        return results
