from PySide6.QtGui import QAction, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from cilissa_gui.ui.components import ConsoleBox, Explorer, Properties, Queue, Workspace


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
        - Queue
    """

    def __init__(self, window: QMainWindow) -> None:
        super().__init__()

        self.window = window

        self.init_components()
        self.create_actions()
        self.create_menubar()
        self.create_toolbar()
        self.create_statusbar()

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
        self.explorer = Explorer(self)
        self.workspace = Workspace(self)
        self.console = ConsoleBox(self)
        self.properties = Properties(self)
        self.queue = Queue(self)

    def init_left_panel(self) -> QVBoxLayout:
        left_panel = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.explorer)
        scroll_area.setWidgetResizable(True)
        left_panel.addWidget(scroll_area)
        return left_panel

    def init_middle_panel(self) -> QVBoxLayout:
        middle_panel = QVBoxLayout()
        workspace_box = QGroupBox("Workspace")
        workspace_box.setLayout(self.workspace)
        middle_panel.addWidget(workspace_box)
        middle_panel.addWidget(self.console)
        return middle_panel

    def init_right_panel(self) -> QVBoxLayout:
        right_panel = QVBoxLayout()
        properties_box = QGroupBox("Properties")
        properties_box.setLayout(self.properties)
        right_panel.addWidget(properties_box)
        right_panel.addWidget(self.queue)
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
        self.documentation_action = QAction(
            "Documentation",
            self,
            statusTip="Open documentation website",
            triggered=lambda: QDesktopServices.openUrl("https://github.com/exler/cilissa"),
        )

    def create_menubar(self) -> None:
        menubar = self.window.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_images_action)
        file_menu.addAction(self.open_folder_action)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.documentation_action)

    def create_toolbar(self) -> None:
        self.toolbar = self.window.addToolBar("Main toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.open_images_action)
        self.toolbar.addAction(self.open_folder_action)

    def create_statusbar(self) -> None:
        self.statusbar = self.window.statusBar()
        self.statusbar.showMessage("CILISSA is ready.")
