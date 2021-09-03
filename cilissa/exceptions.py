class ShapesNotEqual(Exception):
    """Two images must be of equal size to compare"""

    pass


class NotOnImageError(Exception):
    """Points of interest are outside image's boundary"""

    pass
