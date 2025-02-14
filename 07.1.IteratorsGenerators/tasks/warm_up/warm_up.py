from collections.abc import Generator
from typing import Any


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    res: list[list[Any]] = [[] for i in range(len(matrix[0]))]
    for row in matrix:
        for (i, x) in enumerate(row):
            res[i].append(x)
    return res


def uniq(sequence: list[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
    the same order without duplicates
    """
    seen_set: set[Any] = set()
    for x in sequence:
        if x not in seen_set:
            seen_set.add(x)
            yield x


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictionary
    """
    merged_dict: dict[Any, Any] = {}

    for d in dicts:
        merged_dict.update(d)

    return merged_dict


def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum([l * r for (l, r) in zip(lhs, rhs)])
