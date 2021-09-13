from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE, PSNR
from cilissa.roi import ROI
from cilissa_gui.components import (
    ConsoleBox,
    Explorer,
    OperationsBox,
    PropertiesBox,
    Workspace,
)
from cilissa_gui.managers import ImageCollectionManager, OperationsManager
from cilissa_gui.widgets.errors import CQErrorDialog


class Interface(QWidget):
    """
    Interface is split into three vertical panels:

    Left panel:
        - Explorer

    Middle panel:
        - Workspace
        - Console

    Right panel:
        - Properties
        - Operations
    """

    def __init__(self, window: QMainWindow) -> None:
        super().__init__()

        self.main_window = window

        self.operations_manager = OperationsManager()
        self.collection_manager = ImageCollectionManager()

        self.init_components()
        self.create_actions()
        self.create_menubar()
        self.create_toolbar()
        self.create_statusbar()

        self.create_connections()

        self.panels = QHBoxLayout()
        left_panel = self.init_left_panel()
        middle_panel = self.init_middle_panel()
        right_panel = self.init_right_panel()

        self.panels.addWidget(left_panel)
        self.panels.addWidget(middle_panel)
        self.panels.addWidget(right_panel)
        self.setLayout(self.panels)

    def init_components(self) -> None:
        self.explorer = Explorer()
        self.workspace = Workspace()
        self.console_box = ConsoleBox()
        self.properties_box = PropertiesBox()
        self.operations_box = OperationsBox()

    def init_left_panel(self) -> QVBoxLayout:
        left_panel = QWidget()
        left_panel.setFixedWidth(324)

        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.explorer)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        left_panel.setLayout(layout)
        return left_panel

    def init_middle_panel(self) -> QVBoxLayout:
        middle_panel = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.workspace)
        layout.addWidget(self.console_box)

        middle_panel.setLayout(layout)
        return middle_panel

    def init_right_panel(self) -> QVBoxLayout:
        right_panel = QWidget()
        right_panel.setFixedWidth(256)

        layout = QVBoxLayout()
        layout.addWidget(self.properties_box)
        layout.addWidget(self.operations_box)

        right_panel.setLayout(layout)
        return right_panel

    def create_actions(self) -> None:
        self.open_images_action = QAction(
            QIcon(":add-file"),
            "Open Images...",
            self,
            statusTip="Open an image file",
            shortcut=QKeySequence.Open,
            triggered=self.explorer.open_image_dialog,
        )
        self.open_folder_action = QAction(
            QIcon(":add-folder"),
            "Open Folder...",
            self,
            statusTip="Open an image folder",
            triggered=self.explorer.open_image_folder_dialog,
        )
        self.skip_roi_action = QAction(
            "Skip ROI",
            self,
            statusTip="Skip region of interests in operations",
            triggered=self.set_use_roi_on_collection,
            checkable=True,
        )
        self.add_pair_action = QAction(
            QIcon(":compare"),
            "Add pair",
            self,
            statusTip="Add image pair to collection",
            triggered=self.add_selected_pair_to_collection,
            enabled=False,
        )
        self.run_action = QAction(
            QIcon(":play"),
            "Run",
            self,
            statusTip="Run operations from list on image collection",
            triggered=self.run_operations,
        )
        self.documentation_action = QAction(
            "Documentation",
            self,
            statusTip="Open documentation website",
            triggered=lambda: QDesktopServices.openUrl("https://github.com/exler/cilissa"),
        )
        self.debug_action = QAction(
            "Debug", self, statusTip="Debug only action for testing purposes", triggered=self.debug
        )

    def debug(self) -> None:
        im1 = Image(Path("tests", "data", "ref_images", "monarch.bmp"))
        im2 = Image(Path("tests", "data", "transformations", "monarch_linear.bmp"))
        im_pair = ImagePair(im1, im2)
        im_pair.set_roi(ROI(0, 0, 384, 512))
        self.collection_manager.push(im_pair)
        self.workspace.list_tab.refresh()

        mse = MSE()
        psnr = PSNR()
        self.operations_manager.push(mse)
        self.operations_manager.push(psnr)
        self.operations_box.operations.refresh()

    def create_connections(self) -> None:
        self.explorer.images_tab.itemSelectionChanged.connect(self.explorer.images_tab.enable_add_pair)
        self.explorer.explorerItemSelected.connect(self.properties_box.properties.open_selection)
        self.operations_box.operations.itemClicked.connect(self.properties_box.properties.open_selection)
        self.console_box.console.itemClicked.connect(
            lambda: self.show_message_in_statusbar("Double-click the result in console to see detailed information")
        )

    @Slot(str)
    def show_message_in_statusbar(self, message: str) -> None:
        self.statusbar.showMessage(message, 3000)

    def run_operations(self) -> None:
        if self.operations_manager.is_empty:
            self.statusbar.showMessage("You have not chosen any operations!", 3000)
        elif self.collection_manager.is_empty:
            self.statusbar.showMessage("You have not chosen any images!", 3000)
        else:
            self.statusbar.showMessage("CILISSA is running...")
            results = self.operations_manager.run_all(self.collection_manager)
            for image_results in results:
                for operation_result in image_results:
                    self.console_box.console.add_item(operation_result)

    def add_selected_pair_to_collection(self) -> None:
        indexes = self.explorer.images_tab.selectedIndexes()
        ref = self.explorer.images_tab.get_item(indexes[0].row(), indexes[0].column()).image
        A = self.explorer.images_tab.get_item(indexes[1].row(), indexes[1].column()).image

        try:
            image_pair = ImagePair(ref, A)
            self.collection_manager.push(image_pair)
            self.collection_manager.changed.emit()
        except ShapesNotEqual:
            err_dialog = CQErrorDialog("Images must be of the same proportions to analyze!")
            err_dialog.exec()

    def set_use_roi_on_collection(self) -> None:
        use_roi = not self.skip_roi_action.isChecked()
        self.collection_manager.set_use_roi(use_roi)

    def create_menubar(self) -> None:
        menubar = self.main_window.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_images_action)
        file_menu.addAction(self.open_folder_action)

        configuration_menu = menubar.addMenu("&Configuration")
        configuration_menu.addAction(self.skip_roi_action)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.documentation_action)
        help_menu.addAction(self.debug_action)

    def create_toolbar(self) -> None:
        self.toolbar = self.main_window.addToolBar("Main toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.open_images_action)
        self.toolbar.addAction(self.open_folder_action)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.add_pair_action)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.run_action)

    def create_statusbar(self) -> None:
        self.statusbar = self.main_window.statusBar()
        self.statusbar.showMessage("CILISSA is ready.")
