from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Type, Union

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import (
    QAction,
    QContextMenuEvent,
    QImage,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from cilissa.helpers import clamp
from cilissa.images import Image
from cilissa.operations import ImageOperation
from cilissa.results import AnalysisResult
from cilissa.roi import ROI
from cilissa_gui.managers import OperationsManager


class CQOperation(QWidget):
    def __init__(self, operation: Type[ImageOperation]) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.operation = operation
        self.operations_manager = OperationsManager()

        self.create_actions()

        self.image_label = QLabel()
        pixmap = QPixmap(":placeholder-64")
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(operation.get_class_name())
        self.text_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.text_label)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(96)

    def create_actions(self) -> None:
        self.add_with_default_params_action = QAction(
            "Add With Default Parameters",
            self,
            statusTip="Add operation to list",
            triggered=self.add_with_default_params,
        )

    def add_with_default_params(self) -> None:
        self.operations_manager.push(self.operation())
        self.operations_manager.changed.emit()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.add_with_default_params_action)
        menu.exec(event.globalPos())


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
        self.setMaximumHeight(self.image.height + 32)

        resized_image = self.image.get_resized(width=self.width, height=self.height)

        q_image = QImage(
            resized_image.im,
            resized_image.width,
            resized_image.height,
            resized_image.width * resized_image.channels_num,
            QImage.Format_BGR888,
        )

        pixmap = QPixmap.fromImage(q_image)
        if roi:
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.red, 2, Qt.DashDotDotLine))
            painter.drawRect(roi.x0, roi.y0, roi.x1 - roi.x0, roi.y1 - roi.y0)
            painter.end()

        self.image_label.setPixmap(pixmap)

    @staticmethod
    def load(image_path: Union[Path, str], **kwargs: Any) -> CQImage:
        im = Image(image_path)
        cqimage = CQImage(im, **kwargs)
        return cqimage

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.exec(event.globalPos())


class CQResult(QListWidgetItem):
    def __init__(self, result: AnalysisResult) -> None:
        super().__init__(result.pretty())

        self.result = result


class CQResultDialog(QMessageBox):
    def __init__(self, result: AnalysisResult) -> None:
        super().__init__()

        self.result = result

        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle("Analysis result")

        self.setTextFormat(Qt.RichText)
        self.setText(self.format_result())
        self.setStandardButtons(QMessageBox.Close)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 16, 24, 8)

    def format_result(self) -> None:
        result_list: List[str] = []
        d = self.result.get_parameters_dict()
        for field_name, field_value in d.items():
            html = self.get_html_for_result_field(field_name, field_value)
            if html:
                result_list.append(html)

        return "<br>".join([s for s in result_list]) + "<br>"

    def get_html_for_result_field(self, field_name: str, field_value: Any) -> str:
        html = f"<strong>{field_name.capitalize()}:</strong> "
        t = self.result.get_parameter_type(field_name)

        if t == dict:
            items = field_value.items()
            if items:
                html += "<ul>"
                html += "".join(["<li>{}: {}</li>".format(k, v) for k, v in items])
                html += "</ul>"
            else:
                html += "No parameters"
        elif t == Image:
            return ""
        else:
            html += str(field_value)

        return html


class CQErrorDialog(QMessageBox):
    def __init__(self, msg: str, title: Optional[str] = None) -> None:
        super().__init__()

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(title or "An error occurred")

        self.setTextFormat(Qt.PlainText)
        self.setText(msg)
        self.setStandardButtons(QMessageBox.Ok)


class CQROIDialog(QDialog):
    def __init__(self, image: Image, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.main_layout = QVBoxLayout()

        self.image = CQROIImage(image)

        self.buttons_panel = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)
        self.buttons_panel.addWidget(self.confirm_button)

        self.main_layout.addWidget(self.image)
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)

    def confirm(self) -> None:
        roi = self.image.get_roi()
        print(roi)
        self.close()


class CQROIImage(QLabel):
    def __init__(self, image: Image, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

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
                x = clamp(x, 0, width)
                pos.setX(x)

            if y < 0 or y > height:
                y = clamp(y, 0, height)
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

    def set_image(self, image: Image) -> None:
        resized_image = image.get_resized()

        thumbnail = QImage(
            resized_image.im,
            resized_image.width,
            resized_image.height,
            resized_image.width * resized_image.channels_num,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap.fromImage(thumbnail)
        self.setPixmap(pixmap)

    def get_roi(self) -> ROI:
        if self.point1 and self.point2:
            return ROI(self.point1.x(), self.point1.y(), self.point2.x(), self.point2.y())
        return ROI()
