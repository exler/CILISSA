from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel


class Workspace(QGridLayout):
    def __init__(self) -> None:
        super().__init__()

        self.change_base_image()
        self.change_comp_image()

    def change_base_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setPixmap(image)
        self.addWidget(image_label, 0, 0)

    def change_comp_image(self) -> None:
        # TODO: Implement me
        image = QPixmap(":placeholder-128")
        image_label = QLabel()
        image_label.setPixmap(image)
        self.addWidget(image_label, 0, 1)
