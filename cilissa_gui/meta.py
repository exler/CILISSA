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

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwargs)
                self._instances[self] = instance
        return self._instances[self]
