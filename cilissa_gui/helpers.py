from inspect import isclass
from typing import Optional

from PySide6.QtGui import QImage, QPixmap

from cilissa.images import Image
from cilissa.operations import ImageOperation, Metric, Transformation


def get_operation_icon_name(operation: ImageOperation) -> str:
    if isclass(operation):
        if issubclass(operation, Transformation):
            return ":letter-t"
        elif issubclass(operation, Metric):
            return ":letter-m"
    else:
        if isinstance(operation, Transformation):
            return ":letter-t"
        elif isinstance(operation, Metric):
            return ":letter-m"

    return ""


def get_parameter_display_name(parameter: str) -> str:
    return parameter.replace("_", " ").capitalize()


def get_pixmap_from_image(image: Image, width: Optional[int] = None, height: Optional[int] = None) -> QPixmap:
    resized_image = image.get_resized(width=width, height=height)
    q_im = QImage(
        resized_image.im,
        resized_image.width,
        resized_image.height,
        resized_image.width * resized_image.channels_num,
        QImage.Format_BGR888,
    )
    return QPixmap.fromImage(q_im)
