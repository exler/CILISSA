from typing import Any

from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMenu,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from cilissa.images import Image
from cilissa_gui.managers import ImageCollectionManager
from cilissa_gui.widgets import CQROIImage


class Workspace(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.list_tab = WorkspaceListTab(self)
        self.details_tab = WorkspaceDetailsTab(self)

        self.addTab(self.list_tab, "List")
        self.addTab(self.details_tab, "Details")


class WorkspaceTab(QWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__()

        self.setMaximumWidth(parent.width())


class WorkspaceListTab(QTreeWidget, WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.collection_manager = ImageCollectionManager()
        self.collection_manager.changed.connect(self.refresh)

        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.itemDoubleClicked.connect(self.open_selected)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)

        self.setFrameStyle(QFrame.NoFrame)

        self.setColumnCount(2)
        self.setColumnWidth(0, 168)
        self.setHeaderLabels(["Reference image", "Compared image"])

        self.setMaximumHeight(168)

    @Slot()
    def refresh(self) -> None:
        self.clear()
        for item in self.collection_manager.get_order():
            item = item[1]
            self.addTopLevelItem(QTreeWidgetItem([item[0].name, item[1].name]))

    def show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        menu.addAction(QAction("Delete", self, statusTip="Delete image pair", triggered=self.delete_selected))
        menu.exec(self.mapToGlobal(pos))

    def delete_selected(self) -> None:
        rows = [index.row() for index in self.selectedIndexes()][::2]
        for idx, row in enumerate(rows):
            decrement = sum([1 for d_row in rows[:idx] if d_row < row])
            self.collection_manager.pop(row - decrement)
        self.collection_manager.changed.emit()

    @Slot()
    def open_selected(self) -> None:
        row = [index.row() for index in self.selectedIndexes()][-1]
        image_pair = self.collection_manager[row]
        self.parent().parent().details_tab.change_base_image(image_pair[0])
        self.parent().parent().details_tab.change_comp_image(image_pair[1])

        self.parent().parent().setCurrentWidget(self.parent().parent().details_tab)


class WorkspaceDetailsTab(WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.init_images()

    def init_images(self) -> None:
        image = QPixmap(":placeholder-128")
        self.image_label_base = CQROIImage()
        self.image_label_base.setAlignment(Qt.AlignCenter)
        self.image_label_base.setPixmap(image)
        self.main_layout.addWidget(self.image_label_base)

        self.main_layout.addSpacing(64)

        image = QPixmap(":placeholder-128")
        self.image_label_comp = CQROIImage()
        self.image_label_comp.setAlignment(Qt.AlignCenter)
        self.image_label_comp.setPixmap(image)
        self.main_layout.addWidget(self.image_label_comp)

    def change_base_image(self, image: Image) -> None:
        self.image_label_base.replace_label_pixmap(image)

    def change_comp_image(self, image: Image) -> None:
        self.image_label_comp.replace_label_pixmap(image)
