import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    if not x.shape[0]:
        return np.empty(x.shape).astype(np.int_)
    res = np.zeros(x.shape[0] * 2 - 1)
    res[::2] = x
    return res.astype(np.int_)
