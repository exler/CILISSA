from dataclasses import dataclass
from typing import Tuple, Union


@dataclass
class ROI:
    x0: Union[int, None] = None
    y0: Union[int, None] = None
    x1: Union[int, None] = None
    y1: Union[int, None] = None

    @property
    def slices(self) -> Tuple[slice, slice]:
        return (slice(self.y0, self.y1), slice(self.x0, self.x1))
