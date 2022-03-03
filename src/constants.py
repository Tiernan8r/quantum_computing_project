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
from src.matrices import DefaultMatrix
import math

IDENTITY = DefaultMatrix([[1, 0], [0, 1]])
TWO_HADAMARD = DefaultMatrix([[1, 1], [1, -1]]) * (1/math.sqrt(2))
ZERO_VECTOR = DefaultMatrix([[1], [0]])
ONE_VECTOR = DefaultMatrix([[0], [1]])
PAULI_X = DefaultMatrix([[0, 1], [1, 0]])
PAULI_Z = DefaultMatrix([[1, 0], [0, -1]])
