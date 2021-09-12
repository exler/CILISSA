from typing import Any, Optional, Union

from PySide6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QSpinBox

from cilissa_gui.widgets.inputs.base import (
    MAX_NEG_INTEGER,
    MAX_POS_INTEGER,
    CQInputWidget,
)


class CQIntInputWidget(CQInputWidget):
    def __init__(self, parameter: str, default: Optional[Union[int, float]], label: Optional[str] = None) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label or parameter))

        self.sb = QSpinBox()
        self.sb.setRange(MAX_NEG_INTEGER, MAX_POS_INTEGER)
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
        self.sb.setRange(MAX_NEG_INTEGER, MAX_POS_INTEGER)
        self.sb.setSingleStep(1)
        if default:
            self.sb.setValue(default)
        layout.addWidget(self.sb)

        self.setLayout(layout)

    def get_value(self) -> Any:
        return self.sb.value()
