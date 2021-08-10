from __future__ import annotations

from pathlib import Path
from typing import Type, Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QContextMenuEvent, QImage, QPixmap
from PySide6.QtWidgets import QLabel, QMenu, QVBoxLayout, QWidget

from cilissa.images import Image
from cilissa.operations import ImageOperation
from cilissa_gui.managers import QueueManager


class CQOperation(QWidget):
    def __init__(self, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.operation = operation
        self.queue_manager = QueueManager()

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
        self.add_to_queue_action = QAction(
            "Add To Queue", self, statusTip="Add operation to queue", triggered=self.add_to_queue
        )

    def add_to_queue(self) -> None:
        self.queue_manager.push(self.operation())
        self.queue_manager.changed.emit()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.add_to_queue_action)
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
        self.add_to_collection_action = QAction(
            "Add To Collection", self, statusTip="Add image to collection", triggered=self.add_to_collection
        )

    def add_to_collection(self) -> None:
        print("Added")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.add_to_collection_action)
        menu.exec(event.globalPos())
