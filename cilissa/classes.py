from abc import ABC
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    get_type_hints,
)


class Parameterized(ABC):
    def get_parameters_dict(self) -> Dict[str, Any]:
        d = vars(self)
        return d

    def get_parameter_type(self, parameter: str) -> Union[Type, None]:
        attr = self.get_parameter(parameter, None)
        if attr is not None:
            return type(attr)

        # Try to get the type from type hinting
        try:
            t = get_type_hints(self.__init__).get(parameter)  # type: ignore
            t_args = t.__args__  # type: ignore
            for arg in t_args:
                if not isinstance(None, arg):
                    return arg
        except AttributeError:
            # `t` is a type or None
            return t

        return None

    def set_parameter(self, parameter: str, value: Any) -> None:
        setattr(self, parameter, value)

    def get_parameter(self, parameter: str, default: Optional[Any] = None) -> Any:
        return getattr(self, parameter, default)


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

    def __getitem__(self, index: int) -> Any:
        return self.items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.items[index] = value

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
