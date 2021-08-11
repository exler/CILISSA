from typing import Any, Iterable, List, Optional, Tuple


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

    def __iter__(self) -> Iterable:
        return iter(self.items)

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
