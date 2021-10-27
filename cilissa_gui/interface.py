from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from cilissa.exceptions import ShapesNotEqual
from cilissa.images import ImagePair
from cilissa_gui.components import (
    ConsoleBox,
    Explorer,
    OperationsBox,
    PropertiesBox,
    Workspace,
)
from cilissa_gui.managers import ImageCollectionManager, OperationsManager
from cilissa_gui.widgets import CQErrorDialog


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

        self.panels.setStretchFactor(left_panel, 1)
        self.panels.setStretchFactor(middle_panel, 2)
        self.panels.setStretchFactor(right_panel, 1)

    def init_components(self) -> None:
        self.explorer = Explorer()
        self.workspace = Workspace()
        self.console_box = ConsoleBox()
        self.properties_box = PropertiesBox()
        self.operations_box = OperationsBox()

    def init_left_panel(self) -> QVBoxLayout:
        left_panel = QWidget()
        left_panel.setMinimumWidth(288)

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
        right_panel.setMinimumWidth(288)

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
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_O),
            triggered=self.explorer.open_image_dialog,
        )
        self.open_folder_action = QAction(
            QIcon(":add-folder"),
            "Open Folder...",
            self,
            statusTip="Open an image folder",
            shortcut=QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_O),
            triggered=self.explorer.open_image_folder_dialog,
        )
        self.save_operations_action = QAction(
            "Save Operations List...",
            self,
            statusTip="Save current operations list",
            triggered=self.operations_box.save_operations,
        )
        self.load_operations_action = QAction(
            "Load Operations List...",
            self,
            statusTip="Open and restore operations list",
            triggered=self.operations_box.load_operations,
        )
        self.remove_images_action = QAction(
            QIcon(":trash"),
            "Remove images",
            self,
            statusTip="Remove selected images from explorer",
            triggered=self.explorer.images_tab.remove_selected,
            enabled=False,
        )
        self.exit_application_action = QAction(
            QIcon(":delete"),
            "Exit",
            self,
            statusTip="Exit the application",
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_Q),
            triggered=self.main_window.close,
        )
        self.ignore_roi_action = QAction(
            "Ignore ROI",
            self,
            statusTip="Ignore region of interests in operations",
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
            QIcon(":document"),
            "Documentation",
            self,
            statusTip="Open documentation website",
            shortcut=QKeySequence(Qt.Key_F1),
            triggered=lambda: QDesktopServices.openUrl("https://cilissa.readthedocs.io/"),
        )

    def create_connections(self) -> None:
        self.explorer.images_tab.itemSelectionChanged.connect(self.enable_actions)
        self.explorer.metrics_tab.itemClicked.connect(self.properties_box.properties.open_selection)
        self.explorer.transformations_tab.itemClicked.connect(self.properties_box.properties.open_selection)
        self.operations_box.operations.itemClicked.connect(self.properties_box.properties.open_selection)
        self.console_box.console.itemClicked.connect(
            lambda: self.show_message_in_statusbar("Double-click the result to see detailed information")
        )

    @Slot()
    def enable_actions(self) -> None:
        images_selected = len(self.explorer.images_tab.selectedIndexes())

        if images_selected > 0:
            self.remove_images_action.setEnabled(True)
            if images_selected == 2:
                self.add_pair_action.setEnabled(True)
            else:
                self.add_pair_action.setEnabled(False)
        else:
            self.remove_images_action.setEnabled(False)
            self.add_pair_action.setEnabled(False)

    @Slot(str)
    def show_message_in_statusbar(self, message: str, timeout: int = 0) -> None:
        self.statusbar.showMessage(message, timeout)

    def run_operations(self) -> None:
        if self.operations_manager.is_empty:
            self.show_message_in_statusbar("You have not chosen any operations!", 3000)
        elif self.collection_manager.is_empty:
            self.show_message_in_statusbar("You have not chosen any images!", 3000)
        else:
            self.show_message_in_statusbar("CILISSA is running...")
            results = self.operations_manager.run_all(self.collection_manager)
            for index, image_results in enumerate(results):
                image_pair = self.collection_manager[index]
                self.console_box.console.add_item(index, image_pair, image_results)
            self.show_message_in_statusbar("All operations finished")

    def add_selected_pair_to_collection(self) -> None:
        items = self.explorer.images_tab.selectedItems()
        ref, A = items[0].image, items[1].image

        try:
            image_pair = ImagePair(ref, A)
            self.collection_manager.push(image_pair)
            self.collection_manager.changed.emit()
        except ShapesNotEqual:
            err_dialog = CQErrorDialog("Images must be of the same proportions to analyze!")
            err_dialog.exec()

    def set_use_roi_on_collection(self) -> None:
        use_roi = not self.ignore_roi_action.isChecked()
        self.collection_manager.set_use_roi(use_roi)
        self.workspace.details_tab.refresh()

    def create_menubar(self) -> None:
        menubar = self.main_window.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_images_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_operations_action)
        file_menu.addAction(self.load_operations_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_application_action)

        configuration_menu = menubar.addMenu("&Configuration")
        configuration_menu.addAction(self.ignore_roi_action)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.documentation_action)
        # help_menu.addSeparator()

    def create_toolbar(self) -> None:
        self.toolbar = self.main_window.addToolBar("Main toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.open_images_action)
        self.toolbar.addAction(self.open_folder_action)
        self.toolbar.addAction(self.remove_images_action)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.add_pair_action)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.run_action)

    def create_statusbar(self) -> None:
        self.statusbar = self.main_window.statusBar()
        self.statusbar.showMessage("CILISSA is ready.")
