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
Constructs the quantum register, circuits of composite gates, and runs the
simulation of Grover's Algorithm
"""
import abc
import random
from typing import List, Tuple

import qcp.register as reg
from qcp.matrices import SPARSE, DefaultMatrix, Matrix


class GeneralAlgorithm(abc.ABC):

    def __init__(self, size: int):
        assert size > 1, "need minimum of two qbits"
        self.size = size

        self.state = self.initial_state()
        self.circuit = self.construct_circuit()

    def initial_state(self) -> Matrix:
        """
        Creates a state vector corresponding to |1..0>

        returns:
            Matrix: the state vector
        """
        entries: SPARSE = {i: {} for i in range(2 ** self.size)}
        entries[0][0] = 1
        return DefaultMatrix(entries)

    def construct_circuit(self) -> Matrix:
        """
        Construct the circuit for the algorithm

        returns:
            Matrix: Matrix representing our the circuit for the algorithm
        """
        pass

    def run(self) -> Matrix:
        """
        Run the algorithm by applying the quantum circuit to the initial
        state

        returns:
            Matrix: Column matrix representation of the final state
        """
        if self.circuit is not None:
            self.state = self.circuit * self.state

        return self.state

    def measure(self) -> Tuple[int, float]:
        """
        'measures' self.state by selecting a state weighted by its
        (amplitude ** 2)

        returns:
            Tuple[int, float]: The state observed and the probability of
            measuring said state
        """
        p = self.probabilities()
        # list of weighted probabilities with the index representing the state

        observed = random.choices(
            [i for i in range(len(p))], p, k=1)  # type: ignore
        probability = p[observed[0]]

        return int(observed[0]), probability

    def probabilities(self) -> List[float]:
        """
        Returns the amplitudes of the measured state, representing the
        probabilities to be in each state.

        returns:
            List[float]: A list of states, where each element is the
                probability to be in that state.
        """
        if self.state is not None:
            return reg.measure(self.state)

    def measure_probabilities(self):
        """
        Print a table of the probabilities associated with each
        measured state.
        """
        pass
