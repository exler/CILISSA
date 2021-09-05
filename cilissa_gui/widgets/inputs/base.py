from abc import abstractmethod
from typing import Any

from PySide6.QtWidgets import QWidget


class CQInputWidget(QWidget):
    def __init__(self, parameter: str) -> None:
        super().__init__()

        self.parameter = parameter

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError("Input widgets must implement the `get_value` method")
