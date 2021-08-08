from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette


class BackgroundColorMixin:
    """
    Mixin used to see the boundaries of QWidget. Useful while debugging.
    """

    def __init__(self) -> None:
        super().__init__()

        palette = self.palette()  # type: ignore
        palette.setColor(QPalette.Window, Qt.red)  # type: ignore
        self.setAutoFillBackground(True)  # type: ignore
        self.setPalette(palette)  # type: ignore
