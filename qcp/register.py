#!/usr/bin/env python
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
from qcp.matrices import Matrix
import cmath
from qcp.matrices.types import VECTOR


def measure(mat: Matrix) -> VECTOR:
    """Convert the qbit states into probability amplitudes"""
    assert mat.num_columns == 1, \
        "can only measure the probabilities of column matrices"
    states = mat.get_state()

    probabilities = [s[0]**2 for s in states]

    # Normalise the probabilities if they aren't, but avoid divide by
    # 0 errors
    magnitude = sum(probabilities)
    if not cmath.isclose(magnitude, 1) and not cmath.isclose(magnitude, 0):
        probabilities = [p / magnitude for p in probabilities]

    return probabilities
