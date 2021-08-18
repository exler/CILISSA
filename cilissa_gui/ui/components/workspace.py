from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from cilissa_gui.managers import ImageCollectionManager


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
            self.addTopLevelItem(QTreeWidgetItem([item.ref.name, item.A.name]))

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


class WorkspaceDetailsTab(WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.change_base_image()
        self.change_comp_image()

    def change_base_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(image)
        self.main_layout.addWidget(image_label)

    def change_comp_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(image)
        self.main_layout.addWidget(image_label)
