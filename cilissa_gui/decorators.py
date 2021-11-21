import sys
from contextlib import ContextDecorator


class PathInsert(ContextDecorator):
    """
    Non-thread-safe context manager that allows for temporarily appending a single path to the system path.
    """

    def __init__(self, p: str) -> None:
        self.ins_path = p

    def __enter__(self) -> None:
        self._sys_path = sys.path
        sys.path = sys.path[:]
        sys.path.insert(0, self.ins_path)

    def __exit__(self, *exc: Exception) -> None:
        sys.path = self._sys_path
