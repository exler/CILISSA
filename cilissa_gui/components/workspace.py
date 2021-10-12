from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QStackedWidget,
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

        self.set_details_tab_enabled(False)  # Disable Details on start

    def set_details_tab_enabled(self, enabled: bool) -> None:
        self.setTabEnabled(1, enabled)


class WorkspaceTabMixin:
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.tab_widget = parent


class WorkspaceListTab(WorkspaceTabMixin, QStackedWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.help = WorkspaceHelp()
        self.list = WorkspaceList()

        self.addWidget(self.help)
        self.addWidget(self.list)


class WorkspaceHelp(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.help_icon = QLabel()
        self.help_icon.setPixmap(QPixmap(":add"))
        self.help_icon.setAlignment(Qt.AlignCenter)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)
        self.help_icon.setGraphicsEffect(self.opacity_effect)

        self.help_text = QLabel("Select an image pair and press 'Add pair' in the toolbar to add it to the collection")
        self.help_text.setStyleSheet("QLabel { color: darkgray; }")
        self.help_text.setWordWrap(False)
        self.help_text.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.help_icon)
        self.main_layout.addWidget(self.help_text)
        self.setLayout(self.main_layout)


class WorkspaceList(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.tree = QTreeWidget()
        self.tree.setStyleSheet("QTreeWidget { border: none; border-right: 1px solid silver !important; }")

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.info_button = QPushButton(QIcon(":info"), "", enabled=False, toolTip="Show details about image pair")
        self.info_button.clicked.connect(self.open_selected)

        self.delete_button = QPushButton(QIcon(":delete"), "", enabled=False, toolTip="Delete selected image pairs")
        self.delete_button.clicked.connect(self.delete_selected)

        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.setContentsMargins(0, 4, 6, 0)
        self.buttons_panel.setAlignment(Qt.AlignTop)
        self.buttons_panel.addWidget(self.info_button)
        self.buttons_panel.addWidget(self.delete_button)

        self.collection_manager = ImageCollectionManager()
        self.collection_manager.changed.connect(self.refresh)

        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree.setFocusPolicy(Qt.NoFocus)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

        self.tree.itemDoubleClicked.connect(self.open_selected)

        self.tree.setColumnCount(3)
        self.tree.setColumnWidth(0, 32)
        self.tree.setColumnWidth(1, 272)
        self.tree.setHeaderLabels(["#", "Reference image", "Input image"])

        self.main_layout.addWidget(self.tree)
        self.main_layout.addLayout(self.buttons_panel)

        self.tree.itemSelectionChanged.connect(self.enable_buttons)

        self.setLayout(self.main_layout)

    @Slot()
    def refresh(self) -> None:
        self.tree.clear()
        if self.collection_manager.is_empty:
            self.parent().setCurrentWidget(self.parent().help)
        else:
            self.parent().setCurrentWidget(self)

        for item in self.collection_manager.get_order():
            index = item[0]
            item = item[1]
            self.tree.addTopLevelItem(QTreeWidgetItem([str(index + 1), item[0].name, item[1].name]))

    @Slot()
    def enable_buttons(self) -> None:
        if len(self.tree.selectedIndexes()) > 0:
            self.info_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.info_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    @Slot()
    def delete_selected(self) -> None:
        rows = [index.row() for index in self.tree.selectedIndexes()][::3]
        for idx, row in enumerate(rows):
            decrement = sum([1 for d_row in rows[:idx] if d_row < row])
            self.collection_manager.pop(row - decrement)
        self.collection_manager.changed.emit()

    @Slot()
    def open_selected(self) -> None:
        row = [index.row() for index in self.tree.selectedIndexes()][-1]
        image_pair = self.collection_manager[row]
        self.parent().tab_widget.details_tab.change_images(image_pair)
        self.parent().tab_widget.setCurrentWidget(self.parent().tab_widget.details_tab)

    def show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        menu.addAction(QAction("Delete", self, statusTip="Delete image pair", triggered=self.delete_selected))
        menu.exec(self.mapToGlobal(pos))


class WorkspaceDetailsTab(WorkspaceTabMixin, QWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.image_pair = None

        self.init_images()
        self.init_details()
        self.init_buttons()

        self.main_layout.setStretchFactor(self.images_panel, 2)
        self.setLayout(self.main_layout)

    def init_images(self) -> None:
        self.images_panel = QHBoxLayout()
        self.images_panel.setAlignment(Qt.AlignCenter)

        self.ref_image_layout = QVBoxLayout()
        self.ref_image_label = QLabel("Reference image")
        self.ref_image_label.setAlignment(Qt.AlignCenter)
        self.ref_image = CQImage.placeholder(height=164)
        self.ref_image_layout.addWidget(self.ref_image_label)
        self.ref_image_layout.addWidget(self.ref_image)
        self.images_panel.addLayout(self.ref_image_layout)

        self.images_panel.addSpacing(32)

        self.input_image_layout = QVBoxLayout()
        self.input_image_label = QLabel("Input image")
        self.input_image_label.setAlignment(Qt.AlignCenter)
        self.input_image = CQImage.placeholder(height=164)
        self.input_image_layout.addWidget(self.input_image_label)
        self.input_image_layout.addWidget(self.input_image)
        self.images_panel.addLayout(self.input_image_layout)

        self.main_layout.addLayout(self.images_panel)

    def init_details(self) -> None:
        self.details_panel = QVBoxLayout()
        self.details_panel.setAlignment(Qt.AlignBottom)

        self.shape_info = QLabel("")
        self.roi_info = QLabel("")
        self.details_panel.addWidget(self.shape_info)
        self.details_panel.addWidget(self.roi_info)

        self.main_layout.addLayout(self.details_panel)

    def init_buttons(self) -> None:
        self.buttons_panel = QHBoxLayout()

        self.swap_images_button = QPushButton("Swap images")
        self.swap_images_button.clicked.connect(self.swap_images)
        self.select_roi_button = QPushButton("Select ROI")
        self.select_roi_button.clicked.connect(self.select_roi)
        self.clear_roi_button = QPushButton("Clear ROI")
        self.clear_roi_button.clicked.connect(self.clear_roi)
        self.buttons_panel.addWidget(self.swap_images_button)
        self.buttons_panel.addWidget(self.select_roi_button)
        self.buttons_panel.addWidget(self.clear_roi_button)

        self.main_layout.addLayout(self.buttons_panel)

    @Slot()
    def swap_images(self) -> None:
        if self.image_pair:
            self.image_pair.swap()
            self.refresh()

    def change_images(self, image_pair: ImagePair) -> None:
        self.image_pair = image_pair
        self.refresh()

    @Slot()
    def select_roi(self) -> None:
        dialog = CQROIDialog(self.image_pair)
        dialog.exec()
        self.refresh()

    @Slot()
    def clear_roi(self) -> None:
        if self.image_pair:
            self.image_pair.clear_roi()
            self.refresh()

    def refresh(self) -> None:
        if self.image_pair:
            self.tab_widget.set_details_tab_enabled(True)
            self.ref_image.set_image(self.image_pair.im1, roi=self.image_pair.roi)
            self.input_image.set_image(self.image_pair.im2, roi=self.image_pair.roi)

            self.shape_info.setText(
                f"<b>Image pair shape:</b> {self.image_pair.im1.width}x{self.image_pair.im1.height}"
            )
            roi = self.image_pair.roi
            if roi:
                msg = f"<b>ROI:</b> start point - {roi.start_point}, end point - {roi.end_point}"
                if not self.image_pair.use_roi:
                    msg += " <span style='color: red;'>(ROI ignored)</span>"
                self.roi_info.setText(msg)
            else:
                self.roi_info.setText("<b>ROI:</b> not selected")
