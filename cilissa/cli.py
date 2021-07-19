import ast
from typing import Any, Dict, List, Type

from cilissa.metrics import Metric
from cilissa.operations import ImageOperation
from cilissa.transformations import Transformation
from cilissa.utils import all_metrics, all_transformations


def get_operation_instances(operations: List[str], kwargs: Dict[str, Any]) -> List[Type[ImageOperation]]:
    all_operations = {**all_metrics, **all_transformations}

    instances = {"metrics": [], "transformations": []}
    for operation in operations:
        operation = all_operations.get(operation)
        op_kwargs = [arg for arg in kwargs if arg.find(operation.get_class_name()) == 0]
        parsed_kwargs = {}
        for arg in op_kwargs:
            start = len(operation.get_class_name()) + 1
            evaluate_type = False
            try:
                # Checking if argument has a value supplied
                key = arg[start : arg.index("=")].replace("-", "_")
                value = arg[arg.index("=") + 1 :]
                evaluate_type = True
            except ValueError:
                # Argument is a flag
                key = arg[start:]
                value = True

            if evaluate_type:
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
