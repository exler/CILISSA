from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConsoleBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__("Console")

        self.parent = parent

        self.setMaximumHeight(168)

        self.layout = QHBoxLayout()
        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.addWidget(QPushButton("&Clear"))

        self.layout.addWidget(Console(self))
        self.layout.addLayout(self.buttons_panel)
        self.setLayout(self.layout)


class Console(QListWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__()

        self.parent = parent

        # TODO: Implement me
        self.addItem(QListWidgetItem("Metric: MSE, result: 0.67"))
        self.addItem(QListWidgetItem("Metric: SSIM, result: 0.64258"))
