from typing import Any

from PySide6.QtWidgets import QGridLayout, QLabel, QTabWidget, QWidget


class Explorer(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.addTab(ImagesTab(), "Images")
        self.addTab(MetricsTab(), "Metrics")
        self.addTab(TransformationsTab(), "Transformations")


class ExplorerTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.items = []

    def add_item(self, item: Any) -> None:
        self.layout.addWidget(item, self.get_row(), self.get_column())
        self.items.append(item)

    def get_row(self) -> int:
        return (len(self.items) - len(self.items) % 2) / 2

    def get_column(self) -> int:
        return len(self.items) % 2


class ImagesTab(ExplorerTab):
    def __init__(self) -> None:
        super().__init__()

        self.add_item(QLabel("(0, 0)"))
        self.add_item(QLabel("(0, 1)"))
        self.add_item(QLabel("(1, 0)"))


class MetricsTab(ExplorerTab):
    pass


class TransformationsTab(ExplorerTab):
    pass
