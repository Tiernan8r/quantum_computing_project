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
from urllib.request import build_opener
from qcp.matrices import SquareMatrix
import pytest


IDENTITY = SquareMatrix([[1, 0], [0, 1]])
TEST_ONE_BY_ONE = SquareMatrix([[1]])
TEST_TWO_BY_TWO = SquareMatrix([[1, 2], [3, 4]])
TEST_THREE_BY_THREE = SquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_sq_m_init():
    input1 = []
    with pytest.raises(AssertionError) as ae1:
        _ = SquareMatrix(input1)
    assert ae1.match("attempting to initialise matrix with no dimensions")

    input2 = [[1], [2, 3]]
    with pytest.raises(AssertionError) as ae2:
        _ = SquareMatrix(input2)
    assert ae2.match("attempting to initialise non-square matrix.")

    test_input_types = [
        [[1]],
        [[2.0]],
        [[3+3j]]
    ]
    for inp in test_input_types:
        sqm = SquareMatrix(inp)
        assert sqm.get_state() == inp



def test_sq_m_len():
    assert len(TEST_ONE_BY_ONE) == 1
    assert len(TEST_TWO_BY_TWO) == 2
    assert len(TEST_THREE_BY_THREE) == 3


def test_sq_m_get_item():
    assert TEST_ONE_BY_ONE[0][0] == 1
    assert TEST_TWO_BY_TWO[1][1] == 4
    assert TEST_THREE_BY_THREE[2][2] == 9

    with pytest.raises(AssertionError) as ae:
        _ = TEST_TWO_BY_TWO[3][3]
    assert ae.match("index out of range")


def test_sq_m_set_item():
    one_by_one = deepcopy(TEST_ONE_BY_ONE)
    one_by_one[0] = [0]
    assert one_by_one[0][0] == 0

    two_by_two = deepcopy(TEST_TWO_BY_TWO)
    two_by_two[1] = [5, 6]
    assert two_by_two[1][1] == 6

    with pytest.raises(AssertionError) as ae1:
        two_by_two[2] = [5, 6]
    assert ae1.match("index out of range")

    with pytest.raises(AssertionError) as ae2:
        two_by_two[0] = [1, 2, 3, 4]
    assert ae2.match("row dimension does not match")


def test_sq_m_get_state():
    assert TEST_ONE_BY_ONE.get_state() == [[1]]
    assert TEST_TWO_BY_TWO.get_state() == [[1, 2], [3, 4]]


def test_sq_m_set_state():
    one_by_one = deepcopy(TEST_ONE_BY_ONE)

    with pytest.raises(AssertionError) as ae1:
        one_by_one.set_state(None)
    with pytest.raises(AssertionError) as ae2:
        one_by_one.set_state([])

    with pytest.raises(AssertionError) as ae3:
        one_by_one.set_state([[1], [2, 3]])
    assert ae3.match("non square matrix")

    one_by_one.set_state([[1, 2], [3, 4]])
    assert one_by_one.get_state() == [[1, 2], [3, 4]]


def test_sq_m_rows():
    assert TEST_ONE_BY_ONE.rows() == [[1]]
    assert TEST_TWO_BY_TWO.rows() == [[1, 2], [3, 4]]


def test_sq_m_columns():
    assert TEST_ONE_BY_ONE.columns() == [[1]]
    assert TEST_TWO_BY_TWO.columns() == [[1, 3], [2, 4]]
    assert TEST_THREE_BY_THREE.columns() == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]


def test_sq_m_iter():
    build_1x1 = []
    for r1 in TEST_ONE_BY_ONE:
        build_1x1.append(r1)
    expected_1x1 = [[1]]

    assert build_1x1 == expected_1x1

    build_2x2 = []
    for r2 in TEST_TWO_BY_TWO:
        build_2x2.append(r2)
    expected_2x2 = [[1, 2], [3, 4]]

    assert build_2x2 == expected_2x2

    build_3x3 = []
    for r3 in TEST_THREE_BY_THREE:
        build_3x3.append(r3)
    expected_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    assert build_3x3 == expected_3x3


def test_sq_m_add():
    A1x1 = SquareMatrix([[1]])
    B1x1 = SquareMatrix([[2]])
    C1x1 = SquareMatrix([[3]])

    assert (A1x1 + B1x1).get_state() == C1x1.get_state()

    A2x2 = SquareMatrix([[1, 2], [3, 4]])
    B2x2 = SquareMatrix([[5, 6], [7, 8]])
    C2x2 = SquareMatrix([[6, 8], [10, 12]])

    assert (A2x2 + B2x2).get_state() == C2x2.get_state()


def test_sq_m_sub():
    A1x1 = SquareMatrix([[2]])
    B1x1 = SquareMatrix([[1]])
    C1x1 = SquareMatrix([[1]])

    assert (A1x1 - B1x1).get_state() == C1x1.get_state()

    A2x2 = SquareMatrix([[5, 6], [7, 8]])
    B2x2 = SquareMatrix([[1, 2], [3, 4]])
    C2x2 = SquareMatrix([[4, 4], [4, 4]])

    assert (A2x2 - B2x2).get_state() == C2x2.get_state()


def test_sq_m_mul_scalar():
    # Testing with ints:
    A1x1 = SquareMatrix([[1]])
    B1x1 = SquareMatrix([[2]])

    assert (A1x1 * 2).get_state() == B1x1.get_state()

    A2x2 = SquareMatrix([[1, 2], [3, 4]])
    B2x2 = SquareMatrix([[3, 6], [9, 12]])

    assert (A2x2 * 3).get_state() == B2x2.get_state()

    # Testing with floats:
    A1x1 = SquareMatrix([[1.0]])
    B1x1 = SquareMatrix([[0.5]])

    assert (A1x1 * 0.5).get_state() == B1x1.get_state()

    A2x2 = SquareMatrix([[1.5, 2.5], [3.5, 4.5]])
    B2x2 = SquareMatrix([[2.25, 3.75], [5.25, 6.75]])

    assert (A2x2 * 1.5).get_state() == B2x2.get_state()

    # Testing with complex:
    A1x1 = SquareMatrix([[1]])
    B1x1 = SquareMatrix([[1 + 0j]])

    assert (A1x1 * (1+0j)).get_state() == B1x1.get_state()

    A2x2 = SquareMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    B2x2 = SquareMatrix([[2 + 2j, 4 + 4j], [6 + 6j, 8 + 8j]])

    assert (A2x2 * 2).get_state() == B2x2.get_state()

    C2x2 = SquareMatrix([[1 + 1j, 2 + 2j], [3 + 3j, 4 + 4j]])
    D2x2 = SquareMatrix([[4j, 8j], [12j, 16j]])

    assert (C2x2 * (2+2j)).get_state() == D2x2.get_state()


def test_sq_m_mul_dot_product():
    # Test the assertions for the 1x1 case
    A1x1 = SquareMatrix([[2]])
    B1x1 = SquareMatrix([[3]])
    C1x1 = SquareMatrix([[6]])

    with pytest.raises(AssertionError) as ae2:
        A1x1 * SquareMatrix([[1, 2],[3, 4]])
    assert ae2.match("matrices don't match on their row/column dimensions")

    assert (A1x1 * B1x1).get_state() == C1x1.get_state()

    A2x2 = SquareMatrix([[1, 2], [3, 4]])
    B2x2 = SquareMatrix([[5, 6], [7, 8]])
    C2x2 = SquareMatrix([[19, 22], [43, 50]])

    assert (A2x2 * B2x2).get_state() == C2x2.get_state()

    A3x3 = SquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B3x3 = SquareMatrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
    C3x3 = SquareMatrix([[84, 90, 96], [201, 216, 231], [318, 342, 366]])

    assert (A3x3 * B3x3).get_state() == C3x3.get_state()

def test_sq_m_str():
    expected1x1 = "[ 1]"
    assert str(TEST_ONE_BY_ONE) == expected1x1

    expected2x2 = "[ 1, 2]\n[ 3, 4]"
    assert str(TEST_TWO_BY_TWO) == expected2x2

    expected3x3 = "[ 1, 2, 3]\n[ 4, 5, 6]\n[ 7, 8, 9]"
    assert str(TEST_THREE_BY_THREE) == expected3x3