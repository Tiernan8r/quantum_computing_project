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
from qcp.matrices import SparseMatrix
import qcp.gates as gts
import pytest



def test_multi_gate():
    pass


def test_control_x():
    # Gate needs a minimum of two qubits to make sense
    with pytest.raises(AssertionError) as ae1:
        gts.control_x(1, [], 0)
    assert ae1.match("need minimum of two qubits")

    # Control bits need to be within qubit range:
    with pytest.raises(AssertionError) as ae2:
        gts.control_x(2, [5], 0)
    assert ae2.match("control bit out of range")

    # More control bits indexed than there are qubits:
    with pytest.raises(AssertionError) as ae3:
        gts.control_x(2, [1, 1, 1, 1, 1, 1], 0)
    assert ae3.match("too many control bits provided")

    # Target qbit needs to be not one of the control bits:
    with pytest.raises(AssertionError) as ae4:
        gts.control_x(2, [0], 0)
    assert ae4.match("control bits and target bit cannot be the same")

    cx_4x4 = gts.control_x(2, [0], 1)
    expected_4x4 = SparseMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    assert cx_4x4.get_state() == expected_4x4.get_state()

    # Create a |00> + |10> qbit state:
    two_qubits = SparseMatrix({0: {0: 1}, 1: {}, 2: {0: 1}, 3: {}})

    # The first qbit should be untouched, the second should be flipped
    transformed_qbits = cx_4x4 * two_qubits
    expected_2_qbits = SparseMatrix({0: {0: 1}, 1: {}, 2: {}, 3: {0: 1}})
    assert transformed_qbits.get_state() == expected_2_qbits.get_state()

    cx_8x8 = gts.control_x(3, [1], 3)
    # | 000 >
    three_qbits = SparseMatrix({
        0: {0: 1}, 1: {}, 2: {}, 3: {},
        4: {}, 5: {}, 6: {}, 7: {}})
    transform_3qbits = cx_8x8 * three_qbits
    expected_3qbits = SparseMatrix({
        0: {0: 1}, 1: {}, 2: {}, 3: {},
        4: {}, 5: {}, 6: {}, 7: {}})

    assert transform_3qbits.get_state() == expected_3qbits.get_state()


def test_control_z():

    qubit0 = DefaultMatrix([[1],[0],[0],[0]])
    qubit1 = DefaultMatrix([[0],[1],[0],[0]])
    qubit2 = DefaultMatrix([[0],[0],[1],[0]])
    qubit3 = DefaultMatrix([[0],[0],[0],[1]])

    ans0 = CONTROL_Z * qubit0
    ans1 = CONTROL_Z * qubit1
    ans2 = CONTROL_Z * qubit2
    ans3 = CONTROL_Z * qubit3
    
    pass


def test_control_phase():
    pass


def test_phase_shift():
    pass

from qcp.matrices import Matrix, DefaultMatrix
from qcp.gates import oracle, oracle_gate, phase_shift
from qcp.constants import CONTROL_Z, TWO_HADAMARD
from math import pi, sqrt
import cmath

def test_phase_gate():

       ms = [ DefaultMatrix([[1,0],[0,1]]), 
           DefaultMatrix([[1,0],[0,1j]]), 
           DefaultMatrix([[1,0],[0,-1]]), 
           DefaultMatrix([[1,0],[0,-1j]]) ] 
       
       assert cmath.isclose(phase_shift(0)[1][1], ms[0][1][1])
       assert cmath.isclose(phase_shift(pi/2)[1][1], ms[1][1][1])
       assert cmath.isclose(phase_shift(pi)[1][1], ms[2][1][1])
       assert cmath.isclose(phase_shift(3*pi/2)[1][1], ms[3][1][1])

def test_hadamard_gate():

       qubit0 = DefaultMatrix([[1],[0]])
       qubit1 = DefaultMatrix([[0],[1]])
       
       ans0 = TWO_HADAMARD * qubit0
       ans1 = TWO_HADAMARD * qubit1 

       expected0 = (1/(sqrt(2))) * DefaultMatrix([[1],[1]])
       expected1 = (1/(sqrt(2))) * DefaultMatrix([[1],[-1]])

       print(TWO_HADAMARD)
       print()
       print(qubit0)
       print()
       print(ans0)
       print()
       print(expected0)

       assert expected0.get_state() == ans0.get_state()
       assert expected1.get_state() == ans1.get_state()

def test_oracle_gate():

     qubit0 = DefaultMatrix([[1],[0]])
     qubit1 = DefaultMatrix([[0],[1]])
     qubit2 = DefaultMatrix([[0],[0],[1],[0]])
     qubit3 = DefaultMatrix([[0],[0],[0],[1]])

     ans0N = oracle(0,qubit0)
     ans0P = oracle(1,qubit0)
     ans1P = oracle(0,qubit1)
     ans1N = oracle(1,qubit1)
     ans2N = oracle(2,qubit2)
     ans2P = oracle(1,qubit2)
     ans3P = oracle(3,qubit3)
     ans3N = oracle(1,qubit3)

     expected0N = DefaultMatrix([[-1],[0]])
     expected0P = DefaultMatrix([[1],[0]])
     expected1N = DefaultMatrix([[-1],[0]])
     expected1P = DefaultMatrix([[1],[0]])
     expected2N = DefaultMatrix([[0],[0],[-1],[0]])
     expected2P = DefaultMatrix([[0],[0],[1],[0]])
     expected3N = DefaultMatrix([[0],[0],[0],[-1]])
     expected3P = DefaultMatrix([[0],[0],[0],[1]])

     assert expected0N.get_state() == ans0N.get_state()
     assert expected0P.get_state() == ans0P.get_state()
     assert expected1N.get_state() == ans1N.get_state()
     assert expected1P.get_state() == ans1P.get_state()
     assert expected2N.get_state() == ans2N.get_state()
     assert expected2P.get_state() == ans2P.get_state()
     assert expected3N.get_state() == ans3N.get_state()
     assert expected3P.get_state() == ans3P.get_state()