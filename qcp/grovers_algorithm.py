from qcp.matrices import Matrix, DefaultMatrix, SPARSE
import constants as c
import tensor_product as tp
import gates as g


def pull_set_bits(n):
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
    def __init__(self, size, target_state):
        self.size = size
        self.target = target_state
        self.state = self.initial_state()

        self.oracle = self.single_target_oracle()
        self.diffuser = self.diffusion()
        self.max_reflections = self.size - 1

        self.circuit = self.construct_circuit()

    def initial_state(self):
        m = DefaultMatrix([[1]])
        for i in range(self.size):
            m = tp.tensor_product(m, c.ZERO_VECTOR)
        return m

    def single_target_oracle(self):

        not_placement = (2 ** self.size) - 1 - self.target
        t = pull_set_bits(not_placement)

        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)], self.size - 1)
        selector = g.multi_gate(self.size, t, g.Gate.X)
        oracle = selector * cz
        oracle *= selector
        return oracle

    def diffusion(self):
        h = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.H)
        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)], self.size - 1)
        x = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.X)
        diff = h * (x * (cz * (x * h)))
        return diff

    def construct_circuit(self):
        circuit = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.H)

        while self.max_reflections > 0:
            circuit *= self.oracle
            circuit *= self.diffuser
            self.max_reflections -= 1
        return circuit

    def probabilities(self):
        pass


x = Grovers(3, 4)
