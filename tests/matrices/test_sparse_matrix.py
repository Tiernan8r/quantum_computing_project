# Copyright 2022 Tiernan8r
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from copy import deepcopy
from qcp.matrices import SparseMatrix
import pytest


TEST_1x1 = SparseMatrix([[1]])
TEST_2x2 = SparseMatrix([[1, 0],
                         [0, 2]])
TEST_3x3 = SparseMatrix([[1, 0, 0],
                         [0, 2, 0],
                         [0, 0, 3]])
TEST_4x4 = SparseMatrix([[1, 0, 0, 0],
                         [0, 2, 0, 0],
                         [0, 0, 3, 0],
                         [0, 0, 0, 4]])


def test_sp_m_identity():
    # Non-integer dimension:
    with pytest.raises(TypeError) as ve:
        _ = SparseMatrix.identity(2+2j)
    assert ve.match("can't convert .* to int")

    # Negative dimension:
    with pytest.raises(AssertionError) as ae1:
        _ = SparseMatrix.identity(-1)
    assert ae1.match("Matrix dimension must be positive")

    expected1x1 = [[1]]
    i1x1 = SparseMatrix.identity(1)
    assert i1x1.get_state() == expected1x1

    expected3x3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    i3x3 = SparseMatrix.identity(3)
    assert i3x3.get_state() == expected3x3


def test_sp_m_init():
    # Test initialisation with a dict of dicts
    input1 = {0: {0: 1, 1: 1}, 1: {0: 1, 1: 1}}
    sp1 = SparseMatrix(input1)

    assert sp1.num_rows == 2
    assert sp1.num_columns == 2

    assert sp1.get_state() == [[1, 1], [1, 1]]

    # Test initialisation with a list of lists input
    input2 = [[1, 2], [3, 4]]
    sp2 = SparseMatrix(input2)

    assert sp2.num_rows == 2
    assert sp2.num_columns == 2

    assert sp2.get_state() == [[1, 2], [3, 4]]


def test_sp_m_len():
    assert TEST_1x1.num_rows == 1
    assert TEST_1x1.num_columns == 1
    assert TEST_2x2.num_rows == 2
    assert TEST_2x2.num_columns == 2
    assert TEST_3x3.num_rows == 3
    assert TEST_3x3.num_columns == 3
    assert TEST_4x4.num_rows == 4
    assert TEST_4x4.num_columns == 4


def test_sp_square():
    assert TEST_1x1.square
    assert TEST_2x2.square
    assert TEST_3x3.square
    assert TEST_4x4.square
    I: SparseMatrix = SparseMatrix.identity(10)
    assert I.square

    A = SparseMatrix({0: {10: 9}})
    assert A.square is False


def test_sp_m_get_item():
    assert TEST_1x1[0][0] == 1
    assert TEST_2x2[1][1] == 2
    assert TEST_3x3[2][2] == 3
    assert TEST_4x4[3][3] == 4

    with pytest.raises(AssertionError) as ae:
        _ = TEST_2x2[3][3]
    assert ae.match("index out of range")


def test_sp_m_set_item():
    two_by_two = deepcopy(TEST_2x2)
    with pytest.raises(AssertionError) as ae1:
        two_by_two[2] = [5, 6]
    assert ae1.match("index out of range")

    with pytest.raises(AssertionError) as ae2:
        two_by_two[0] = [1, 2, 3, 4]
    assert ae2.match("row dimension does not match")

    one_by_one = deepcopy(TEST_1x1)
    one_by_one[0] = [0]
    assert one_by_one[0][0] == 0

    two_by_two = deepcopy(TEST_2x2)
    two_by_two[1] = [5, 6]
    assert two_by_two.get_state() == [[1, 0], [5, 6]]
    assert two_by_two[1][1] == 6


def test_sp_m_get_state():
    assert TEST_1x1.get_state() == [[1]]
    assert TEST_2x2.get_state() == [[1, 0], [0, 2]]
    assert TEST_3x3.get_state() == [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
    assert TEST_4x4.get_state() == [[1, 0, 0, 0], [0, 2, 0, 0], [
        0, 0, 3, 0], [0, 0, 0, 4]]


def test_sp_m_rows():
    assert TEST_1x1.rows() == [[1]]
    assert TEST_2x2.rows() == [[1, 0], [0, 2]]


def test_sp_m_columns():
    # The test matrices are diagonal, so shouldn't expect any changes
    assert TEST_1x1.columns() == [[1]]
    assert TEST_2x2.columns() == [[1, 0], [0, 2]]
    assert TEST_3x3.columns() == [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
    assert TEST_4x4.columns() == [[1, 0, 0, 0], [0, 2, 0, 0], [
        0, 0, 3, 0], [0, 0, 0, 4]]

    A = SparseMatrix([[1, 2, 0], [0, 3, 4], [0, 0, 5]])
    assert A.columns() == [[1, 0, 0], [2, 3, 0], [0, 4, 5]]


def test_sp_m_transpose():
    A = SparseMatrix([[1], [2], [3], [4]])
    B = SparseMatrix([[1, 2, 3, 4]])

    assert A.transpose().get_state() == B.get_state()


def test_sp_m_conjugate():
    # Non-complex values shoule be unchanged.
    A = SparseMatrix([[1, 2], [3, 4]])
    assert A.conjugate().get_state() == A.get_state()

    # complex should be conjugated
    B = SparseMatrix([[1j, 0], [0, 1j]])
    C = SparseMatrix([[-1j, 0], [0, -1j]])

    assert B.conjugate().get_state() == C.get_state()


def test_d_m_adjoint():
    # Should be transposed, and conjugated
    A = SparseMatrix([[1j, 2j], [3j, 4j]])
    B = SparseMatrix([[-1j, -3j], [-2j, -4j]])

    assert A.adjoint().get_state() == B.get_state()


def test_sp_m_add():
    with pytest.raises(AssertionError) as ae:
        A = SparseMatrix([[1]])
        B = SparseMatrix([[1, 2], [3, 4]])
        A + B
    assert ae.match("Matrix dimensions must be equal for addition")

    A1x1 = SparseMatrix([[1]])
    B1x1 = SparseMatrix([[2]])
    C1x1 = SparseMatrix([[3]])

    assert (A1x1 + B1x1).get_state() == C1x1.get_state()

    A2x2 = SparseMatrix([[1, 2], [3, 4]])
    B2x2 = SparseMatrix([[5, 6], [7, 8]])
    C2x2 = SparseMatrix([[6, 8], [10, 12]])

    assert (A2x2 + B2x2).get_state() == C2x2.get_state()

    A3x3 = SparseMatrix([[0, 1, 0], [2, 0, 0], [0, 0, 3]])
    B3x3 = SparseMatrix([[4, 0, 0], [0, 5, 0], [0, 0, 6]])
    C3x3 = SparseMatrix([[4, 1, 0], [2, 5, 0], [0, 0, 9]])

    assert (A3x3 + B3x3).get_state() == C3x3.get_state()

    A1x4 = SparseMatrix([[1], [2], [3], [4]])
    B1x4 = SparseMatrix([[5], [0], [0], [6]])
    C1x4 = SparseMatrix([[6], [2], [3], [10]])

    assert (A1x4 + B1x4).get_state() == C1x4.get_state()


def test_sp_m_sub():
    A1x1 = SparseMatrix([[2]])
    B1x1 = SparseMatrix([[1]])
    C1x1 = SparseMatrix([[1]])

    assert (A1x1 - B1x1).get_state() == C1x1.get_state()

    A2x2 = SparseMatrix([[5, 6], [7, 8]])
    B2x2 = SparseMatrix([[1, 2], [3, 4]])
    C2x2 = SparseMatrix([[4, 4], [4, 4]])

    assert (A2x2 - B2x2).get_state() == C2x2.get_state()

    A1x4 = SparseMatrix([[1], [2], [3], [4]])
    B1x4 = SparseMatrix([[5], [0], [0], [6]])
    C1x4 = SparseMatrix([[-4], [2], [3], [-2]])

    assert (A1x4 - B1x4).get_state() == C1x4.get_state()


def test_sp_m_mul_scalar():
    # Testing with ints:
    A1x1_1 = SparseMatrix([[1]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = SparseMatrix([[2]])

    assert (A1x1_1 * 2).get_state() == B1x1.get_state()
    assert (2 * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = SparseMatrix([[1, 2], [3, 4]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = SparseMatrix([[3, 6], [9, 12]])

    assert (A2x2_1 * 3).get_state() == B2x2.get_state()
    assert (3 * A2x2_2).get_state() == B2x2.get_state()

    # Testing with floats:
    A1x1_1 = SparseMatrix([[1.0]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = SparseMatrix([[0.5]])

    assert (A1x1_1 * 0.5).get_state() == B1x1.get_state()
    assert (0.5 * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = SparseMatrix([[1.5, 2.5], [3.5, 4.5]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = SparseMatrix([[2.25, 3.75], [5.25, 6.75]])

    assert (A2x2_1 * 1.5).get_state() == B2x2.get_state()
    assert (1.5 * A2x2_2).get_state() == B2x2.get_state()

    # Testing with complex:
    A1x1_1 = SparseMatrix([[1]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = SparseMatrix([[1 + 0j]])

    assert (A1x1_1 * (1+0j)).get_state() == B1x1.get_state()
    assert ((1+0j) * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = SparseMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = SparseMatrix([[2 + 2j, 4 + 4j], [6 + 6j, 8 + 8j]])

    assert (A2x2_1 * 2).get_state() == B2x2.get_state()
    assert (2 * A2x2_2).get_state() == B2x2.get_state()

    C2x2_1 = SparseMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    C2x2_2 = deepcopy(C2x2_1)
    D2x2 = SparseMatrix([[4j, 8j], [12j, 16j]])

    assert (C2x2_1 * (2+2j)).get_state() == D2x2.get_state()
    assert ((2+2j) * C2x2_2).get_state() == D2x2.get_state()


def test_sp_m_mul_dot_product():
    # Test the assertions for the 1x1 case
    A1x1 = SparseMatrix([[2]])
    B1x1 = SparseMatrix([[3]])
    C1x1 = SparseMatrix([[6]])

    with pytest.raises(AssertionError) as ae2:
        A1x1 * SparseMatrix([[1, 2], [3, 4]])
    assert ae2.match("matrices don't match on their row/column dimensions")

    assert (A1x1 * B1x1).get_state() == C1x1.get_state()

    A2x2 = SparseMatrix([[1, 2], [3, 4]])
    B2x2 = SparseMatrix([[5, 6], [7, 8]])
    C2x2 = SparseMatrix([[19, 22], [43, 50]])

    assert (A2x2 * B2x2).get_state() == C2x2.get_state()

    A3x3 = SparseMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B3x3 = SparseMatrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
    C3x3 = SparseMatrix([[84, 90, 96], [201, 216, 231], [318, 342, 366]])

    assert (A3x3 * B3x3).get_state() == C3x3.get_state()

    C4x4 = SparseMatrix({0: {0: 1}, 1: {1: 4}, 2: {2: 9}, 3: {3: 16}})
    assert (TEST_4x4 * TEST_4x4).get_state() == C4x4.get_state()


def test_sp_m_column_mul():

    A = SparseMatrix([[1, 1], [1, -1]])
    B = SparseMatrix([[1], [0]])

    C = A * B

    expected = SparseMatrix([[1], [1]])

    assert C.get_state() == expected.get_state()


def test_sp_m_str():
    expected1x1 = "[  1]"
    assert str(TEST_1x1) == expected1x1

    expected2x2 = "[  1,  0]\n[  0,  2]"
    assert str(TEST_2x2) == expected2x2

    expected3x3 = "[  1,  0,  0]\n[  0,  2,  0]\n[  0,  0,  3]"
    assert str(TEST_3x3) == expected3x3

    expected1x4 = "[  0]\n[  0]\n[  0]\n[  5]"
    assert str(SparseMatrix({3: {0: 5}})) == expected1x4
