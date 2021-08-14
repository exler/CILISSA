from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
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
