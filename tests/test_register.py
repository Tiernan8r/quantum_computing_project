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
import pytest
from qcp.matrices import DefaultMatrix
import qcp.register as reg
import math


def test_measure():
    # Test non-column matrix
    A = DefaultMatrix([[1, 2], [3, 4]])

    with pytest.raises(AssertionError) as ae:
        _ = reg.measure(A)
    assert ae.match("can only measure the probabilities of column matrices")

    # Make sure divide by 0 error not raised
    Z = DefaultMatrix([[0], [0], [0], [0]])
    try:
        _ = reg.measure(Z)
    except ZeroDivisionError as zde:
        assert False, "expected no ZeroDivisionError"

    # Test probabilities come out as expected
    factor = 1 / math.sqrt(2)
    B = factor * DefaultMatrix([[1], [1]])
    prob = reg.measure(B)
    assert math.isclose(prob[0], 0.5)

    # Test normalisation works 
    C = DefaultMatrix([[1],[1]])
    prob2 = reg.measure(C)
    assert math.isclose(prob2[0], 0.5)