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
import math

from qcp.matrices import DefaultMatrix

#: The 2x2 Identity Matrix
IDENTITY = DefaultMatrix([[1, 0], [0, 1]])
#: The 2x2 Hadamard Gate
TWO_HADAMARD = (1/math.sqrt(2)) * DefaultMatrix([[1, 1], [1, -1]])
#: A Column Vector representing the |0> state
ZERO_VECTOR = DefaultMatrix([[1], [0]])
#: A Column Vector representing the |1> state
ONE_VECTOR = DefaultMatrix([[0], [1]])
#: The 2x2 Pauli-X Gate
PAULI_X = DefaultMatrix([[0, 1], [1, 0]])
#: The 2x2 Pauli-Z Gate
PAULI_Z = DefaultMatrix([[1, 0], [0, -1]])

#: CLI flag values:
HELP_SHORT = "-h"
HELP_LONG = "--help"
ALGORITHM_SHORT = "-a"
ALGORITHM_LONG = "--algorithm"
TARGET_SHORT = "-t"
TARGET_LONG = "--target"
UNITARY_SHORT = "-u"
UNITARY_LONG = "--unitary"
PHASE_SHORT = "-p"
PHASE_LONG = "--phase"

#: All the flags accepted by the CLI, mapping their short name to
#: the more verbose one
FLAG_MAPPING = {
    HELP_SHORT: HELP_LONG,
    ALGORITHM_SHORT: ALGORITHM_LONG,
    TARGET_SHORT: TARGET_LONG,
    UNITARY_SHORT: UNITARY_LONG,
    PHASE_SHORT: PHASE_LONG
}
