from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QContextMenuEvent, QPainter, QPen
from PySide6.QtWidgets import QLabel, QMenu, QVBoxLayout, QWidget

from cilissa.images import Image
from cilissa.roi import ROI
from cilissa_gui.helpers import get_pixmap_from_image


class CQImage(QWidget):
    def __init__(
        self, image: Image, roi: Optional[ROI] = None, width: Optional[int] = None, height: Optional[int] = None
    ) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.width = width
        self.height = height
        self.set_image(image, roi=roi)

        self.main_layout.addWidget(self.image_label)
        self.setLayout(self.main_layout)

    def set_image(self, image: Image, roi: Optional[ROI] = None) -> None:
        self.image = image

        pixmap = get_pixmap_from_image(self.image, width=self.width, height=self.height)

        if roi:
            scale_factor = self.image.get_scale_factor(width=self.width, height=self.height)
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.red, 2, Qt.DashDotDotLine))
            painter.drawRect(
                roi.x0 * scale_factor,
                roi.y0 * scale_factor,
                (roi.x1 - roi.x0) * scale_factor,
                (roi.y1 - roi.y0) * scale_factor,
            )
            painter.end()

        self.setToolTip(self.image.name)
        self.image_label.setPixmap(pixmap)
        self.setMaximumHeight(pixmap.height() + 32)

    @staticmethod
    def load(image_path: Union[Path, str], **kwargs: Any) -> CQImage:
        im = Image(image_path)
        cqimage = CQImage(im, **kwargs)
        return cqimage

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.exec(event.globalPos())
