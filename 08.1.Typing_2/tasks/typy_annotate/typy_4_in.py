import numbers
from typing import Optional, Container, TypeVar

T = TypeVar('T', str, numbers.Real, int)


def f(a: Container[T], b: T) -> Optional[T]:
    return b if b in a else None


TEST_SAMPLES = """
# SUCCESS

a: float | None
a = f([1, 2, 3], 1)
if a is not None:
    a += 1

# SUCCESS
a: float | None
a = f({1, 2, 3}, 1)


# SUCCESS
a: str | None
a = f("abcd", "a")

# SUCCESS
class A:
    def __contains__(self, a: object) -> bool:
        return True

a: int | None
a = f(A(), 10)

b: str | None
b = f(A(), "qwerty")

# ERROR
f([1, 2, 3], "h")

# ERROR
f([1, 2, 3], 1.3)

# ERROR
f([1.4, 2, 3], 1)

# ERROR
f(["a", "b", "c"], 1)
"""
