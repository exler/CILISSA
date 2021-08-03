from PySide6.QtGui import QAction, QDesktopServices, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

import cilissa_gui.resources  # noqa


class Application(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setWindowTitle("CILISSA")
        self.resize(800, 600)

        self._create_actions()
        self._create_menubar()
        self._create_toolbar()
        self._create_statusbar()

    def _create_actions(self) -> None:
        self.open_images_action = QAction(QIcon(":add-file"), "&Open Images...", self)
        self.open_folder_action = QAction(QIcon(":add-folder"), "Open Folder...", self)

        self.documentation_action = QAction("Documentation", self)
        self.documentation_action.triggered.connect(
            lambda: QDesktopServices.openUrl("https://github.com/exler/cilissa")
        )

    def _create_menubar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_images_action)
        file_menu.addAction(self.open_folder_action)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.documentation_action)

    def _create_toolbar(self) -> None:
        self.toolbar = self.addToolBar("Main toolbar")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.open_images_action)
        self.toolbar.addAction(self.open_folder_action)

    def _create_statusbar(self) -> None:
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("CILISSA is ready.")


if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    window.show()
    exit(app.exec())
