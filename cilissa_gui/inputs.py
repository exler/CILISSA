from abc import abstractmethod
from typing import Any, Optional, Type, Union

from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QWidget,
)


def get_input_widget_for_type(input_type: Union[Type, None]) -> Union[QWidget, None]:
    if not input_type:
        return None

    if isinstance(1, input_type):
        return CQIntInputWidget
    elif isinstance(1.0, input_type):
        return CQFloatInputWidget
    elif isinstance(True, input_type):
        return CQBooleanInputWidget
    else:
        return None


class CQInputWidget(QWidget):
    def __init__(self, parameter: str) -> None:
        super().__init__()

        self.parameter = parameter

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError("Input widgets must implement the `get_value` method")


class CQIntInputWidget(CQInputWidget):
    def __init__(self, parameter: str, default: Optional[Union[int, float]], label: Optional[str] = None) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label or parameter))

        self.sb = QSpinBox()
        self.sb.setSingleStep(1)
        if default:
            self.sb.setValue(default)
        layout.addWidget(self.sb)

        self.setLayout(layout)

    def get_value(self) -> Any:
        return self.sb.value()


class CQFloatInputWidget(CQInputWidget):
    def __init__(self, parameter: str, default: Optional[Union[int, float]], label: Optional[str] = None) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label or parameter))

        self.sb = QDoubleSpinBox()
        self.sb.setSingleStep(1)
        if default:
            self.sb.setValue(default)
        layout.addWidget(self.sb)

        self.setLayout(layout)

    def get_value(self) -> Any:
        return self.sb.value()


class CQBooleanInputWidget(CQInputWidget):
    def __init__(self, parameter: str, default: bool, label: Optional[str] = None) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()

        self.cb = QCheckBox(label or parameter, checked=default)
        layout.addWidget(self.cb)

        self.setLayout(layout)

    def get_value(self) -> Any:
        return self.cb.isChecked()
