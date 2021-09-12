from typing import Any

import numpy as np
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QMouseEvent, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QVBoxLayout,
)

from cilissa.images import Image, ImagePair
from cilissa.roi import ROI
from cilissa_gui.helpers import get_pixmap_from_image, get_screen_size


class CQROIDialog(QDialog):
    def __init__(self, image_pair: ImagePair, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Select ROI")

        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.image_pair = image_pair
        self.image = CQROIImage(image_pair.get_full_image(0))

        self.buttons_panel = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)
        self.buttons_panel.addWidget(self.confirm_button)

        self.main_layout.addWidget(self.image)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)

    def confirm(self) -> None:
        roi = self.image.get_roi()
        self.image_pair.set_roi(roi)
        self.close()


class CQROIImage(QLabel):
    def __init__(self, image: Image, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        screen_size = get_screen_size()
        self.max_width = screen_size.width() - 192
        self.max_height = screen_size.height() - 192
        self.set_dimensions(image)

        self.set_image(image)

        self.point1 = None
        self.point2 = None
        self.draw_flag = False

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.draw_flag = True
        self.point1 = ev.localPos().toPoint()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.draw_flag = False

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self.draw_flag:
            pos = ev.localPos().toPoint()
            x = pos.x()
            y = pos.y()
            width = self.width() - 1
            height = self.height() - 1

            if x < 0 or x > width:
                x = np.clip(x, 0, width)
                pos.setX(x)

            if y < 0 or y > height:
                y = np.clip(y, 0, height)
                pos.setY(y)

            self.point2 = pos
            self.update()

    def paintEvent(self, ev: QPaintEvent) -> None:
        super().paintEvent(ev)
        try:
            rect = QRect(self.point1, self.point2)
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.DashDotDotLine))
            painter.drawRect(rect)
        except TypeError:
            # Object was just initialized
            pass

    def set_dimensions(self, image: Image) -> None:
        self.image_width = image.width
        self.image_height = image.height
        self.scale_factor = 1.0

        if self.max_width < self.image_width or self.max_height < self.image_height:
            width_factor = image.get_scale_factor(width=self.max_width)
            height_factor = image.get_scale_factor(height=self.max_height)

            if width_factor > height_factor:
                self.image_width = None
                self.image_height = self.max_height
                self.scale_factor = height_factor
            else:
                self.image_width = self.max_width
                self.image_height = None
                self.scale_factor = width_factor

    def set_image(self, image: Image) -> None:
        pixmap = get_pixmap_from_image(image, width=self.image_width, height=self.image_height)
        self.setPixmap(pixmap)

    def get_roi(self) -> ROI:
        if self.point1 and self.point2:
            x0 = int(self.point1.x() / self.scale_factor)
            y0 = int(self.point1.y() / self.scale_factor)
            x1 = int(self.point2.x() / self.scale_factor)
            y1 = int(self.point2.y() / self.scale_factor)

            return ROI(x0, y0, x1, y1)
        return ROI()
