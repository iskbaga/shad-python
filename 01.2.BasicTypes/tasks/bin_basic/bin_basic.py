def find_value(nums: list[int] | range, value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    left = 0
    right = len(nums)
    while right - left > 1:
        med = (right + left) // 2
        if nums[med] <= value:
            left = med
        else:
            right = med
    return left < len(nums) and nums[left] == value
