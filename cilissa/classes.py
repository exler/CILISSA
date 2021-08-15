from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import numpy as np


class OrderedList:
    """
    Simple list that can be reordered.

    Behaviour similar to :type:`list`, but does not derive from it to avoid lay-out conflict with QObject

    Implements `get_order` and `change_order` methods to manage the list's order.
    """

    items: List[Any] = []

    def __init__(self, items: List[Any] = []) -> None:
        self.clear()
        for item in items:
            self.push(item)

    def __str__(self) -> str:
        return f"OrderedList(items=[{', '.join([str(item) for item in self.items])}])"

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.items)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self, index: Optional[int] = None) -> Any:
        if index:
            return self.items.pop(index)

        return self.items.pop(0)

    def get_order(self) -> List[Tuple[int, Any]]:
        return [(index, element) for index, element in enumerate(self.items)]

    def change_order(self, a: int, b: int) -> None:
        self.items[a], self.items[b] = self.items[b], self.items[a]

    def clear(self) -> None:
        self.items = []


@dataclass(frozen=True)
class AnalysisResult:
    name: str
    parameters: Dict[str, Any]
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
