import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float64], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """

    if not np.size(matrix):
        return None
    temp_matrix = abs(matrix - value)

    minn = np.min(temp_matrix)

    ind = np.where(temp_matrix == minn)
    return float(matrix[ind[0][0], ind[1][0]])
