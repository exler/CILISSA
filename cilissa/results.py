from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Union

import numpy as np

from cilissa.classes import Parameterized
from cilissa.images import Image


@dataclass(frozen=True)  # type: ignore
class Result(Parameterized, ABC):
    name: str
    parameters: Dict[str, Any]

    @abstractmethod
    def pretty(self) -> str:
        pass


@dataclass(frozen=True)
class AnalysisResult(Result):
    value: Union[float, np.float64]

    def __eq__(self, o: Any) -> bool:
        if isinstance(o, AnalysisResult):
            return self.name == o.name and np.isclose(self.value, o.value, rtol=1e-05, atol=1e-08, equal_nan=False)
        elif isinstance(o, float):
            return np.isclose(self.value, o, rtol=1e-05, atol=1e-08, equal_nan=False)
        else:
            return self.value == o

    def __lt__(self, o: Any) -> bool:
        if isinstance(o, AnalysisResult):
            return self.name == o.name and np.less(self.value, o.value)
        else:
            return np.less(self.value, o)

    def __le__(self, o: Any) -> bool:
        return self == o or self < o

    def __gt__(self, o: Any) -> bool:
        if isinstance(o, AnalysisResult):
            return self.name == o.name and np.greater(self.value, o.value)
        else:
            return np.greater(self.value, o)

    def __ge__(self, o: Any) -> bool:
        return self == o or self > o

    def pretty(self) -> str:
        return f"Analysis - metric: {self.name}, result: {round(self.value, 4)}"


@dataclass(frozen=True, eq=False, order=False)
class TransformationResult(Result):
    before: Image
    after: Image

    def pretty(self) -> str:
        return f"Transformation - name: {self.name}"
