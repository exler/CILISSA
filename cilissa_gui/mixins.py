from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette


class BackgroundColorMixin:
    """
    Mixin used to see the boundaries of QWidget. Useful while debugging.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.red)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
