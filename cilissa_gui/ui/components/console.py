from PySide6.QtWidgets import QListWidget, QListWidgetItem


class Console(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(168)

        # TODO: Implement me
        self.addItem(QListWidgetItem("Metric: MSE, result: 0.67"))
        self.addItem(QListWidgetItem("Metric: SSIM, result: 0.64258"))
