from PySide6.QtWidgets import QListWidget, QListWidgetItem


class OperationsQueue(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(168)

        # TODO: Implement me
        self.addItem(QListWidgetItem("MSE"))
        self.addItem(QListWidgetItem("Blur"))
        self.addItem(QListWidgetItem("Sharpen"))
        self.addItem(QListWidgetItem("SSIM"))
