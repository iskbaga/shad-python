import numpy as np
import numpy.typing as npt


def nonzero_product(matrix: npt.NDArray[np.int_]) -> int | None:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    diag = np.diagonal(matrix)
    diag = diag[diag != 0]
    if not diag.size:
        return None
    return int(np.prod(diag))
