from PySide6.QtGui import QAction, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from cilissa.images import ImagePair
from cilissa_gui.managers import ImageCollectionManager, OperationsManager
from cilissa_gui.ui.components import (
    ConsoleBox,
    Explorer,
    OperationsBox,
    Properties,
    Workspace,
)


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

        self.panels.addLayout(left_panel)
        self.panels.addLayout(middle_panel)
        self.panels.addLayout(right_panel)
        self.setLayout(self.panels)

        self.panels.setStretch(1, 16)

    def init_components(self) -> None:
        self.explorer = Explorer()
        self.workspace = Workspace()
        self.console = ConsoleBox()
        self.properties = Properties()
        self.operations = OperationsBox()

    def init_left_panel(self) -> QVBoxLayout:
        left_panel = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.explorer)
        scroll_area.setWidgetResizable(True)
        left_panel.addWidget(scroll_area)
        return left_panel

    def init_middle_panel(self) -> QVBoxLayout:
        middle_panel = QVBoxLayout()
        middle_panel.addWidget(self.workspace)
        middle_panel.addWidget(self.console)
        return middle_panel

    def init_right_panel(self) -> QVBoxLayout:
        right_panel = QVBoxLayout()
        properties_box = QGroupBox("Properties")
        properties_box.setLayout(self.properties)
        right_panel.addWidget(properties_box)
        right_panel.addWidget(self.operations)
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
        self.add_pair_action = QAction(
            QIcon(":compare"),
            "Add pair",
            self,
            statusTip="Add image pair to collection",
            triggered=lambda: self.add_selected_pair_to_collection(),
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
        print("Operations manager order: ", self.operations_manager.get_order())
        print("Collections manager order: ", self.collection_manager.get_order())

    def create_connections(self) -> None:
        self.explorer.images_tab.itemSelectionChanged.connect(self.explorer.images_tab.enable_add_pair)

    def run_operations(self) -> None:
        results = self.operations_manager.run(self.collection_manager)
        self.console.console.add_item(str(results))

    def add_selected_pair_to_collection(self) -> None:
        indexes = self.explorer.images_tab.selectedIndexes()
        ref = self.explorer.images_tab.get_item(indexes[0].row(), indexes[0].column()).image
        A = self.explorer.images_tab.get_item(indexes[1].row(), indexes[1].column()).image

        self.collection_manager.push(ImagePair(ref, A))
        self.collection_manager.changed.emit()

    def create_menubar(self) -> None:
        menubar = self.main_window.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_images_action)
        file_menu.addAction(self.open_folder_action)

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
