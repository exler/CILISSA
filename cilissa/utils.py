from typing import Dict, Type

from cilissa.metrics import Metric
from cilissa.operations import ImageOperation
from cilissa.transformations import Transformation


def get_operation_subclasses(operation: Type[ImageOperation]) -> Dict[str, Type[ImageOperation]]:
    subclasses = operation.__subclasses__()
    operations = {}
    for cls in subclasses:
        operations[cls.get_class_name()] = cls

    return operations


all_metrics = get_operation_subclasses(Metric)
all_transformations = get_operation_subclasses(Transformation)
