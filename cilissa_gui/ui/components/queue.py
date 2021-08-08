from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidget

from cilissa_gui.managers import QueueManager


class Queue(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.queue_manager = QueueManager()
        self.queue_manager.changed.connect(self.refresh)

        self.setMaximumHeight(168)

    @Slot()
    def refresh(self) -> None:
        self.clear()
        for item in self.queue_manager.get_order():
            self.addItem(item[1].get_class_name())
