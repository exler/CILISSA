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
    QLabel,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from cilissa.helpers import clamp
from cilissa.images import Image
from cilissa.operations import ImageOperation
from cilissa.results import AnalysisResult
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
    def __init__(self, image: Image) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image = image

        self.create_actions()

        self.image_label = QLabel()
        thumbnail = QImage(self.image.get_thumbnail(64, 64), 64, 64, 64 * self.image.channels_num, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(thumbnail)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.setLayout(self.main_layout)

        self.setMaximumHeight(96)

    @staticmethod
    def load(image_path: Union[Path, str]) -> CQImage:
        im = Image(image_path)
        cqimage = CQImage(im)
        return cqimage

    def create_actions(self) -> None:
        pass

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


class CQROIImage(QLabel):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

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
        thumbnail = QImage(image.get_thumbnail(128, 128), 128, 128, 128 * image.channels_num, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(thumbnail)
        self.setPixmap(pixmap)
