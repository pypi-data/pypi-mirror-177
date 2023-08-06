import math

__default_a = 7
__default_b = 2
__default_c = 8


def triangle_perimeter(a=__default_a, b=__default_b, c=__default_c) -> float:
    return a + b + c


def triangle_area(a=__default_a, b=__default_b, c=__default_c) -> float:
    p: float = triangle_perimeter(a, b, c) / 2

    return math.sqrt(p * (p - a) * (p - b) * (p - c))
