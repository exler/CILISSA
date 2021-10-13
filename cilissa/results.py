from __future__ import annotations

import csv
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

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
    def __init__(self, results: List[Result]) -> None:
        self.results = results
        self.last_changes: Dict[str, float] = {}

    def get_change_in_metric(self, name: str, value: float) -> float:
        if name in self.last_changes:
            change = value - self.last_changes[name]
            self.last_changes[name] = change
        else:
            self.last_changes[name] = value
            return 0

        return change

    def to_html(self) -> str:
        def get_table_head() -> str:
            return """
            <thead>
                <tr>
                    <th>type</th>
                    <th>name</th>
                    <th>parameters</th>
                    <th width="128">value</th>
                    <th>change</th>
                </tr>
            </thead>
            """

        def get_table_body(results: List[Result]) -> str:
            html = ""
            for result in results:
                html += get_table_row(result)
            return html

        def get_table_row(result: Result) -> str:
            from cilissa.operations import Metric

            def get_prefix_for_change(change: Union[float, np.floating]) -> str:
                if change > 0:
                    return "+"
                else:
                    return ""

            html = "<tr>"
            html += get_table_cell(result.type.get_class_name())
            html += get_table_cell(result.name)
            html += get_table_cell(result.parameters)
            html += get_table_cell(result.value)
            if result.type == Metric:
                change = self.get_change_in_metric(result.name, float(result.value))  # type: ignore
                html += get_table_cell(change if change != 0 else "", prefix=get_prefix_for_change(change))
            html += "</tr>"
            return html

        def get_table_cell(value: Any = None, prefix: Optional[str] = None) -> str:
            def format_parameters(parameters: Dict[str, Any]) -> str:
                if parameters:
                    html = "".join(
                        [
                            "• <strong>{}</strong>: {}<br>".format(get_parameter_display_name(k), v)
                            for k, v in parameters.items()
                        ]
                    )
                else:
                    html = "No parameters"
                return html

            html = "<td align='center'>"
            if prefix:
                html += prefix

            if isinstance(value, Image):
                data_uri = value.get_resized(height=64).as_data_uri()
                html += f"<img src='{data_uri}'>"
            elif isinstance(value, dict):
                html += format_parameters(value)
            elif isinstance(value, float) or isinstance(value, np.floating):
                html += str(round(value, 4))
            else:
                html += str(value)

            html += "</td>"
            return html

        html = "<table border='1' cellpadding='8' width='728'>"
        html += get_table_head()
        html += get_table_body(self.results)
        html += "</table>"
        return html

    def to_csv(self, output_path: Union[Path, str]) -> None:
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["type", "name", "parameters", "value"])

            for result in self.results:
                writer.writerow(
                    [
                        result.type.get_class_name(),
                        result.name,
                        str(result.parameters),
                        result.value if not isinstance(result.value, Image) else "",
                    ]
                )
