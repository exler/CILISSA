from typing import Any, Optional

from PySide6.QtWidgets import QCheckBox, QHBoxLayout

from cilissa_gui.widgets.inputs.base import CQInputWidget


class CQBooleanInputWidget(CQInputWidget):
    def __init__(self, parameter: str, default: bool, label: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(parameter)

        layout = QHBoxLayout()

        self.cb = QCheckBox(label or parameter, checked=default)
        layout.addWidget(self.cb)

        self.setLayout(layout)

    def get_value(self) -> Any:
        return self.cb.isChecked()
