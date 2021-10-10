from dataclasses import dataclass
from typing import Tuple


@dataclass
class ROI:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def slices(self) -> Tuple[slice, slice]:
        return (slice(self.y0, self.y1), slice(self.x0, self.x1))
