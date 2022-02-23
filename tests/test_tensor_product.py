from qcp.tensor_product import tensor_product
from qcp.square_matrix import SquareMatrix

I = SquareMatrix([[1,0],[0,1]])

def test_tensor_product_with_identity():

    A = SquareMatrix([[1, 2], [3, 4]])

    C = tensor_product(I, A)

    expected = SquareMatrix(
        [
            [1,2,0,0],
            [3,4,0,0],
            [0,0,1,2],
            [0,0,3,4]
        ]
    )

    assert(C.get_state() == expected.get_state(), "Matrix does not return expected entries!")