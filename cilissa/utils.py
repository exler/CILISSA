from typing import Dict, Type

from cilissa.operations import ImageOperation


def get_operation_subclasses(operation: Type[ImageOperation]) -> Dict[str, Type[ImageOperation]]:
    subclasses = operation.__subclasses__()
    operations = {}
    for cls in subclasses:
        operations[cls.get_class_name()] = cls

    return operations
