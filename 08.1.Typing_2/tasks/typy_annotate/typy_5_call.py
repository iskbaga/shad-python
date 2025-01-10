import collections.abc
import typing as tp

T_1 = tp.TypeVar('T_1', complex, float, int)
T_2 = tp.TypeVar('T_2', complex, float, int)
T_3 = tp.TypeVar('T_3', complex, float, int)


def f(a: collections.abc.Callable[[T_1, T_2, T_3], float], b: T_1, c: T_2, d: T_3) -> float:
    return a(b, c, d)


TEST_SAMPLES = """
# SUCCESS
def g(a: float, b: float, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# SUCCESS
def g(a: complex, b: complex, c: complex) -> bool:
    return True

f(g, 1, 4, True)

# ERROR
def g(a: bool, b: float, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# ERROR
def g(a: int, b: int, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# ERROR
def g(a: int, b: float, c: float) -> int:
    return 1

f(g, 1, 4.5, 1j)

# SUCCESS
def g(a: float, b: float, c: complex) -> float:
    return 1.0

f(g, True, True, True)

# ERROR
def g(a: float, b: float, c: complex) -> complex:
    return 1j

f(g, True, True, True)
"""
