from typing import Optional

from PySide6.QtGui import QImage, QPixmap

from cilissa.images import Image


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
