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

from qcp.matrices import Matrix, DefaultMatrix
from qcp.gates import phase_shift
from qcp.constants import TWO_HADAMARD
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


