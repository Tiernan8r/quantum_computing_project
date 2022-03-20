import random

import qcp.gates as g
import qcp.register as reg
from qcp.algorithms import GeneralAlgorithm

# This class uses Grover's algorithm to solve the 2x2 sudoku board with 4
# entries V0, V1, V2, V3 and two number choices, 0 & 1
#   +----+----+
#   | V0 | V1 |
#   +----+----+
#   | V2 | V3 |
#   +----+----+
#
# To do this we use 9 qubits with the first 4 representing our inputs
# V0, V1, V2, V3. The second 4 representing the four conditions we have for a
# solution for this sudoku board, such that when the qubit is 1, the condition
# is met. And the final qubit representing whether all the conditions have
# been met.
#


class Sudoku(GeneralAlgorithm):

    def __init__(self):
        super().__init__(9)

    def oracle(self):
        """
        The oracle gate for this problem checks the inputs to see whether the
        conditions have been met, using self.sudoku_conditions(), stores
        whether all of the conditions have been met or not in the 9th qubit by
        using a cnot gate, and then resets all the condition qubits that were
        changed by self.sudoku_conditions()

        :return: Matrix: representing the oracle gate
        """
        cond = self.sudoku_conditions()
        cnot = g.control_x(9, [4, 5, 6, 7], 8)
        oracle = cond * cnot * cond
        return oracle

    def sudoku_conditions(self):
        """
        For the 2x2 sudoku board there are 4 conditions which must be true for
        a solution to be valid:
        V0 != V1
        V0 != V2
        V1 != V3
        V2 != V3
        the variables cond1,..,cond4 respectively enforce these conditions by
        applying XOR gates across the relevant input qubits and outputting in
        the relative condition qubit
        :return: Matrix: representing all of the sudoku conditions
        """
        cond1 = g.control_x(9, [1], 4) * g.control_x(9, [0], 4)
        cond2 = g.control_x(9, [2], 5) * g.control_x(9, [0], 5)
        cond3 = g.control_x(9, [3], 6) * g.control_x(9, [1], 6)
        cond4 = g.control_x(9, [3], 7) * g.control_x(9, [2], 7)
        cond = cond4 * cond3 * cond2 * cond1

        return cond

    def diffusion(self):
        """
        Creates a diffusion gate - a gate which amplifies the probability of
        selecting our target state

        returns:
            Matrix: Matrix representing diffusion gate
        """
        had = g.multi_gate(9, [0, 1, 2, 3], g.Gate.H)
        xs = g.multi_gate(9, [0, 1, 2, 3], g.Gate.X)
        cz = g.control_z(9, [0, 1, 2], 3)

        diff = had * xs * cz * xs * had

        return diff

    def construct_circuit(self):
        """
        Constructs the circuit to solve the sudoku problem by implementing the
        hadamard on the first 4 qubits, then the oracle gate across the
        entire circuit, followed by the diffusion gate that acts on the first 4
        qubits applying the oracle and diffuser twice to maximise the amplitude
        of the solution

        returns:
            Matrix representing our completed Grover's algorithm for sudoku
        """
        had = g.multi_gate(9, [0, 1, 2, 3], g.Gate.H)
        circuit = had

        for i in range(2):
            circuit = self.oracle() * circuit

            circuit = self.diffusion() * circuit

        return circuit

    def measure_state(self):
        """
        Randomly 'measures' self.state by selecting a state (out of 2**9)
        weighted by its (amplitude ** 2)

        returns:
            Tuple[int, float]: The state observed and the probability of
            measuring said state
        """
        p = reg.measure(self.state)
        # list of weighted probabilities with the index representing the state

        observed = random.choices(
            [i for i in range(len(p))], p, k=1)  # type: ignore
        probability = p[observed[0]]

        return observed[0], probability

    def measure_solution(self):
        """
        Randomly measures 1 of 16 possible options that the 4 input variables
        can be with the probability of measuring a certain option determined by
        the probabilities associated with each state
        :return:
            Tuple[[str], float]: The input solution observed and the
            probability of observing that solution
        """
        prob = reg.measure(self.state)
        sol_probs = [0] * 16
        for i in range(len(prob)):
            sol_probs[i % 16] += prob[i]

        observed = random.choices(
            [i for i in range(len(sol_probs))], sol_probs, k=1)  # type: ignore
        chosen_prob = sol_probs[observed[0]]

        vx = format(observed[0], '04b')

        return [vx[-4], vx[-3], vx[-2], vx[-1]], chosen_prob
