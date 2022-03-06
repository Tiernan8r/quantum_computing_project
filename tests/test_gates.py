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
import qcp.gates as gts


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
    pass


def test_control_z():
    pass


def test_control_phase():
    pass


def test_phase_shift():
    pass
