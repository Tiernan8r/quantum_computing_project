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
import math
import tests.test_helpers as h
import qcp.gates as gts


def test_multi_gate():
    pass


def test_control_x():
    pass


def test_control_z():
    pass


def test_control_phase():
    pass


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
