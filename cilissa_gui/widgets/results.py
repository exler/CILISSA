from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidgetItem, QMessageBox

from cilissa.images import ImagePair
from cilissa.results import Result, ResultGenerator


class CQResultsItem(QListWidgetItem):
    def __init__(self, index: int, image_pair: ImagePair, image_results: List[Result]) -> None:
        super().__init__(f"Operations ran for image pair #{index + 1}. Double-click here for details.")

        self.image_pair = image_pair.copy()
        self.results = image_results


class CQResultsDialog(QMessageBox):
    def __init__(self, image_pair: ImagePair, results: Result) -> None:
        super().__init__()

        self.setIcon(QMessageBox.NoIcon)
        self.setWindowIcon(QIcon(":cilissa-icon"))
        self.setWindowTitle("Results Window")

        html = self.format_image_pair_as_html(image_pair)
        html += ResultGenerator(results).to_html()
        self.setTextFormat(Qt.RichText)
        self.setText(html)
        self.setStandardButtons(QMessageBox.Close)

        self.layout().setSpacing(16)
        self.layout().setContentsMargins(0, 16, 24, 16)

    def format_image_pair_as_html(self, image_pair: ImagePair) -> str:
        im1_data_uri = image_pair[0].get_resized(height=128).as_data_uri()
        im2_data_uri = image_pair[1].get_resized(height=128).as_data_uri()

        return f"""
            <div align='center'>
                <table border='0' cellpadding='16' >
                    <tr>
                        <td align='center'><strong>Reference image</strong></td>
                        <td align='center'><strong>Input image</strong></td>
                    </tr>
                    <tr>
                        <td align='center'>
                            <img src='{im1_data_uri}' />
                        </td>
                        <td align='center'>
                            <img src='{im2_data_uri}' />
                        </td>
                    </tr>
                </table>
            </div>
        """
