import ast
from typing import Any, Dict, List

from cilissa.metrics import Metric
from cilissa.operations import ImageOperation
from cilissa.transformations import Transformation
from cilissa.utils import all_metrics, all_transformations


def get_operation_instances(operations: List[str], kwargs: List[Any]) -> Dict[str, List[ImageOperation]]:
    all_operations = {**all_metrics, **all_transformations}

    instances: Dict[str, List[ImageOperation]] = {"metrics": [], "transformations": []}
    for op_name in operations:
        operation = all_operations.get(op_name)
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

        instance = operation(**parsed_kwargs)

        if issubclass(operation, Metric):
            key = "metrics"
        elif issubclass(operation, Transformation):
            key = "transformations"

        instances[key].append(instance)

    return instances
