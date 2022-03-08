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
import qcp.gates as gts
import pytest


def test_multi_gate():
    # Verify each of the enums:
    # HADAMARD Gate:
    had = gts.multi_gate(1, [0], const.Gate.H)
    assert had.get_state() == const.TWO_HADAMARD.get_state()

    # PAULI-X Gate:
    pauli_x = gts.multi_gate(1, [0], const.Gate.X)
    assert pauli_x.get_state() == const.PAULI_X.get_state()

    # PAULI-Z Gate:
    pauli_z = gts.multi_gate(1, [0], const.Gate.Z)
    assert pauli_z.get_state() == const.PAULI_Z.get_state()

    # PHASE SHIFT Gate:
    phase = gts.multi_gate(1, [0], const.Gate.P)
    assert phase.get_state() == gts.phase_shift(0j).get_state()

    # UNSPECIFIED/IDENTITY:
    id = gts.multi_gate(1, [0], const.Gate.I)
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

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_x(2, [0], 0)
    assert ae4.match("control bits and target bit cannot be the same")

    # Two qbit state has two options for the control/target position:
    # Test for 1st expected result
    cx_4x4 = gts.control_x(2, [0], 1)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    assert cx_4x4.get_state() == expected_4x4.get_state()

    # Test for second:
    cx_4x4_2 = gts.control_x(2, [1], 0)
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
        [0],  # |000>
        [1],  # |001>
        [0],  # |010>
        [0],  # |011>
        [0],  # |100>
        [0],  # |101>
        [0],  # |110>
        [0]  # |111>
    ])
    transform_3qbits = cx_8x8 * three_qbits
    expected_3qbits = SparseMatrix([
        [0],  # |000>
        [0],  # |001>
        [0],  # |010>
        [0],  # |011>
        [0],  # |100>
        [1],  # |101>
        [0],  # |110>
        [0]  # |111>
    ])

    assert transform_3qbits.get_state() == expected_3qbits.get_state()


def test_control_z():
    pass


def test_control_phase():
    pass


def test_phase_shift():
    pass
