from PySide6.QtCore import QObject, Signal

from cilissa.core import OperationsQueue
from cilissa_gui.meta import SingletonMeta


class QueueManager(QObject, OperationsQueue, metaclass=SingletonMeta):
    """
    Singleton responsible for holding the operations queue
    """

    changed = Signal()
