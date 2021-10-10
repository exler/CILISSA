from pathlib import Path

from PySide6.QtCore import QDir, QSize
from PySide6.QtWidgets import QFileDialog, QListWidget, QTabWidget

from cilissa.images import Image
from cilissa.metrics import all_metrics
from cilissa.transformations import all_transformations
from cilissa_gui.widgets import CQImageItem, CQOperationItem


class Explorer(QTabWidget):
    IMAGE_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]

    def __init__(self) -> None:
        super().__init__()

        self.images_tab = ImagesTab(self)
        self.metrics_tab = MetricsTab(self)
        self.transformations_tab = TransformationsTab(self)

        self.addTab(self.images_tab, "Images")
        self.addTab(self.metrics_tab, "Metrics")
        self.addTab(self.transformations_tab, "Transformations")

        self.currentChanged.connect(self.clear_selection_in_tabs)

    def clear_selection_in_tabs(self) -> None:
        for index in range(self.count()):
            self.widget(index).clearSelection()

    def open_image_dialog(self) -> None:
        # This returns a tuple ([filenames], "filter"), we are interested only in the filenames
        filenames = QFileDialog.getOpenFileNames(
            self, "Open images...", "", f"Images ({' '.join([ext for ext in self.IMAGE_EXTENSIONS])})"
        )[0]

        for fn in filenames:
            image = Image(fn)
            cq_image = CQImageItem(image, width=128, height=128)
            self.images_tab.addItem(cq_image)

    def open_image_folder_dialog(self) -> None:
        dirname = QFileDialog.getExistingDirectory(self, "Open images folder...", "", QFileDialog.ShowDirsOnly)
        d = QDir(dirname)

        for fn in d.entryList(self.IMAGE_EXTENSIONS):
            image = Image(Path(dirname, fn))
            cq_image = CQImageItem(image, width=128, height=128)
            self.images_tab.addItem(cq_image)


class ExplorerTab(QListWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__()

        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(82, 82))
        self.setUniformItemSizes(True)
        self.setMovement(QListWidget.Static)
        self.setResizeMode(QListWidget.Adjust)
        self.setFrameStyle(QListWidget.NoFrame)

        self.setMaximumWidth(parent.width())

    def remove_selected(self) -> None:
        rows = [index.row() for index in self.selectedIndexes()]
        for row in rows:
            self.takeItem(row)


class ImagesTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.setSelectionMode(QListWidget.ExtendedSelection)


class MetricsTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        for metric in all_metrics.values():
            self.addItem(CQOperationItem(metric))


class TransformationsTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        for transformation in all_transformations.values():
            self.addItem(CQOperationItem(transformation))
