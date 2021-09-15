from __future__ import annotations

import csv
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Union

import numpy as np

from cilissa.classes import Parameterized
from cilissa.images import Image
from cilissa.utils import get_parameter_display_name

if TYPE_CHECKING:
    from cilissa.operations import ImageOperation


@dataclass(frozen=True)  # type: ignore
class Result(Parameterized, ABC):
    name: str
    parameters: Dict[str, Any]
    value: Union[float, np.float64, Image]
    type: ImageOperation

    def __eq__(self, o: Any) -> bool:
        if isinstance(o, Result):
            return self.name == o.name and np.isclose(self.value, o.value, rtol=1e-05, atol=1e-08)  # type: ignore
        elif isinstance(o, float):
            return np.isclose(self.value, o, rtol=1e-05, atol=1e-08, equal_nan=False)  # type: ignore
        else:
            return self.value == o


class ResultGenerator:
    @staticmethod
    def to_html(results: List[Result]) -> str:
        def get_table_head() -> str:
            return """
            <thead>
                <tr>
                    <th>type</th>
                    <th>name</th>
                    <th>parameters</th>
                    <th>value</th>
                </tr>
            </thead>
            """

        def get_table_body(results: List[Result]) -> str:
            html = ""
            for result in results:
                html += get_table_row(result)
            return html

        def get_table_row(result: Result) -> str:
            html = "<tr>"
            html += get_table_cell(result.type.get_class_name())
            html += get_table_cell(result.name)
            html += get_table_cell(result.parameters)
            html += get_table_cell(result.value)
            html += "</tr>"
            return html

        def get_table_cell(value: Any) -> str:
            def format_parameters(parameters: Dict[str, Any]) -> str:
                if parameters:
                    html = "<ul>"
                    html += "".join(
                        ["<li>{}: {}</li>".format(get_parameter_display_name(k), v) for k, v in parameters.items()]
                    )
                    html += "</ul>"
                else:
                    html = "No parameters"
                return html

            html = "<td>"

            if isinstance(value, Image):
                data_uri = value.as_data_uri(height=64)
                html += f"<img src='{data_uri}'>"
            elif isinstance(value, dict):
                html += format_parameters(value)
            elif isinstance(value, float) or isinstance(value, np.floating):
                html += str(round(value, 4))
            else:
                html += str(value)

            html += "</td>"
            return html

        html = "<table border='1' cellpadding='8'>"
        html += get_table_head()
        html += get_table_body(results)
        html += "</table>"
        return html

    @staticmethod
    def to_csv(results: List[Result], output_path: Union[Path, str]) -> None:
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["type", "name", "parameters", "value"])

            for result in results:
                writer.writerow(
                    [
                        result.type.get_class_name(),
                        result.name,
                        str(result.parameters),
                        result.value if not isinstance(result.value, Image) else "",
                    ]
                )
