from qcp.matrices import DefaultMatrix, Matrix, MATRIX
import qcp.register as reg
import qcp.gates as g
import random

class sudoku:

    def __init__(self):
        self.size = 9
        self.state = self.initial_state()

        self.circuit = self.construct_circuit()

    def initial_state(self) -> Matrix:
        """
        Creates a state vector corresponding to |1..0>

        returns:
            Matrix: the state vector
        """
        entries: MATRIX = [[0] for _ in range(2 ** self.size)]
        entries[0][0] = 1
        return DefaultMatrix(entries)

    def oracle(self):
        cond = self.sudoku_conditions()
        cnot = g.control_x(9, [4, 5, 6, 7], 8)
        oracle = cond * cnot * cond
        return oracle

    def sudoku_conditions(self):
        cond1 = g.control_x(9, [1], 4) * g.control_x(9, [0], 4)
        cond2 = g.control_x(9, [2], 5) * g.control_x(9, [0], 5)
        cond3 = g.control_x(9, [3], 6) * g.control_x(9, [1], 6)
        cond4 = g.control_x(9, [3], 7) * g.control_x(9, [2], 7)
        cond = cond4 * cond3 * cond2 * cond1
        return cond

    def diffusion(self):
        had = g.multi_gate(9, [0, 1, 2, 3], g.Gate.H)
        xs = g.multi_gate(9, [0, 1, 2, 3], g.Gate.X)
        cz = g.control_z(9, [0, 1, 2], 3)

        diff = had * xs * cz * xs * had
        return diff

    def construct_circuit(self):
        had = g.multi_gate(9, [0, 1, 2, 3], g.Gate.H)
        circuit = had

        for i in range(2):
            circuit = self.oracle() * circuit

            circuit = self.diffusion() * circuit
        return circuit

    def run(self):
        self.state = self.circuit * self.state
        return self.state

    def measure(self):
        p = reg.measure(self.state)
        # list of weighted probabilities with the index representing the state

        observed = random.choices(
            [i for i in range(len(p))], p, k=1)  # type: ignore
        probability = p[observed[0]]
        return observed[0], probability


s = sudoku()

s.run()
o, p = s.measure()
print(s.state)
#print(o)
#print(p)

