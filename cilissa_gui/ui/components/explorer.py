from pathlib import Path
from typing import Any, List

from PySide6.QtCore import QDir
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QTabWidget, QWidget


class Explorer(QTabWidget):
    IMAGE_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]

    def __init__(self) -> None:
        super().__init__()

        self.images_tab = ImagesTab()
        self.metrics_tab = MetricsTab()
        self.transformations_tab = TransformationsTab()

        self.addTab(self.images_tab, "Images")
        self.addTab(self.metrics_tab, "Metrics")
        self.addTab(self.transformations_tab, "Transformations")

    def open_image_dialog(self) -> None:
        # This return a tuple ([filenames], "filter"), we are interested only in the filenames
        filenames = QFileDialog.getOpenFileNames(
            self, "Open images...", None, f"Images ({' '.join([ext for ext in self.IMAGE_EXTENSIONS])})"
        )[0]
        for fn in filenames:
            # TODO: Open as CILISSA Image, make QWidget of it and show thumbnail
            self.images_tab.add_item(QLabel(fn))

    def open_image_folder_dialog(self) -> None:
        dirname = QFileDialog.getExistingDirectory(self, "Open images folder...", None, QFileDialog.ShowDirsOnly)
        d = QDir(dirname)

        for fn in d.entryList(self.IMAGE_EXTENSIONS):
            # TODO: Open as CILISSA Image, make QWidget of it and show thumbnail
            path = Path(dirname, fn)
            self.images_tab.add_item(QLabel(str(path.resolve())))


class ExplorerTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.items: List[Any] = []

    def add_item(self, item: Any) -> None:
        self.layout.addWidget(item, self.get_row(), self.get_column())
        self.items.append(item)

    def get_row(self) -> int:
        return int((len(self.items) - len(self.items) % 2) / 2)

    def get_column(self) -> int:
        return len(self.items) % 2


class ImagesTab(ExplorerTab):
    def __init__(self) -> None:
        super().__init__()


class MetricsTab(ExplorerTab):
    pass


class TransformationsTab(ExplorerTab):
    pass
