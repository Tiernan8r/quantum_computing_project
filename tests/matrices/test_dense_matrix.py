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
from qcp.matrices import DenseMatrix
import pytest


TEST_1x1 = DenseMatrix([[1]])
TEST_2x2 = DenseMatrix([[1, 2],
                        [3, 4]])
TEST_3x3 = DenseMatrix([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]])


def test_d_m_identity():
    # Non-integer dimension:
    with pytest.raises(AssertionError) as ae1:
        _ = DenseMatrix.identity(2+2j)
    assert ae1.match("must provide integer dimension")

    # Negative dimension:
    with pytest.raises(AssertionError) as ae2:
        _ = DenseMatrix.identity(-1)
    assert ae2.match("Matrix dimension must be positive")

    expected1x1 = [[1]]
    i1x1 = DenseMatrix.identity(1)
    assert i1x1.get_state() == expected1x1

    expected3x3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    i3x3 = DenseMatrix.identity(3)
    assert i3x3.get_state() == expected3x3


def test_d_m_init():
    input1 = []
    with pytest.raises(AssertionError) as ae1:
        _ = DenseMatrix(input1)
    assert ae1.match("attempting to initialise matrix with no dimensions")

    input2 = [[1], [2, 3]]
    with pytest.raises(AssertionError) as ae2:
        _ = DenseMatrix(input2)
    assert ae2.match("attempting to initialise non-square matrix.")

    test_input_types = [
        [[1]],
        [[2.0]],
        [[3+3j]]
    ]
    for inp in test_input_types:
        sqm = DenseMatrix(inp)
        assert sqm.get_state() == inp


def test_d_m_len():
    assert len(TEST_1x1) == 1
    assert len(TEST_2x2) == 2
    assert len(TEST_3x3) == 3


def test_d_m_get_item():
    assert TEST_1x1[0][0] == 1
    assert TEST_2x2[1][1] == 4
    assert TEST_3x3[2][2] == 9

    with pytest.raises(AssertionError) as ae:
        _ = TEST_2x2[3][3]
    assert ae.match("index out of range")


def test_d_m_set_item():
    one_by_one = deepcopy(TEST_1x1)
    one_by_one[0] = [0]
    assert one_by_one[0][0] == 0

    two_by_two = deepcopy(TEST_2x2)
    two_by_two[1] = [5, 6]
    assert two_by_two[1][1] == 6

    with pytest.raises(AssertionError) as ae1:
        two_by_two[2] = [5, 6]
    assert ae1.match("index out of range")

    with pytest.raises(AssertionError) as ae2:
        two_by_two[0] = [1, 2, 3, 4]
    assert ae2.match("row dimension does not match")


def test_d_m_get_state():
    assert TEST_1x1.get_state() == [[1]]
    assert TEST_2x2.get_state() == [[1, 2], [3, 4]]


def test_d_m_zeros():
    A = DenseMatrix.zeros(2, 3)
    expected = DenseMatrix([[0 for _ in range(3)] for _ in range(2)])

    assert A.get_state() == expected.get_state()


def test_d_m_rows():
    assert TEST_1x1.rows() == [[1]]
    assert TEST_2x2.rows() == [[1, 2], [3, 4]]


def test_d_m_columns():
    assert TEST_1x1.columns() == [[1]]
    assert TEST_2x2.columns() == [[1, 3], [2, 4]]
    assert TEST_3x3.columns() == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]


def test_d_m_iter():
    build_1x1 = []
    for r1 in TEST_1x1:
        build_1x1.append(r1)
    expected_1x1 = [[1]]

    assert build_1x1 == expected_1x1

    build_2x2 = []
    for r2 in TEST_2x2:
        build_2x2.append(r2)
    expected_2x2 = [[1, 2], [3, 4]]

    assert build_2x2 == expected_2x2

    build_3x3 = []
    for r3 in TEST_3x3:
        build_3x3.append(r3)
    expected_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    assert build_3x3 == expected_3x3


def test_d_m_add():
    A1x1 = DenseMatrix([[1]])
    B1x1 = DenseMatrix([[2]])
    C1x1 = DenseMatrix([[3]])

    assert (A1x1 + B1x1).get_state() == C1x1.get_state()

    A2x2 = DenseMatrix([[1, 2], [3, 4]])
    B2x2 = DenseMatrix([[5, 6], [7, 8]])
    C2x2 = DenseMatrix([[6, 8], [10, 12]])

    assert (A2x2 + B2x2).get_state() == C2x2.get_state()


def test_d_m_sub():
    A1x1 = DenseMatrix([[2]])
    B1x1 = DenseMatrix([[1]])
    C1x1 = DenseMatrix([[1]])

    assert (A1x1 - B1x1).get_state() == C1x1.get_state()

    A2x2 = DenseMatrix([[5, 6], [7, 8]])
    B2x2 = DenseMatrix([[1, 2], [3, 4]])
    C2x2 = DenseMatrix([[4, 4], [4, 4]])

    assert (A2x2 - B2x2).get_state() == C2x2.get_state()


def test_d_m_mul_scalar():
    # Testing with ints:
    A1x1_1 = DenseMatrix([[1]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = DenseMatrix([[2]])

    assert (A1x1_1 * 2).get_state() == B1x1.get_state()
    assert (2 * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = DenseMatrix([[1, 2], [3, 4]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = DenseMatrix([[3, 6], [9, 12]])

    assert (A2x2_1 * 3).get_state() == B2x2.get_state()
    assert (3 * A2x2_2).get_state() == B2x2.get_state()

    # Testing with floats:
    A1x1_1 = DenseMatrix([[1.0]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = DenseMatrix([[0.5]])

    assert (A1x1_1 * 0.5).get_state() == B1x1.get_state()
    assert (0.5 * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = DenseMatrix([[1.5, 2.5], [3.5, 4.5]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = DenseMatrix([[2.25, 3.75], [5.25, 6.75]])

    assert (A2x2_1 * 1.5).get_state() == B2x2.get_state()
    assert (1.5 * A2x2_2).get_state() == B2x2.get_state()

    # Testing with complex:
    A1x1_1 = DenseMatrix([[1]])
    A1x1_2 = deepcopy(A1x1_1)
    B1x1 = DenseMatrix([[1 + 0j]])

    assert (A1x1_1 * (1+0j)).get_state() == B1x1.get_state()
    assert ((1+0j) * A1x1_2).get_state() == B1x1.get_state()

    A2x2_1 = DenseMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    A2x2_2 = deepcopy(A2x2_1)
    B2x2 = DenseMatrix([[2 + 2j, 4 + 4j], [6 + 6j, 8 + 8j]])

    assert (A2x2_1 * 2).get_state() == B2x2.get_state()
    assert (2 * A2x2_2).get_state() == B2x2.get_state()

    C2x2_1 = DenseMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    C2x2_2 = deepcopy(C2x2_1)
    D2x2 = DenseMatrix([[4j, 8j], [12j, 16j]])

    assert (C2x2_1 * (2+2j)).get_state() == D2x2.get_state()
    assert ((2+2j) * C2x2_2).get_state() == D2x2.get_state()


def test_d_m_mul_dot_product():
    # Test the assertions for the 1x1 case
    A1x1 = DenseMatrix([[2]])
    B1x1 = DenseMatrix([[3]])
    C1x1 = DenseMatrix([[6]])

    with pytest.raises(AssertionError) as ae2:
        A1x1 * DenseMatrix([[1, 2], [3, 4]])
    assert ae2.match("matrices don't match on their row/column dimensions")

    assert (A1x1 * B1x1).get_state() == C1x1.get_state()

    A2x2 = DenseMatrix([[1, 2], [3, 4]])
    B2x2 = DenseMatrix([[5, 6], [7, 8]])
    C2x2 = DenseMatrix([[19, 22], [43, 50]])

    assert (A2x2 * B2x2).get_state() == C2x2.get_state()

    A3x3 = DenseMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B3x3 = DenseMatrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
    C3x3 = DenseMatrix([[84, 90, 96], [201, 216, 231], [318, 342, 366]])

    assert (A3x3 * B3x3).get_state() == C3x3.get_state()


def test_d_m_str():
    expected1x1 = "[  1]"
    assert str(TEST_1x1) == expected1x1

    expected2x2 = "[  1,  2]\n[  3,  4]"
    assert str(TEST_2x2) == expected2x2

    expected3x3 = "[  1,  2,  3]\n[  4,  5,  6]\n[  7,  8,  9]"
    assert str(TEST_3x3) == expected3x3


def test_d_m_transpose():
    A = DenseMatrix([[1], [2], [3], [4]])
    B = DenseMatrix([[1, 2, 3, 4]])

    assert A.transpose().get_state() == B.get_state()


