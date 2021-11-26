import inspect
from abc import ABC
from typing import Any, Dict, Iterator, List, Optional, Tuple, Type, Union


class Parameterized(ABC):
    def get_parameters_dict(self) -> Dict[str, Any]:
        d = vars(self)
        return d

    def get_parameter_type(self, parameter: str) -> Tuple[Union[Type, None], bool]:
        """
        Gets class variable's type from the `__init__` function.

        Works best if the function is type hinted, fallbacks to variable's value type.
        """
        signature = inspect.signature(self.__init__)  # type: ignore
        parameter_obj = signature.parameters.get(parameter, None)
        if parameter_obj:
            annotation = parameter_obj.annotation
            try:
                if annotation.__origin__ == Union:
                    t = annotation.__args__
                    optional = type(None) in t
                    return t[0], optional
            except AttributeError:
                t = annotation
                return t, False

        attr = self.get_parameter(parameter, None)
        if attr is not None:
            return type(attr), False

        return None, True

    def set_parameter(self, parameter: str, value: Any) -> None:
        setattr(self, parameter, value)

    def get_parameter(self, parameter: str, default: Optional[Any] = None) -> Any:
        return getattr(self, parameter, default)


class OrderedList:
    """
    Simple list that can be reordered.

    Behaviour similar to `list`, but does not derive from it to avoid lay-out conflict with QObject

    Implements `get_order` and `change_order` methods to manage the list's order.
    """

    def __init__(self, items: List[Any] = []) -> None:
        self.items = list(items)

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

    def pop(self, index: int = -1) -> Any:
        return self.items.pop(index)

    def get_order(self) -> List[Tuple[int, Any]]:
        return [(index, element) for index, element in enumerate(self.items)]

    def change_order(self, a: int, b: int) -> None:
        self.items[a], self.items[b] = self.items[b], self.items[a]

    def clear(self) -> None:
        self.items = []
