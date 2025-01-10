def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    x = min(a, b, c)
    y = max(a, b, c)
    return a + b + c - x - y
