from typing import Type

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QContextMenuEvent, QPixmap
from PySide6.QtWidgets import QLabel, QMenu, QVBoxLayout, QWidget

from cilissa.operations import ImageOperation
from cilissa_gui.helpers import get_operation_icon_name
from cilissa_gui.managers import OperationsManager


class CQOperation(QWidget):
    def __init__(self, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.operation = operation
        self.operations_manager = OperationsManager()

        self.create_actions()

        self.image_label = QLabel()
        pixmap_name = get_operation_icon_name(self.operation)
        pixmap = QPixmap(pixmap_name)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(operation.get_class_name())
        self.text_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.text_label)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(96)

    def create_actions(self) -> None:
        self.add_with_default_params_action = QAction(
            "Add With Default Parameters",
            self,
            statusTip="Add operation to list",
            triggered=self.add_with_default_params,
        )

    def add_with_default_params(self) -> None:
        self.operations_manager.push(self.operation())
        self.operations_manager.changed.emit()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.add_with_default_params_action)
        menu.exec(event.globalPos())
