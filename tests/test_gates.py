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
from qcp.matrices import DefaultMatrix
import qcp.constants as const
import math
from qcp.matrices import SparseMatrix
import tests.test_helpers as h
import qcp.gates as gts
import pytest


def test_multi_gate():
    # Verify each of the enums:
    # HADAMARD Gate:
    had = gts.multi_gate(1, [0], gts.Gate.H)
    assert had.get_state() == const.TWO_HADAMARD.get_state()

    # PAULI-X Gate:
    pauli_x = gts.multi_gate(1, [0], gts.Gate.X)
    assert pauli_x.get_state() == const.PAULI_X.get_state()

    # PAULI-Z Gate:
    pauli_z = gts.multi_gate(1, [0], gts.Gate.Z)
    assert pauli_z.get_state() == const.PAULI_Z.get_state()

    # PHASE SHIFT Gate:
    phase = gts.multi_gate(1, [0], gts.Gate.P)
    assert phase.get_state() == gts.phase_shift(0j).get_state()

    # UNSPECIFIED/IDENTITY:
    id = gts.multi_gate(1, [0], gts.Gate.I)
    assert id.get_state() == DefaultMatrix.identity(2**1).get_state()


def test_control_x():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_x(1, [], 0)
    assert ae1.match("need minimum of two qubits")

    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_x(2, [5], 0)
    assert ae2.match("control bit out of range")

    # Target bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae3:
        gts.control_x(2, [1], 4)
    assert ae3.match("target bit out of range")

    # More control bits indexed than there are qubits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_x(2, [1, 1, 1, 1, 1, 1], 0)
    assert ae4.match("too many control bits provided")

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae5:
        gts.control_x(2, [0], 0)
    assert ae5.match("control bits and target bit cannot be the same")

    cx_4x4 = gts.control_x(2, [0], 1)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    assert cx_4x4.get_state() == expected_4x4.get_state()

    # Create a |00> + |10> qbit state:
    two_qubits = SparseMatrix({0: {0: 1}, 1: {}, 2: {0: 1}, 3: {}})

    # The first qbit should be untouched, the second should be flipped
    transformed_qbits = cx_4x4 * two_qubits
    expected_2_qbits = SparseMatrix({0: {0: 1}, 1: {}, 2: {}, 3: {0: 1}})
    assert transformed_qbits.get_state() == expected_2_qbits.get_state()

    cx_8x8 = gts.control_x(3, [1], 3)
    # | 000 >
    three_qbits = SparseMatrix({
        0: {0: 1}, 1: {}, 2: {}, 3: {},
        4: {}, 5: {}, 6: {}, 7: {}})
    transform_3qbits = cx_8x8 * three_qbits
    expected_3qbits = SparseMatrix({
        0: {0: 1}, 1: {}, 2: {}, 3: {},
        4: {}, 5: {}, 6: {}, 7: {}})

    assert transform_3qbits.get_state() == expected_3qbits.get_state()


def test_control_z():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_z(1, [], 0)
    assert ae1.match("need minimum of two qubits")

    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_z(2, [5], 0)
    assert ae2.match("control bit out of range")

    # Target bit needs to be within qubit range:
    with pytest.raises(AssertionError) as ae3:
        gts.control_z(2, [1], 4)
    assert ae3.match("target bit out of range")

    # More control bits indexed than there are qubits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_z(2, [1, 1, 1, 1, 1, 1], 0)
    assert ae4.match("too many control bits provided")

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae5:
        gts.control_z(2, [0], 0)
    assert ae5.match("control bits and target bit cannot be the same")

    cz_4x4 = gts.control_z(2, [0], 1)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])
    assert cz_4x4.get_state() == expected_4x4.get_state()


def test_control_phase():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_phase(1, [], 0, 0j)
    assert ae1.match("need minimum of two qubits")

    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_phase(2, [5], 0, 0j)
    assert ae2.match("control bit out of range")

    # Target bit needs to be within qubit range:
    with pytest.raises(AssertionError) as ae3:
        gts.control_phase(2, [1], 4, 0j)
    assert ae3.match("target bit out of range")

    # More control bits indexed than there are qubits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_phase(2, [1, 1, 1, 1, 1, 1], 0, 0j)
    assert ae4.match("too many control bits provided")

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae5:
        gts.control_phase(2, [0], 0, 0j)
    assert ae5.match("control bits and target bit cannot be the same")

    cp_4x4_0 = gts.control_phase(2, [0], 1, 0)
    expected_4x4_0 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    assert cp_4x4_0.get_state() == expected_4x4_0.get_state()

    cp_4x4_1 = gts.control_phase(2, [0], 1, math.pi / 2)
    expected_4x4_1 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1j]
    ])
    h.compare_matrices(cp_4x4_1, expected_4x4_1)

    cp_4x4_2 = gts.control_phase(2, [0], 1, math.pi)
    expected_4x4_2 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])
    h.compare_matrices(cp_4x4_2, expected_4x4_2)

    cp_4x4_3 = gts.control_phase(2, [0], 1, 3 * math.pi / 2)
    expected_4x4_3 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1j]
    ])
    h.compare_matrices(cp_4x4_3, expected_4x4_3)

    # a 2 * pi rotation should be same as a 0 rotation:
    cp_4x4_4 = gts.control_phase(2, [0], 1, 2 * math.pi)
    h.compare_matrices(cp_4x4_4, expected_4x4_0)


def test_phase_shift():
    ps1 = gts.phase_shift(0)
    ps2 = gts.phase_shift(math.pi/2)
    ps3 = gts.phase_shift(math.pi)
    ps4 = gts.phase_shift(3*math.pi/2)

    expected1 = DefaultMatrix([[1, 0], [0, 1]])
    expected2 = DefaultMatrix([[1, 0], [0, 1j]])
    expected3 = DefaultMatrix([[1, 0], [0, -1]])
    expected4 = DefaultMatrix([[1, 0], [0, -1j]])

    h.compare_matrices(ps1, expected1)
    h.compare_matrices(ps2, expected2)
    h.compare_matrices(ps3, expected3)
    h.compare_matrices(ps4, expected4)


def test_hadamard_gate():

    qubit0 = DefaultMatrix([[1], [0]])
    qubit1 = DefaultMatrix([[0], [1]])

    ans0 = const.TWO_HADAMARD * qubit0
    ans1 = const.TWO_HADAMARD * qubit1

    expected0 = (1/(math.sqrt(2))) * DefaultMatrix([[1], [1]])
    expected1 = (1/(math.sqrt(2))) * DefaultMatrix([[1], [-1]])

    assert expected0.get_state() == ans0.get_state()
    assert expected1.get_state() == ans1.get_state()
