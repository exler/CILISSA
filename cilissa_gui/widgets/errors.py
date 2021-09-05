from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox


class CQErrorDialog(QMessageBox):
    def __init__(self, msg: str, title: Optional[str] = None) -> None:
        super().__init__()

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(title or "An error occurred")

        self.setTextFormat(Qt.PlainText)
        self.setText(msg)
        self.setStandardButtons(QMessageBox.Ok)
