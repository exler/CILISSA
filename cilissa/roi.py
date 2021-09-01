from dataclasses import dataclass


@dataclass
class ROI:
    x0: int = None
    y0: int = None
    x1: int = None
    y1: int = None

    def get_slices(self) -> slice:
        return (slice(self.y0, self.y1), slice(self.x0, self.x1))
