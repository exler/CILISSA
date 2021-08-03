# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class Application(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CILISSA")
        self.resize(800, 600)
        self.centralWidget = QLabel("hello, world")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    window.show()
    sys.exit(app.exec())
