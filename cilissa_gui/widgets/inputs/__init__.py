from typing import Type, Union

from .base import CQInputWidget
from .boolean import CQBooleanInputWidget
from .number import CQFloatInputWidget, CQIntInputWidget


def get_input_widget_for_type(input_type: Union[Type, None]) -> Union[CQInputWidget, None]:
    if not input_type:
        return None

    if isinstance(1, input_type):
        return CQIntInputWidget
    elif isinstance(1.0, input_type):
        return CQFloatInputWidget
    elif isinstance(True, input_type):
        return CQBooleanInputWidget
    else:
        return None
