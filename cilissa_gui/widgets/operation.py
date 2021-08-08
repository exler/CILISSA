from typing import Type

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QContextMenuEvent, QPixmap
from PySide6.QtWidgets import QLabel, QMenu, QVBoxLayout, QWidget

from cilissa.operations import ImageOperation
from cilissa_gui.managers import QueueManager
from cilissa_gui.widgets import BackgroundColorMixin


class CQOperation(BackgroundColorMixin, QWidget):
    def __init__(self, parent: QWidget, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()

        self.operation = operation
        self.queue_manager = QueueManager()

        self.create_actions()

        self.image_label = QLabel()
        pixmap = QPixmap(":placeholder-64")
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(operation.get_class_name())
        self.text_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.text_label)
        self.setLayout(self.layout)

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
