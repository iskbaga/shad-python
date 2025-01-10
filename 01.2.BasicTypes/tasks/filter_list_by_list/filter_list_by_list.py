def filter_list_by_list(lst_a: list[int] | range, lst_b: list[int] | range) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    result: list[int] = []
    i, j = 0, 0
    lst_a = list(lst_a)
    lst_b = list(lst_b)
    while i < len(lst_a):
        if j >= len(lst_b):
            result = result + lst_a[i:]
            break
        else:
            if lst_a[i] > lst_b[j]:
                while j < len(lst_b) and lst_a[i] > lst_b[j]:
                    j += 1
            elif lst_a[i] == lst_b[j]:
                i += 1
            else:
                result.append(lst_a[i])
                i += 1
    return result
