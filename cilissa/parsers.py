import ast
import logging
from typing import Any, List

from cilissa import metrics  # noqa
from cilissa import transformations  # noqa
from cilissa.operations import ImageOperation
from cilissa.roi import ROI


def parse_operations_from_str(operations: List[str], kwargs: List[Any]) -> List[ImageOperation]:
    """
    Parses operations and their parameters from string input.

    Parameters use the following format:

    `<operation-name>-<parameter-name>=<value>`

    where `parameter-name` uses hyphens (-) instead of underscores (_).
    """
    op_dict = {op.get_class_name(): op for op in ImageOperation.get_subclasses()}

    instances: List[ImageOperation] = []
    for op_name in operations:
        operation = op_dict.get(op_name)
        if not operation:
            continue

        op_kwargs = [arg for arg in kwargs if arg.find(operation.get_class_name()) == 0]
        parsed_kwargs = {}
        for arg in op_kwargs:
            slice_from = len(operation.get_class_name()) + 1
            value: Any
            try:
                # Checking if argument has a value supplied
                key = arg[slice_from : arg.index("=")].replace("-", "_")
                value = arg[arg.index("=") + 1 :]
            except ValueError:
                # Argument is a flag
                key = arg[slice_from:]
                value = True

            if isinstance(value, str):
                # Try to figure out the correct type for argument
                try:
                    value = ast.literal_eval(value)
                except ValueError:
                    # Argument is a string or cannot guess correct type
                    pass

            parsed_kwargs[key] = value

        instance = operation(**parsed_kwargs)  # type: ignore
        instances.append(instance)

    return instances


def parse_roi(string: str) -> ROI:
    points = string.split(",")

    start_point = points[0].split("x")
    end_point = points[1].split("x")

    try:
        x0 = int(start_point[0])
        y0 = int(start_point[1])
        x1 = int(end_point[0])
        y1 = int(end_point[1])
    except TypeError:
        logging.error("ROI points must be integers")

    return ROI(x0, y0, x1, y1)
