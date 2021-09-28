from typing import Type

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem

from cilissa.operations import ImageOperation
from cilissa_gui.helpers import get_operation_icon_name
from cilissa_gui.managers import OperationsManager


class CQOperationItem(QListWidgetItem):
    def __init__(self, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.operation = operation
        self.operations_manager = OperationsManager()

        pixmap_name = get_operation_icon_name(self.operation)
        self.setIcon(QIcon(QPixmap(pixmap_name)))
        self.setText(operation.get_display_name())
