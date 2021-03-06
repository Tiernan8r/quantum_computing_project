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
from qcp.matrices import DefaultMatrix, SparseMatrix
import qcp.constants as const
import math
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

    # Test for a two hadamard system applied to the first qbit and third qbit
    # but not the second
    # Using the info from the lecture notes, compare this composite gate
    # applied to a 3 qbit system to what is expected according to the notes.
    h_gate = gts.multi_gate(3, [0, 2], gts.Gate.H)
    qbit_initial_state = DefaultMatrix([
        [1],  # |000>
        [0],  # |001>
        [0],  # |010>
        [0],  # |011>
        [0],  # |100>
        [0],  # |101>
        [0],  # |110>
        [0]  # |111>
    ])
    applied_state = h_gate * qbit_initial_state
    expected_qbit_state = 0.5 * DefaultMatrix([
        [1],  # |000>
        [1],  # |001>
        [0],  # |010>
        [0],  # |011>
        [1],  # |100>
        [1],  # |101>
        [0],  # |110>
        [0]  # |111>
    ])

    h.compare_matrices(applied_state, expected_qbit_state)


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

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_x(2, [0], 0)
    assert ae4.match("control bits and target bit cannot be the same")

    # Two qbit state has two options for the control/target position:
    # Test for 1st expected result
    cx_4x4 = gts.control_x(2, [1], 0)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    assert cx_4x4.get_state() == expected_4x4.get_state()

    # Test for second:
    cx_4x4_2 = gts.control_x(2, [0], 1)
    expected_4x4_2 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0]
    ])
    assert cx_4x4_2.get_state() == expected_4x4_2.get_state()

    # Create a |00> + |10> qbit state (non-normalised as that doesn't matter
    # for tests):
    two_qubits = SparseMatrix([
        [1],  # |00>
        [0],  # |01>
        [1],  # |10>
        [0]  # |11>
    ])

    # The first qbit should be untouched, the second should be flipped
    transformed_qbits = cx_4x4 * two_qubits
    expected_2_qbits = SparseMatrix([
        [1],  # |00>
        [0],  # |01>
        [0],  # |10>
        [1]  # |11>
    ])
    assert transformed_qbits.get_state() == expected_2_qbits.get_state()

    cx_8x8 = gts.control_x(3, [1], 0)
    # Set the 3 qbit state to initially be in |001> state
    three_qbits = SparseMatrix([
        [1],  # |000>
        [2],  # |001>
        [3],  # |010>
        [4],  # |011>
        [5],  # |100>
        [6],  # |101>
        [7],  # |110>
        [8]  # |111>
    ])
    transform_3qbits = cx_8x8 * three_qbits
    expected_3qbits = SparseMatrix([
        [1],  # |000>
        [2],  # |001>
        [4],  # |010>
        [3],  # |011>
        [5],  # |100>
        [6],  # |101>
        [8],  # |110>
        [7]  # |111>
    ])

    assert transform_3qbits.get_state() == expected_3qbits.get_state()

    # Test for multiple controls:
    cx_8x8_2 = gts.control_x(3, [1, 2], 0)
    transform_3qbits_2 = cx_8x8_2 * three_qbits
    expected_3qbits_2 = SparseMatrix([
        [1],  # |000>
        [2],  # |001>
        [3],  # |010>
        [4],  # |011>
        [5],  # |100>
        [6],  # |101>
        [8],  # |110>
        [7]  # |111>
    ])

    assert transform_3qbits_2.get_state() == expected_3qbits_2.get_state()


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

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_z(2, [0], 0)
    assert ae4.match("control bits and target bit cannot be the same")

    # Two qbit state has two options for the control/target position:
    # Test for 1st expected result
    cz_4x4 = gts.control_z(2, [0], 1)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])
    assert cz_4x4.get_state() == expected_4x4.get_state()

    # Test for second:
    # According to "Quantum Computation & Quantum Information"
    # Nielsen & Chuang p179 Ex4.18, should be the same as before
    cz_4x4_2 = gts.control_z(2, [1], 0)
    expected_4x4_2 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])
    assert cz_4x4_2.get_state() == expected_4x4_2.get_state()


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

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_phase(2, [0], 0, 0j)
    assert ae4.match("control bits and target bit cannot be the same")

    cp_4x4_0 = gts.control_phase(2, [0], 1, 0)
    expected_4x4_0 = SparseMatrix([
        [1, 0, 0, 0],  # |00>
        [0, 1, 0, 0],  # |01>
        [0, 0, 1, 0],  # |10>
        [0, 0, 0, 1]  # |11>
    ])
    assert cp_4x4_0.get_state() == expected_4x4_0.get_state()

    cp_4x4_1 = gts.control_phase(2, [0], 1, math.pi / 2)
    expected_4x4_1 = SparseMatrix([
        [1, 0, 0, 0],  # |00>
        [0, 1, 0, 0],  # |01>
        [0, 0, 1, 0],  # |10>
        [0, 0, 0, 1j]  # |11>
    ])
    h.compare_matrices(cp_4x4_1, expected_4x4_1)

    cp_4x4_2 = gts.control_phase(2, [0], 1, math.pi)
    expected_4x4_2 = SparseMatrix([
        [1, 0, 0, 0],  # |00>
        [0, 1, 0, 0],  # |01>
        [0, 0, 1, 0],  # |10>
        [0, 0, 0, -1]  # |11>
    ])
    h.compare_matrices(cp_4x4_2, expected_4x4_2)

    cp_4x4_3 = gts.control_phase(2, [0], 1, 3 * math.pi / 2)
    expected_4x4_3 = SparseMatrix([
        [1, 0, 0, 0],  # |00>
        [0, 1, 0, 0],  # |01>
        [0, 0, 1, 0],  # |10>
        [0, 0, 0, -1j]  # |11>
    ])
    h.compare_matrices(cp_4x4_3, expected_4x4_3)

    # a 2 * pi rotation should be same as a 0 rotation:
    cp_4x4_4 = gts.control_phase(2, [0], 1, 2 * math.pi)
    h.compare_matrices(cp_4x4_4, expected_4x4_0)

    cp_8x8 = gts.control_phase(3, [0], 1, math.pi)
    expected_8x8 = SparseMatrix([
        [1, 0, 0, 0, 0, 0, 0, 0],  # |000>
        [0, 1, 0, 0, 0, 0, 0, 0],  # |001>
        [0, 0, 1, 0, 0, 0, 0, 0],  # |010>
        [0, 0, 0, -1, 0, 0, 0, 0],  # |011>
        [0, 0, 0, 0, 1, 0, 0, 0],  # |100>
        [0, 0, 0, 0, 0, 1, 0, 0],  # |101>
        [0, 0, 0, 0, 0, 0, 1, 0],  # |110>
        [0, 0, 0, 0, 0, 0, 0, -1]  # |111>
    ])
    h.compare_matrices(cp_8x8, expected_8x8)


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


def test_swap():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.swap(1, 0, 1)
    assert ae1.match("need minimum of two qbits")

    # Targets cannot be the same
    with pytest.raises(AssertionError) as ae2:
        gts.swap(2, 0, 0)
    assert ae2.match("swap targets must be different")

    # Target bits needs to be within qubit range:
    with pytest.raises(AssertionError) as ae3:
        gts.swap(2, 4, 0)
    assert ae3.match("first target bit out of range")

    # Target bits needs to be within qubit range:
    with pytest.raises(AssertionError) as ae4:
        gts.swap(2, 0, 4)
    assert ae4.match("second target bit out of range")

    swp_4x4_1 = gts.swap(2, 0, 1)
    expected_4x4 = DefaultMatrix([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    assert swp_4x4_1.get_state() == expected_4x4.get_state()

    # Target bit order shouldn't matter
    swp_4x4_2 = gts.swap(2, 1, 0)
    assert swp_4x4_2.get_state() == expected_4x4.get_state()

    # Verify the gate swaps the bits as expected:
    two_qubits = DefaultMatrix([
        [1],  # |00>
        [2],  # |01>
        [3],  # |10>
        [4]  # |11>
    ])

    transformed_two_qbits = swp_4x4_1 * two_qubits
    expected_transform = DefaultMatrix([
        [1],  # |00>
        [3],  # |01>
        [2],  # |10>
        [4]  # |11>
    ])
    assert transformed_two_qbits.get_state() == expected_transform.get_state()

    swp_8x8 = gts.swap(3, 0, 1)
    three_qbits = DefaultMatrix([
        [1],  # |000>
        [2],  # |001>
        [3],  # |010>
        [4],  # |011>
        [5],  # |100>
        [6],  # |101>
        [7],  # |110>
        [8]  # |111>
    ])
    transform_3qbits = swp_8x8 * three_qbits
    expected_3qbits = DefaultMatrix([
        [1],  # |000>
        [2],  # |001>
        [5],  # |010>
        [6],  # |011>
        [3],  # |100>
        [4],  # |101>
        [7],  # |110>
        [8]  # |111>
    ])

    assert transform_3qbits.get_state() == expected_3qbits.get_state()


def test_control_u():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_u(1, 0, None)
    assert ae1.match("need minimum of two qubits")

    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_u(2, 2, None)
    assert ae2.match("control bit out of range")

    U = DefaultMatrix([
        [2, 3],
        [4, 5]
    ])
    # Use on too small of a control gate
    with pytest.raises(AssertionError) as ae3:
        gts.control_u(2, 0, U)
    assert ae3.match("unitary matrix too big")

    # Create a simple 4x4 CU gate:
    u = DefaultMatrix([[2]])
    cu_4x4_1 = gts.control_u(2, 0, u)
    expected_4x4_1 = DefaultMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 2]
    ])
    assert cu_4x4_1.get_state() == expected_4x4_1.get_state()

    cu_4x4_2 = gts.control_u(2, 1, u)
    expected_4x4_2 = DefaultMatrix([
        [1, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 2]
    ])
    assert cu_4x4_2.get_state() == expected_4x4_2.get_state()

    cu_8x8 = gts.control_u(3, 0, U)
    expected_8x8 = DefaultMatrix([
        [1,  0,  0,  0,  0,  0,  0,  0],
        [0,  1,  0,  0,  0,  0,  0,  0],
        [0,  0,  2,  0,  0,  0,  3,  0],
        [0,  0,  0,  2,  0,  0,  0,  3],
        [0,  0,  0,  0,  1,  0,  0,  0],
        [0,  0,  0,  0,  0,  1,  0,  0],
        [0,  0,  4,  0,  0,  0,  5,  0],
        [0,  0,  0,  4,  0,  0,  0,  5]
    ])

    assert cu_8x8.get_state() == expected_8x8.get_state()
