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

        self.setMaximumHeight(168)

        self.main_layout = QHBoxLayout()
        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.addWidget(QPushButton("&Clear"))

        self.main_layout.addWidget(Console())
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)


class Console(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        # TODO: Implement me
        self.addItem(QListWidgetItem("Metric: MSE, result: 0.67"))
        self.addItem(QListWidgetItem("Metric: SSIM, result: 0.64258"))
