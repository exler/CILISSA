from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from cilissa_gui.widgets import CQResult, CQResultDialog


class ConsoleBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Console")

        self.console = Console()

        self.setMaximumHeight(168)

        self.main_layout = QHBoxLayout()

        self.clear_button = QPushButton(QIcon(":erase"), "")
        self.clear_button.clicked.connect(self.clear_console)

        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.setAlignment(Qt.AlignTop)
        self.buttons_panel.addWidget(self.clear_button)

        self.main_layout.addWidget(self.console)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)

    @Slot()
    def clear_console(self) -> None:
        self.console.clear()


class Console(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.itemDoubleClicked.connect(self.open_result_dialog)

    @Slot(QListWidgetItem)
    def open_result_dialog(self, item: QListWidgetItem) -> None:
        dialog = CQResultDialog(item.result)
        dialog.exec()

    def add_item(self, item: str) -> None:
        self.addItem(CQResult(item))
