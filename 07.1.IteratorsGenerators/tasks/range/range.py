from collections.abc import Iterable, Iterator, Sized


class RangeIterator(Iterator[int]):
    """The iterator class for Range"""

    def __init__(self, range_: 'Range') -> None:
        self._range = range_
        self._cur = self._range.start

    def __iter__(self) -> 'RangeIterator':
        return self

    def __next__(self) -> int:
        if (1 if self._range.step > 0 else -1) * self._cur >= abs(self._range.stop):
            raise StopIteration
        cur = self._cur
        self._cur += self._range.step
        return cur


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        if len(args) == 0:
            self.start, self.stop, self.step = 0, 0, 1
        elif len(args) == 1:
            self.start, self.stop, self.step = 0, args[0], 1
        elif len(args) == 2:
            self.start, self.stop, self.step = args[0], args[1], 1
        elif len(args) == 3:
            self.start, self.stop, self.step = args[0], args[1], args[2]
        else:
            raise TypeError

        if self.step == 0:
            raise ValueError

    def __iter__(self) -> 'RangeIterator':
        return RangeIterator(self)

    def __repr__(self) -> str:
        return f"Range({self.start}, {self.stop}, {self.step})"

    def __str__(self) -> str:
        if self.step == 1:
            return f"range({self.start}, {self.stop})"
        return f"range({self.start}, {self.stop}, {self.step})"

    def __contains__(self, key: int) -> bool:
        if self.step > 0:
            return self.start <= key < self.stop and (key - self.start) % self.step == 0
        return self.stop < key <= self.start and (key - self.start) % self.step == 0

    def __getitem__(self, key: int) -> int:
        if key < 0:
            key += self.__len__()
        if key < 0 or key >= self.__len__():
            raise IndexError
        return self.start + key * self.step

    def __len__(self) -> int:
        if self.step > 0:
            return max(0, (self.stop - self.start + (self.step - 1)) // self.step)
        return max(0, (self.start - self.stop + (-self.step - 1)) // -self.step)
