from __future__ import annotations

from pathlib import Path
from typing import Type, Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QContextMenuEvent, QImage, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from cilissa.classes import AnalysisResult
from cilissa.images import Image
from cilissa.operations import ImageOperation
from cilissa_gui.managers import OperationsManager


class CQOperation(QWidget):
    def __init__(self, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.operation = operation
        self.operations_manager = OperationsManager()

        self.create_actions()

        self.image_label = QLabel()
        pixmap = QPixmap(":placeholder-64")
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(operation.get_class_name())
        self.text_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.text_label)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(96)

    def create_actions(self) -> None:
        self.add_to_operations_action = QAction(
            "Add To Operations List", self, statusTip="Add operation to list", triggered=self.add_to_operations_list
        )

    def add_to_operations_list(self) -> None:
        self.operations_manager.push(self.operation())
        self.operations_manager.changed.emit()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.add_to_operations_action)
        menu.exec(event.globalPos())


class CQImage(QWidget):
    def __init__(self, image: Image) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image = image

        self.create_actions()

        self.image_label = QLabel()
        thumbnail = QImage(self.image.get_thumbnail(64, 64), 64, 64, 64 * self.image.channels_num, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(thumbnail)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(96)

    @staticmethod
    def load(image_path: Union[Path, str]) -> CQImage:
        im = Image(image_path)
        cqimage = CQImage(im)
        return cqimage

    def create_actions(self) -> None:
        pass

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.exec(event.globalPos())


class CQResult(QListWidgetItem):
    def __init__(self, result: AnalysisResult) -> None:
        super().__init__(result.pretty())

        self.result = result


class CQResultDialog(QMessageBox):
    def __init__(self, result: AnalysisResult) -> None:
        super().__init__()

        self.result = result

        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle("Analysis result")

        self.setTextFormat(Qt.RichText)
        self.setText(self.format_result())
        self.setStandardButtons(QMessageBox.Close)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 16, 24, 8)

    def format_result(self) -> None:
        return """
        <strong>Metric name:</strong> {}<br>
        <strong>Result:</strong> {}<br>
        <strong>Properties:</strong>
        <ul>{}</ul>
        <br>
        """.format(
            self.result.name,
            self.result.value,
            "".join(["<li>{}: {}</li>".format(k, v) for k, v in self.result.parameters.items()]),
        )
