import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    nan_indices = np.isnan(matrix)
    meann = np.mean(matrix[~nan_indices])
    if np.isnan(meann):
        meann = 0
    res = matrix
    res[nan_indices] = meann
    return res.astype(np.float64)
