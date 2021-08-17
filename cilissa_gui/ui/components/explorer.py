from pathlib import Path
from typing import Any

from PySide6.QtCore import QDir, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QFrame, QTableWidget, QTabWidget, QWidget

from cilissa.metrics import all_metrics
from cilissa.transformations import all_transformations
from cilissa_gui.widgets import CQImage, CQOperation


class Explorer(QTabWidget):
    IMAGE_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]

    explorerItemSelected = Signal(QWidget)

    def __init__(self) -> None:
        super().__init__()

        self.images_tab = ImagesTab(self)
        self.metrics_tab = MetricsTab(self)
        self.transformations_tab = TransformationsTab(self)

        self.addTab(self.images_tab, "Images")
        self.addTab(self.metrics_tab, "Metrics")
        self.addTab(self.transformations_tab, "Transformations")

    def open_image_dialog(self) -> None:
        # This return a tuple ([filenames], "filter"), we are interested only in the filenames
        filenames = QFileDialog.getOpenFileNames(
            self, "Open images...", "", f"Images ({' '.join([ext for ext in self.IMAGE_EXTENSIONS])})"
        )[0]
        for fn in filenames:
            image = CQImage.load(fn)
            self.images_tab.add_item(image)

    def open_image_folder_dialog(self) -> None:
        dirname = QFileDialog.getExistingDirectory(self, "Open images folder...", "", QFileDialog.ShowDirsOnly)
        d = QDir(dirname)

        for fn in d.entryList(self.IMAGE_EXTENSIONS):
            path = Path(dirname, fn)
            image = CQImage.load(path.resolve())
            self.images_tab.add_item(image)


class ExplorerTab(QTableWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__()

        self.setShowGrid(False)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(96)
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(96)
        self.verticalHeader()
        self.setFrameStyle(QFrame.NoFrame)
        self.setMaximumWidth(parent.width())

        self.cell_counter = 0

        self.cellClicked.connect(self.get_selected_widget)

    def add_item(self, item: Any) -> None:
        row = self.get_next_row()
        column = self.get_next_column()

        if row >= self.rowCount():
            self.insertRow(row)

        self.setCellWidget(row, column, item)
        self.cell_counter += 1

    def get_item(self, row: int, column: int) -> Any:
        return self.cellWidget(row, column)

    def get_next_row(self) -> int:
        return int((self.cell_counter - self.cell_counter % 2) / 2)

    def get_next_column(self) -> int:
        return self.cell_counter % 2

    @Slot()
    def get_selected_widget(self, row: int, column: int) -> None:
        widget = self.get_item(row, column)
        self.parent().parent().explorerItemSelected.emit(widget)


class ImagesTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

    @Slot()
    def enable_add_pair(self) -> None:
        interface = self.parent().parent().parent().parent().parent()
        if len(self.selectedIndexes()) == 2:
            interface.add_pair_action.setEnabled(True)
        else:
            interface.add_pair_action.setEnabled(False)


class MetricsTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        for metric in all_metrics.values():
            self.add_item(CQOperation(metric))


class TransformationsTab(ExplorerTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        for transformation in all_transformations.values():
            self.add_item(CQOperation(transformation))
