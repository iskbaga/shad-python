from __future__ import annotations
import typing as tp

A = tp.TypeVar('A', int, float)


class Pair(tp.Generic[A]):
    def __init__(self, a: A, b: A) -> None:
        self.a: A = a
        self.b: A = b

    def sum(self) -> A:
        return self.a + self.b

    def first(self) -> A:
        return self.a

    def second(self) -> A:
        return self.b

    def __iadd__(self, pair: Pair[A]) -> Pair[A]:
        self.a += pair.a
        self.b += pair.b
        return self
