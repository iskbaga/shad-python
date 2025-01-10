import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return max element after zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """

    zero_indices = np.where(array == 0)[0]
    zero_indices = zero_indices + 1
    zero_indices = zero_indices[zero_indices < len(array)]

    if not zero_indices.size:
        return None

    return int(np.max(array[zero_indices]))
