from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from cilissa.images import ImagePair
from cilissa.results import Result, ResultGenerator
from cilissa_gui.widgets import CQResultsDialog, CQResultsItem


class ConsoleBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Console")

        self.console = Console()

        self.setMaximumHeight(168)

        self.main_layout = QHBoxLayout()

        self.export_button = QPushButton(QIcon(":export"), "", enabled=False)
        self.export_button.clicked.connect(self.export_results)

        self.clear_button = QPushButton(QIcon(":erase"), "")
        self.clear_button.clicked.connect(self.clear_console)

        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.setAlignment(Qt.AlignTop)
        self.buttons_panel.addWidget(self.export_button)
        self.buttons_panel.addWidget(self.clear_button)

        self.console.itemSelectionChanged.connect(self.enable_buttons)

        self.main_layout.addWidget(self.console)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)

    @Slot()
    def enable_buttons(self) -> None:
        if len(self.console.selectedIndexes()) == 1:
            self.export_button.setEnabled(True)

    def export_results(self) -> None:
        row = self.console.selectedIndexes()[-1].row()
        results = self.get_results_from_console(row)

        filename = QFileDialog.getSaveFileName(self, "Save CSV...", "", "CSV file (*.csv)")[0]

        ResultGenerator(results).to_csv(filename)

    def clear_console(self) -> None:
        self.console.clear()

    def get_results_from_console(self, row: int) -> List[Result]:
        item = self.console.item(row)
        return item.results


class Console(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.itemDoubleClicked.connect(self.open_result_dialog)

    @Slot(QListWidgetItem)
    def open_result_dialog(self, item: CQResultsItem) -> None:
        dialog = CQResultsDialog(item.image_pair, item.results)
        dialog.exec()

    def add_item(self, index: int, image_pair: ImagePair, image_results: List[Result]) -> None:
        self.addItem(CQResultsItem(index, image_pair, image_results))
