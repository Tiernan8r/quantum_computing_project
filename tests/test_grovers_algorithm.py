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
from qcp.matrices import DefaultMatrix
import tests.test_helpers as h
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
    # Create initial small grovers algorithm, so the test code doesn't take
    # a while computing large circuits and oracles
    grov = ga.Grovers(2, 0)

    expected4x1 = DefaultMatrix([[1],
                                 [0],
                                 [0],
                                 [0]])
    initial4x1 = grov.initial_state()
    assert initial4x1.get_state() == expected4x1.get_state()

    # Increase the algorithms size, so that larger initial states
    # will be generated
    grov.size = 4
    expected16x1 = DefaultMatrix([[1],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0],
                                 [0]])
    initial16x1 = grov.initial_state()
    assert initial16x1.get_state() == expected16x1.get_state()


def test_single_target_oracle():
    # Create initial small grovers algorithm, so the test code doesn't take
    # a while computing large circuits and oracles
    grov = ga.Grovers(2, 0)

    # iterate over all target possibilities for a 2 qbit system,
    # and verify that the target oracle is generated correctly
    # for each target
    for t in range(0, 4):
        # set the new target
        grov.target = t
        # generate the new target for the state
        oracle4x4 = grov.single_target_oracle()
        # the target index should be -1 in the oracle
        expected4x4 = DefaultMatrix({
            0: {0: 1},
            1: {1: 1},
            2: {2: 1},
            3: {3: 1},
        })
        expected4x4[t][t] = -1

        assert oracle4x4.get_state() == expected4x4.get_state()

    # Test for 8x8 matrices
    grov.size = 3
    grov.target = 0
    oracle8x8 = grov.single_target_oracle()

    expected8x8 = DefaultMatrix.identity(8)
    expected8x8[0][0] = -1

    assert oracle8x8.get_state() == expected8x8.get_state()


def test_diffusion():
    # Create initial small grovers algorithm, so the test code doesn't take
    # a while computing large circuits and oracles
    grov = ga.Grovers(2, 0)

    # The diffuser is independent of the target:
    expected4x4 = 0.5 * DefaultMatrix([[1, -1, -1, -1],
                                       [-1, 1, -1, -1],
                                       [-1, -1, 1, -1],
                                       [-1, -1, -1, 1]])
    for t in range(4):
        grov.target = t
        diff4x4 = grov.diffusion()
        assert diff4x4 == expected4x4

    # Test for 8x8 states
    grov.size = 3
    diff8x8 = grov.diffusion()
    basic_state = [[-1 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        basic_state[i][i] = 3
    expected8x8 = 0.25 * DefaultMatrix(basic_state)

    h.compare_matrices(diff8x8, expected8x8)


def test_construct_circuit():
    # Create initial small grovers algorithm, so the test code doesn't take
    # a while computing large circuits and oracles
    grov = ga.Grovers(2, 0)

    circ4x4 = grov.construct_circuit()
    expected4x4 = 0.5 * DefaultMatrix([
        [1, 1, 1, 1],
        [1, -1, 1, -1],
        [1, 1, -1, -1],
        [1, -1, -1, 1]
    ])
    h.compare_matrices(circ4x4, expected4x4)

    # Change the circuit to be 8x8
    grov.size = 3
    circ8x8 = grov.construct_circuit()
    expected8x8 = 0.354 * DefaultMatrix([[1, 1, 1, 1, 1, 1, 1, 1],
                                         [1, -1, 1, -1, 1, -1, 1, -1],
                                         [1, 1, -1, -1, 1, 1, -1, -1],
                                         [1, -1, -1, 1, 1, -1, -1, 1],
                                         [1, 1, 1, 1, -1, -1, -1, -1],
                                         [1, -1, 1, -1, -1, 1, -1, 1],
                                         [1, 1, -1, -1, -1, -1, 1, 1],
                                         [1, -1, -1, 1, -1, 1, 1, -1]])

    h.compare_matrices(circ8x8, expected8x8, 0.005)


def test_run():
    # Each target in a 2 qbit state should be retrieved exactly
    for t in range(4):
        grov = ga.Grovers(2, t)

        result4x1 = grov.run()

        state = [[0] for _ in range(4)]
        state[t][0] = -1
        expected4x1 = DefaultMatrix(state)

        h.compare_matrices(result4x1, expected4x1)


def test_measure():
    # Create initial small grovers algorithm, so the test code doesn't take
    # a while computing large circuits and oracles
    grov = ga.Grovers(2, 0)

    # Set the state to be in "|00>"
    grov.state = DefaultMatrix([[1], [0], [0], [0]])

    measured_state1, measured_prob1 = grov.measure()
    expec_state1, expec_prob1 = 0, 1
    assert measured_state1 == expec_state1
    assert measured_prob1 == expec_prob1

    # Non-normalised, should still work:
    grov.state *= 0.5

    measured_state2, measured_prob2 = grov.measure()
    expec_state2, expec_prob2 = 0, 1
    assert measured_state2 == expec_state2
    assert measured_prob2 == expec_prob2

    # 8x8 system, close, but not equal probability
    grov.size = 3
    grov.state = DefaultMatrix({0: {0: 0.33}, 1: {0: 0.66}}, h=8, w=1)

    # Get a random result everytime weighted by their probabilities,
    # so need to verify each possibility
    measured_state3, measured_prob3 = grov.measure()
    state_choices, prob_choices = (0, 1), (0.2, 0.8)

    if measured_state3 == state_choices[0]:
        assert pytest.approx(measured_prob3, prob_choices[0]) == True
    elif measured_state3 == state_choices[1]:
        assert pytest.approx(measured_prob3, prob_choices[1]) == True
    else:
        assert False