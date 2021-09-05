from typing import Any, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox

from cilissa.images import Image
from cilissa.results import Result


class CQResult(QListWidgetItem):
    def __init__(self, result: Result) -> None:
        super().__init__(result.pretty())

        self.result = result


class CQResultDialog(QMessageBox):
    def __init__(self, result: Result) -> None:
        super().__init__()

        self.result = result

        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle("Analysis result")

        self.setTextFormat(Qt.RichText)
        self.setText(self.format_result())
        self.setStandardButtons(QMessageBox.Close)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 16, 24, 8)

    def format_result(self) -> None:
        result_list: List[str] = []
        d = self.result.get_parameters_dict()
        for field_name, field_value in d.items():
            html = self.get_html_for_result_field(field_name, field_value)
            if html:
                result_list.append(html)

        return "<br>".join([s for s in result_list]) + "<br>"

    def get_html_for_result_field(self, field_name: str, field_value: Any) -> str:
        html = f"<strong>{field_name.capitalize()}:</strong> "
        t = self.result.get_parameter_type(field_name)

        if t == dict:
            items = field_value.items()
            if items:
                html += "<ul>"
                html += "".join(["<li>{}: {}</li>".format(k, v) for k, v in items])
                html += "</ul>"
            else:
                html += "No parameters"
        elif t == Image:
            return ""
        else:
            html += str(field_value)

        return html
