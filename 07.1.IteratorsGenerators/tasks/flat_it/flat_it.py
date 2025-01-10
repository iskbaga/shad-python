from collections.abc import Iterable, Iterator
from typing import Any


def flat_it(sequence: Iterable[Any]) -> Iterator[Any]:
    """
    :param sequence: iterable with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for item in sequence:
        if isinstance(item, Iterable) and not isinstance(item, (str, range)):
            yield from flat_it(item)
        elif isinstance(item, (str, range)):
            yield from item
        else:
            yield item
