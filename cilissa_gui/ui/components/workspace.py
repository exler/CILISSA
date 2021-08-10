from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QTabWidget, QVBoxLayout, QWidget


class Workspace(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.list_tab = WorkspaceList(self)
        self.details_tab = WorkspaceDetails(self)

        self.addTab(self.list_tab, "List")
        self.addTab(self.details_tab, "Details")


class WorkspaceTab(QWidget):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__()

        self.setMaximumWidth(parent.width())


class WorkspaceList(WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)


class WorkspaceDetails(WorkspaceTab):
    def __init__(self, parent: QTabWidget) -> None:
        super().__init__(parent)

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.change_base_image()
        self.change_comp_image()

    def change_base_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(image)
        self.main_layout.addWidget(image_label)

    def change_comp_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(image)
        self.main_layout.addWidget(image_label)


class ImagePairCard(QWidget):
    pass
