from qcp.tensor_product import tensor_product
from qcp.square_matrix import SquareMatrix
import pytest

IDENTITY = SquareMatrix([[1, 0], [0, 1]])


def test_tensor_product_with_identity():

    A = SquareMatrix([[1, 2], [3, 4]])

    C = tensor_product(IDENTITY, A)

    expected = SquareMatrix(
        [
            [1, 2, 0, 0],
            [3, 4, 0, 0],
            [0, 0, 1, 2],
            [0, 0, 3, 4]
        ]
    )

    assert C.get_state() == expected.get_state()


def test_tensor_product_mismatch_column_dimensions():

    A = SquareMatrix([[1, 2], [3, 4]])
    B = SquareMatrix([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(AssertionError) as ae:
        _ = tensor_product(A, B)
    assert ae.match("A and B have mismatched column dimensions!")


def test_tensor_product_mismatch_row_dimensions():

    A = SquareMatrix([[1, 2], [3, 4]])
    B = SquareMatrix([[1, 2, 3], [4, 5, 6]])

    with pytest.raises(AssertionError) as ae:
        _ = tensor_product(A, B)
    assert ae.match("A and B have mismatched row dimensions!")
