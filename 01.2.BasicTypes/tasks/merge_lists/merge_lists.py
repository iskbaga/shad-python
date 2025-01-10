def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    i, j = 0, 0
    result = [0] * (len(lst_a) + len(lst_b))
    while i + j < len(result):
        if i == len(lst_a):
            result[i + j:] = lst_b[j:]
            break
        elif j == len(lst_b):
            result[i + j:] = lst_a[i:]
            break
        elif lst_a[i] < lst_b[j]:
            result[i + j] = lst_a[i]
            i += 1
        else:
            result[i + j] = lst_b[j]
            j += 1
    return result


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    return sorted(lst_a + lst_b)
