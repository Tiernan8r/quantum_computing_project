from qcp.matrices import Matrix, DefaultMatrix, SPARSE
import constants as c
import tensor_product as tp
import gates as g


def pull_set_bits(n: int):
    """
    Creates a list of bits that would be set to 1
    to make the number n
    :param n: number
    :return: list[int] list of bits
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

    def __init__(self, size, target_state):
        """
        This is an implementation of Grover's algorithm which efficiently
        finds a specific item in a list of items. In this implementation
        we use Grover's algorithm to increase the amplitude of the
        "target_state" and reduce all others in a "size"-qubit system

        :param size: number of qubits in our circuit
        :param target_state: specific state we want to target/select
        """

        assert (target_state < (2 ** size))
        self.size = size
        self.target = target_state
        self.state = self.initial_state()

        self.oracle = self.single_target_oracle()
        self.diffuser = self.diffusion()
        self.max_reflections = self.size - 1
        # can only reflect size-1 times to get maximum probability

        self.circuit = self.construct_circuit()

    def initial_state(self):
        """
        Creates a state vector corresponding to ¦0..0>
        :return: returns state vector
        """
        m = DefaultMatrix([[1]])
        for i in range(self.size):
            m = tp.tensor_product(m, c.ZERO_VECTOR)
        return m

    def single_target_oracle(self):
        """
        Creates an oracle gate - a gate which 'selects' our target state
        by phase shifting it by pi (turning 1 into -1 in the matrix
        representation)
        :return: Matrix representing our oracle
        """
        not_placement = (2 ** self.size) - 1 - self.target
        t = pull_set_bits(not_placement)
        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)], self.size - 1)
        selector = g.multi_gate(self.size, t, g.Gate.X)
        oracle = selector * cz
        oracle *= selector
        return oracle

    def diffusion(self):
        """
        Creates a diffusion gate - a gate which amplifies the probability of
        selecting our target state
        :return: Matrix representing diffusion gate
        """
        h = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.H)
        cz = g.control_z(self.size, [i for i in range(0, self.size - 1)], self.size - 1)
        x = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.X)
        diff = h * (x * (cz * (x * h)))
        return diff

    def construct_circuit(self):
        """
        Constructs the circuit for Grover's algorithm by applying an initial
        set of Hadamards and repeating the oracle and diffusion gates
        until our target state is close to 1 in terms of probability
        :return: Matrix representing our completed Grover's algorithm
        """
        circuit = g.multi_gate(self.size, [i for i in range(0, self.size)], g.Gate.H)

        while self.max_reflections > 0:
            circuit = self.oracle * circuit
            circuit = self.diffuser * circuit
            self.max_reflections -= 1
        return circuit

    def run(self):
        """
        Multiplies our Grover's circuit with the initial state
        :return: Final state
        """
        result = self.circuit * self.state
        self.state = result
        return result


grovs = Grovers(5, 6)
r = grovs.run()
print(r)
