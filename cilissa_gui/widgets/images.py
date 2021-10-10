from __future__ import annotations

from typing import Any, Optional

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPainter, QPen
from PySide6.QtWidgets import QLabel, QListWidgetItem, QVBoxLayout, QWidget

from cilissa.images import Image
from cilissa.roi import ROI
from cilissa_gui.helpers import get_pixmap_from_image


class CQImageItem(QListWidgetItem):
    def __init__(self, image: Image, width: Optional[int] = None, height: Optional[int] = None) -> None:
        super().__init__()

        self.image = image

        pixmap = get_pixmap_from_image(self.image, width=width, height=height)
        self.setIcon(QIcon(pixmap))
        self.setToolTip(self.image.name)


class CQImage(QWidget):
    def __init__(
        self, image: Image, roi: Optional[ROI] = None, width: Optional[int] = None, height: Optional[int] = None
    ) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.image_width = width
        self.image_height = height

        self.set_image(image, roi=roi)

        self.main_layout.addWidget(self.image_label)
        self.setLayout(self.main_layout)

    def set_image(self, image: Image, roi: Optional[ROI] = None) -> None:
        self.image = image

        pixmap = get_pixmap_from_image(self.image, width=self.image_width, height=self.image_height)

        if roi:
            scale_factor = self.image.get_scale_factor(width=self.image_width, height=self.image_height)
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.red, 2, Qt.DashDotDotLine))
            painter.drawRect(
                int(roi.x0 * scale_factor),
                int(roi.y0 * scale_factor),
                int((roi.x1 - roi.x0) * scale_factor),
                int((roi.y1 - roi.y0) * scale_factor),
            )
            painter.end()

        self.setToolTip(self.image.name)
        self.image_label.setPixmap(pixmap)

    @staticmethod
    def placeholder(**kwargs: Any) -> CQImage:
        width = kwargs.get("width")
        height = kwargs.get("height")
        if width and height:
            placeholder_size = (width, height)
        elif width:
            placeholder_size = (width, width)
        elif height:
            placeholder_size = (height, height)
        else:
            placeholder_size = (128, 128)

        im = Image(np.zeros(placeholder_size))
        cqimage = CQImage(im, **kwargs)
        return cqimage
