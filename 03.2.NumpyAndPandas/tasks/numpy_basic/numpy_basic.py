import numpy as np
import numpy.typing as npt


def construct_array(
        matrix: npt.NDArray[np.int_],
        row_indices: npt.NDArray[np.int_] | list[int],
        col_indices: npt.NDArray[np.int_] | list[int]
) -> npt.NDArray[np.int_]:
    """
    Construct slice of given matrix by indices row_indices and col_indices:
    [matrix[row_indices[0], col_indices[0]], ... , matrix[row_indices[N-1], col_indices[N-1]]]
    :param matrix: input matrix
    :param row_indices: list of row indices
    :param col_indices: list of column indices
    :return: matrix slice
    """
    return matrix[row_indices, col_indices]


def detect_identic(
        lhs_array: npt.ArrayLike,
        rhs_array: npt.ArrayLike
) -> bool:
    """
    Check whether two arrays are equal or not
    :param lhs_array: first array
    :param rhs_array: second array
    :return: True if input arrays are equal, False otherwise
    """
    return np.array_equal(lhs_array, rhs_array)


def mean_channel(X: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """
    Given color image (3-dimensional vector of size (n, m, 3).
    Compute average value for all 3 channels
    :param X: color image
    :return: array of size 3 with average values
    """
    res = np.zeros(3)
    res[0] = np.mean(X[..., 0])
    res[1] = np.mean(X[..., 1])
    res[2] = np.mean(X[..., 2])
    return res


def get_unique_rows(X: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Compute unique rows of matrix
    :param X: matrix
    :return: matrix of unique rows
    """
    return np.unique(X, axis=0)


def construct_matrix(
        first_array: npt.NDArray[np.int_], second_array: npt.NDArray[np.int_]
) -> npt.NDArray[np.int_]:
    """
    Construct matrix from pair of arrays
    :param first_array: first array
    :param second_array: second array
    :return: constructed matrix
    """
    if not first_array.shape:
        return np.empty_like((first_array.shape[0], 2))

    res = np.zeros((first_array.shape[0], 2))
    res[:, 0] = first_array
    res[:, 1] = second_array

    return res.astype(np.int_)
