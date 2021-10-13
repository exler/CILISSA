from abc import abstractmethod
from typing import Any, Optional, Union

from PySide6.QtWidgets import QCheckBox, QDoubleSpinBox, QHBoxLayout, QLabel, QSpinBox

from cilissa_gui.widgets.inputs.base import (
    MAX_NEG_INTEGER,
    MAX_POS_INTEGER,
    CQInputWidget,
)


class CQNumberInputWidget(CQInputWidget):
    sb: Union[QSpinBox, QDoubleSpinBox]

    @abstractmethod
    def __init__(
        self, parameter: str, default: Optional[Union[int, float]], label: Optional[str] = None, optional: bool = False
    ) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()

        self.sb.setMinimumWidth(104)
        self.sb.setRange(MAX_NEG_INTEGER, MAX_POS_INTEGER)
        self.sb.setSingleStep(1)
        if default:
            self.sb.setValue(default)

        self.none_checkbox = None
        if optional:
            checked = False if default is None else True
            self.sb.setDisabled(not checked)
            self.none_checkbox = QCheckBox(checked=checked)
            self.none_checkbox.clicked.connect(self.change_spinbox_state)
            layout.addWidget(self.none_checkbox)

        layout.addWidget(QLabel(label or parameter))
        layout.addWidget(self.sb)
        self.setLayout(layout)

    def change_spinbox_state(self) -> None:
        self.sb.setDisabled(self.sb.isEnabled())

    def get_value(self) -> Any:
        if self.none_checkbox and not self.none_checkbox.isChecked():
            return None
        return self.sb.value()


class CQIntInputWidget(CQNumberInputWidget):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.sb = QSpinBox()

        super().__init__(*args, **kwargs)


class CQFloatInputWidget(CQNumberInputWidget):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.sb = QDoubleSpinBox()

        super().__init__(*args, **kwargs)
