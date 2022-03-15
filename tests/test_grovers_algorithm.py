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
import qcp.grovers_algorithm as ga
import pytest


def test_pull_set_bits():
    # Create a list of tuples to test on
    # The first entry is the value to input into pull_set_bits()
    # The second entry is the expected list of indices
    test_table = [
        (1, [0]),
        (7, [0, 1, 2]),
        (10, [1, 3]),
        (21, [0, 2, 4]),
        (31, [0, 1, 2, 3, 4]),
        (32, [5])
    ]

    for tests in test_table:
        n = tests[0]
        expec = tests[1]
        assert ga.pull_set_bits(n) == expec


def test_init():
    # Test for one qbit state assertion error:
    with pytest.raises(AssertionError) as ae1:
        _ = ga.Grovers(1, 0)
    assert ae1.match("need minimum of two qbits")

    # Target out of range
    with pytest.raises(AssertionError) as ae2:
        _ = ga.Grovers(2, 10)
    assert ae2.match("target must be within qbit state indices")

    # Succeed:
    grov = ga.Grovers(2, 0)
    assert grov.size == 2

def test_initial_state():
    pass


def test_single_target_oracle():
    pass


def test_diffusion():
    pass


def test_construct_circuit():
    pass


def test_run():
    pass


def test_measure():
    pass
