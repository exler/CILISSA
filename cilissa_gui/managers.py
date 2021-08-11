from PySide6.QtCore import QObject, Signal

from cilissa.core import OperationsList
from cilissa.images import ImageCollection
from cilissa_gui.meta import SingletonMeta


class OperationsManager(QObject, OperationsList, metaclass=SingletonMeta):
    """
    Singleton responsible for holding the operations list
    """

    changed = Signal()


class ImageCollectionManager(QObject, ImageCollection, metaclass=SingletonMeta):
    """
    Singleton responsible for holding the image collection
    """

    changed = Signal()
