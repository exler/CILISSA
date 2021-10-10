import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

import cilissa_gui.resources  # noqa
from cilissa_gui.interface import Interface


class Application(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setWindowTitle("CILISSA")
        self.setWindowIcon(QIcon(":cilissa-icon"))
        self.resize(1366, 768)

        self.interface = Interface(self)
        self.setCentralWidget(self.interface)


def main() -> None:
    app = QApplication([])
    window = Application()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
