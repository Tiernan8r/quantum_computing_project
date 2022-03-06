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
from qcp.matrices import SparseMatrix
import math
import tests.test_helpers as h
import qcp.gates as gts
import pytest


def test_multi_gate():
    pass


def test_control_x():
    pass


def test_control_z():
    pass


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
    pass
