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
"""
Code that converts a given column vector to the probability distributions of
observing the qbits in each state
"""
from qcp.matrices import Matrix
import cmath
from typing import List

from qcp.matrices.types import SCALARS


def measure(mat: Matrix) -> List[float]:
    """
    Convert the qbit states into probability amplitudes

    :param Matrix mat: the column vector of qbit states to measure.
    returns:
        List[float]: list of probabilities of observing the qbits in each
        state, normalised to total probability of 1.
    """
    assert mat.num_columns == 1, \
        "can only measure the probabilities of column matrices"
    states = mat.get_state()

    probabilities = [_magnitude(s[0]) for s in states]

    # Normalise the probabilities if they aren't, but avoid divide by
    # 0 errors
    magnitude = sum(probabilities)
    if not cmath.isclose(magnitude, 1) and not cmath.isclose(magnitude, 0):
        probabilities = [p / magnitude for p in probabilities]

    return probabilities


def _magnitude(v: SCALARS) -> float:
    """
    Measure the probability magnitude of the given scalar in the
    usual Quantum Mechanical way.

    :param SCALARS v: The value to determine the magnitude of.
    returns:
        float: The magnitude of the scalar
    """
    if isinstance(v, complex):
        return (v * v.conjugate()).real
    else:
        return v**2
