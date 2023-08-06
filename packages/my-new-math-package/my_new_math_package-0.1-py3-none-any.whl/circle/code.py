import math

__default_radius = 5


def circle_perimeter(radius: float = __default_radius.__float__()) -> float:
    return 2 * math.pi * radius


def circle_area(radius: float = __default_radius.__float__()) -> float:
    return math.pi * radius ** 2
