from typing import Any, List

from PySide6.QtCore import QObject, Signal

from cilissa.core import OperationsList
from cilissa.images import ImageCollection
from cilissa_gui.meta import SingletonMeta


class OperationsManager(QObject, OperationsList, metaclass=SingletonMeta):
    """
    Singleton responsible for holding the operations list
    """

    items: List[Any] = []  # Redeclaring to avoid sharing resources with other singleton instances

    changed = Signal()


class ImageCollectionManager(QObject, ImageCollection, metaclass=SingletonMeta):
    """
    Singleton responsible for holding the image collection
    """

    items: List[Any] = []  # Redeclaring to avoid sharing resources with other singleton instances

    changed = Signal()
