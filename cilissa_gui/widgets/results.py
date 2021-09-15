from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox

from cilissa.results import Result, ResultGenerator


class CQResultsItem(QListWidgetItem):
    def __init__(self, index: int, results: List[Result]) -> None:
        super().__init__(f"Run #{index} completed. Double-click here for details.")

        self.results = results


class CQResultsDialog(QMessageBox):
    def __init__(self, results: Result) -> None:
        super().__init__()

        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle("Results Window")

        html = ResultGenerator.to_html(results)
        self.setTextFormat(Qt.RichText)
        self.setText(html)
        self.setStandardButtons(QMessageBox.Close)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 16, 24, 8)
