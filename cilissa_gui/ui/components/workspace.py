from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from cilissa.images import ImagePair
from cilissa_gui.managers import ImageCollectionManager
from cilissa_gui.widgets import CQImage, CQROIDialog


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
        self.setHeaderLabels(["Reference image", "Input image"])

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
        self.parent().parent().details_tab.change_images(image_pair)
        self.parent().parent().setCurrentWidget(self.parent().parent().details_tab)


class WorkspaceDetailsTab(WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.image_pair = None

        self.init_images()
        self.init_buttons()

        self.setLayout(self.main_layout)

    def select_roi(self) -> None:
        dialog = CQROIDialog(self.image_pair)
        dialog.exec()
        self.refresh()

    def init_images(self) -> None:
        self.images_panel = QVBoxLayout()
        self.images_panel.setAlignment(Qt.AlignCenter)

        self.ref_image_label = QLabel("Reference image")
        self.ref_image_label.setAlignment(Qt.AlignCenter)
        self.ref_image = CQImage.load("cilissa_gui/resources/placeholder-128.png", height=128)
        self.images_panel.addWidget(self.ref_image_label)
        self.images_panel.addWidget(self.ref_image)

        self.images_panel.addSpacing(32)

        self.input_image_label = QLabel("Input image")
        self.input_image_label.setAlignment(Qt.AlignCenter)
        self.input_image = CQImage.load("cilissa_gui/resources/placeholder-128.png", height=128)
        self.images_panel.addWidget(self.input_image_label)
        self.images_panel.addWidget(self.input_image)

        self.main_layout.addLayout(self.images_panel)

    def init_buttons(self) -> None:
        self.buttons_panel = QHBoxLayout()

        self.roi_button = QPushButton("Select ROI", disabled=True)
        self.roi_button.clicked.connect(self.select_roi)
        self.buttons_panel.addWidget(self.roi_button)

        self.main_layout.addLayout(self.buttons_panel)

    def change_images(self, image_pair: ImagePair) -> None:
        self.image_pair = image_pair
        self.refresh()

        if self.image_pair:
            self.roi_button.setDisabled(False)

    def refresh(self) -> None:
        self.ref_image.set_image(self.image_pair.get_full_image(0), roi=self.image_pair.roi)
        self.input_image.set_image(self.image_pair.get_full_image(1), roi=self.image_pair.roi)
