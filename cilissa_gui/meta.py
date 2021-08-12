from threading import Lock
from typing import Any

from PySide6.QtCore import QObject


class SingletonMeta(type(QObject), type):
    """
    Thread-safe implementation of Singleton.

    Subclassing from the QObject type to work with Qt signals & slots

    References:
        - https://refactoring.guru/design-patterns/singleton/python/example
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
