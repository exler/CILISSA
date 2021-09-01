class ShapesNotEqual(Exception):
    """Two images must be of equal size to compare."""

    pass


class WrongROIDimensions(Exception):
    """ROI dimensions must be between 0 and width/height of the image"""

    pass
