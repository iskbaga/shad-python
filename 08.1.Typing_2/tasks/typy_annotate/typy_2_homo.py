from typing import Tuple, TypeVar, Optional

T = TypeVar("T", int, float, bool)


def f(a: Tuple[T, ...]) -> Optional[T]:
    return a[0] if a else None


TEST_SAMPLES = """
# SUCCESS
f((1, 1, 2, 4))

# SUCCESS
f((1,))

# SUCCESS
f((1.2, 3.4))

# ERROR
f((1j, 3j, 6j, 7j))

# SUCCESS
f((True, False))

# ERROR
f(("there", "are", "no", "reason"))

# ERROR
f(("there", 1))
"""
