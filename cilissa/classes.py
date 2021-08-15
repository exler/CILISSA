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

    def __eq__(self, o: object) -> bool:
        return self.name == o.name and np.isclose(self.value, o.value, rtol=1e-05, atol=1e-08, equal_nan=False)

    def __lt__(self, o: object) -> bool:
        return self.name == o.name and self.value < o.value

    def __le__(self, o: object) -> bool:
        return self == o or self < o

    def __gt__(self, o: object) -> bool:
        return self.name == o.name and self.value > o.value

    def __ge__(self, o: object) -> bool:
        return self == o or self > o
