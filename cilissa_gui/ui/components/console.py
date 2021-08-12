from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)


class ConsoleBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Console")

        self.console = Console()

        self.setMaximumHeight(168)

        self.main_layout = QHBoxLayout()
        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.addWidget(QPushButton("&Clear"))

        self.main_layout.addWidget(self.console)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)


class Console(QListWidget):
    def __init__(self) -> None:
        super().__init__()

    def add_item(self, item: str) -> None:
        self.addItem(QListWidgetItem(item))
