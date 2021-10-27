import json

from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
)

from cilissa.operations import ImageOperation
from cilissa.parsers import parse_operations_from_json
from cilissa_gui.helpers import get_operation_icon_name
from cilissa_gui.managers import OperationsManager


class OperationsBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Operations")

        self.setMaximumHeight(168)

        self.operations = Operations()

        self.main_layout = QHBoxLayout()

        self.clear_button = QPushButton(QIcon(":erase"), "", toolTip="Clear all operations")
        self.clear_button.clicked.connect(self.clear_operations)

        self.delete_button = QPushButton(QIcon(":delete"), "", enabled=False, toolTip="Delete selected operations")
        self.delete_button.clicked.connect(self.delete_operations)

        self.move_up_button = QPushButton(
            QIcon(":double-up"), "", enabled=False, toolTip="Move selected operations up in queue"
        )
        self.move_up_button.clicked.connect(self.move_operation_up)

        self.move_down_button = QPushButton(
            QIcon(":double-down"), "", enabled=False, toolTip="Move selected operations down in queue"
        )
        self.move_down_button.clicked.connect(self.move_operation_down)

        self.operations.setFocusPolicy(Qt.NoFocus)
        self.operations.setContextMenuPolicy(Qt.CustomContextMenu)
        self.operations.customContextMenuRequested.connect(self.show_context_menu)

        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.setAlignment(Qt.AlignTop)
        self.buttons_panel.addWidget(self.move_up_button)
        self.buttons_panel.addWidget(self.move_down_button)
        self.buttons_panel.addWidget(self.delete_button)
        self.buttons_panel.addWidget(self.clear_button)

        self.main_layout.addWidget(self.operations)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)

        self.operations.itemSelectionChanged.connect(self.enable_buttons)

    @Slot()
    def clear_operations(self) -> None:
        self.operations.operations_manager.clear()
        self.operations.refresh()

    @Slot()
    def delete_operations(self) -> None:
        rows = [index.row() for index in self.operations.selectedIndexes()]
        for idx, row in enumerate(rows):
            decrement = sum([1 for d_row in rows[:idx] if d_row < row])
            self.operations.operations_manager.pop(row - decrement)
        self.operations.refresh()

    @Slot()
    def enable_buttons(self) -> None:
        if len(self.operations.selectedIndexes()) > 0:
            self.move_up_button.setEnabled(True)
            self.move_down_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.move_up_button.setEnabled(False)
            self.move_down_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    @Slot()
    def move_operation_up(self) -> None:
        self.operations.change_selected_order(-1)

    @Slot()
    def move_operation_down(self) -> None:
        self.operations.change_selected_order(1)

    @Slot()
    def load_operations(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Load operations list", "", "JSON files (*.json)")
        if file_name:
            f = open(file_name)
            instances = parse_operations_from_json(f)
            f.close()

            self.operations.operations_manager.clear()
            for instance in instances:
                self.operations.operations_manager.push(instance)
            self.operations.refresh()

    @Slot()
    def save_operations(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(self, "Save operations list", "", "JSON file (*.json)")

        if file_name:
            f = open(file_name, "w")

            data = []
            for operation in self.operations.operations_manager:
                data.append({"name": operation.get_class_name(), "parameters": operation.get_parameters_dict()})

            json.dump(data, f)
            f.close()

    def show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        if self.operations.selectedIndexes():
            menu.addAction(QAction("Delete", self, statusTip="Delete image pair", triggered=self.delete_operations))
        menu.exec(self.mapToGlobal(pos))


class Operations(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.operations_manager = OperationsManager()
        self.operations_manager.changed.connect(self.refresh)

        self.setSelectionMode(QListWidget.ExtendedSelection)

    @Slot()
    def refresh(self) -> None:
        self.clear()
        for item in self.operations_manager.get_order():
            item = self.create_item_from_operation(item[1])
            self.addItem(item)

    def change_selected_order(self, move: int) -> None:
        rows = [index.row() for index in self.selectedIndexes()]
        for row in rows:
            if not (row == 0 and move < 0) and not (row == self.count() - 1 and move > 0):
                self.operations_manager.change_order(row, row + move)
        self.refresh()

    def create_item_from_operation(self, operation: ImageOperation) -> QListWidgetItem:
        icon_name = get_operation_icon_name(operation)
        icon = QIcon(icon_name)
        item = QListWidgetItem(icon, operation.get_display_name(), self)
        return item
