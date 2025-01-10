from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    k = 0
    j = 0
    med1 = 0.0
    med2 = 0.0
    if len(nums1) == 0:
        if len(nums2) % 2 == 0:
            return (nums2[len(nums2) // 2 - 1] + nums2[(len(nums2) // 2)]) / 2
        return float(nums2[len(nums2) // 2])

    if len(nums2) == 0:
        if len(nums1) % 2 == 0:
            return (nums1[len(nums1) // 2 - 1] + nums1[(len(nums1) // 2)]) / 2
        return float(nums1[len(nums1) // 2])

    sumLen = len(nums1) + len(nums2)
    for i in range((sumLen // 2) + 1):
        med1 = med2
        if j >= len(nums2) or (k < len(nums1) and nums1[k] < nums2[j]):
            med2 = nums1[k]
            k += 1
        else:
            med2 = nums2[j]
            j += 1
    if sumLen % 2 == 0:
        return (med1 + med2) / 2
    return float(med2)
