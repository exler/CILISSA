from typing import Union

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class Properties(QVBoxLayout):
    def __init__(self) -> None:
        super().__init__()

        self.addWidget(QCheckBox("Boolean"))
        self.create_input("Example")

    def create_input(self, label: str, default: Union[str, int, None] = None) -> None:
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(QLineEdit(str(default)))
        self.addLayout(layout)
