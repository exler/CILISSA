from PySide6.QtWidgets import QApplication, QMainWindow

import cilissa_gui.resources  # noqa
from cilissa_gui.ui.interface import Interface


class Application(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setWindowTitle("CILISSA")
        self.resize(1024, 768)

        self.interface = Interface(self)
        self.setCentralWidget(self.interface)


if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    window.show()
    exit(app.exec())
