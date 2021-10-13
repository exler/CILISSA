from dataclasses import dataclass
from typing import Tuple


@dataclass
class ROI:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def start_point(self) -> Tuple[int, int]:
        return (self.x0, self.y0)

    @property
    def end_point(self) -> Tuple[int, int]:
        return (self.x1, self.y1)

    @property
    def slices(self) -> Tuple[slice, slice]:
        return (slice(self.y0, self.y1), slice(self.x0, self.x1))
