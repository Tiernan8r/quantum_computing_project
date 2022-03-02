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
import qcp.gates as gts
import pytest


def test_multi_gate():
    pass


def test_control_x():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_x(1, [], 0)
    assert ae1.match("need minimum of two qubits")

    # Target qbit needs to be not one of the control bits:
    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_x(2, [5], 0)
    assert ae2.match("control bit out of range")

    # More control bits indexed than there are qubits:
    with pytest.raises(AssertionError) as ae3:
        gts.control_x(2, [1, 1, 1, 1, 1, 1], 0)
    assert ae3.match("too many control bits provided")

        gts.control_x(2, [0], 0)
    assert ae2.match("control bits and target bit cannot be the same")


def test_control_z():
    pass


def test_control_phase():
    pass


def test_phase_shift():
    pass
