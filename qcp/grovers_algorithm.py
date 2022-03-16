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
from qcp.matrices import DefaultMatrix, Matrix, MATRIX
import qcp.register as reg
import qcp.gates as g
import random
from typing import List, Tuple


def pull_set_bits(n: int) -> List[int]:
    """
    Creates a list of bits that would be set to 1
    to make the number n

    :param n int: number
    :returns List[int]: list of bits
    """
    bits = []
    count = 0
    while n:
        cond = n & 1
        if cond:
            bits.append(count)
        n >>= 1
        count += 1
    return bits


class Grovers:

    def __init__(self, size: int, target_state: int):
        """
        This is an implementation of Grover's algorithm which efficiently
        finds a specific item in a list of items. In this implementation
        we use Grover's algorithm to increase the amplitude of the
        "target_state" and reduce all others in a "size"-qubit system

        :param size int: number of qubits in our circuit
        :param target_state int: specific state we want to target/select
        """
        assert size > 1, "need minimum of two qbits"
        assert target_state < (2 ** size), \
            "target must be within qbit state indices"
        self.size = size
        self.target = target_state
        self.state = self.initial_state()

        self.oracle = self.single_target_oracle()
        self.diffuser = self.diffusion()
        self.max_reflections = self.size - 1
        # can only reflect size-1 times to get maximum probability

        self.circuit = self.construct_circuit()

    def initial_state(self) -> Matrix:
        """
        Creates a state vector corresponding to |1..0>

        :returns Matrix: returns state vector
        """
        entries: MATRIX = [[0] for _ in range(2 ** self.size)]
        entries[0][0] = 1
        return DefaultMatrix(entries)

    def single_target_oracle(self) -> Matrix:
        """
        Creates an oracle gate - a gate which 'selects' our target state
        by phase shifting it by pi (turning 1 into -1 in the matrix
        representation)

        :returns Matrix: Matrix representation of our Oracle
        """
        not_placement = (2 ** self.size) - 1 - self.target
        t = pull_set_bits(not_placement)
        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)],
                         self.size - 1)
        selector = g.multi_gate(self.size, t, g.Gate.X)
        oracle = selector * cz
        oracle *= selector
        return oracle

    def diffusion(self) -> Matrix:
        """
        Creates a diffusion gate - a gate which amplifies the probability of
        selecting our target state

        :returns Matrix: Matrix representing diffusion gate
        """
        h = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.H)
        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)],
                         self.size - 1)
        x = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.X)
        diff = h * (x * (cz * (x * h)))
        return diff

    def construct_circuit(self) -> Matrix:
        """
        Constructs the circuit for Grover's algorithm by applying an initial
        set of Hadamards and repeating the oracle and diffusion gates
        until our target state is close to 1 in terms of probability

        :returns Matrix: Matrix representing our completed Grover's algorithm
        """
        circuit = g.multi_gate(self.size, [i for i in range(0, self.size)],
                               g.Gate.H)

        while self.max_reflections > 0:
            circuit = self.oracle * circuit
            circuit = self.diffuser * circuit
            self.max_reflections -= 1
        return circuit

    def run(self) -> Matrix:
        """
        Multiplies our Grover's circuit with the initial state

        :returns Matrix: Column matrix representation of the final state
        """
        self.state = self.circuit * self.state
        return self.state

    def measure(self) -> Tuple[int, float]:
        """
        'measures' self.state by selecting a state weighted by its
        (amplitude ** 2)

        :returns Tuple[int, float]: The state observed and the probability of 
            measuring said state
        """
        p = reg.measure(self.state)
        # list of weighted probabilities with the index representing the state

        observed = random.choices(
            [i for i in range(len(p))], p, k=1)  # type: ignore
        probability = p[observed[0]]
        return observed[0], probability
