import cmath
import math
import random

import qcp.gates as g
import qcp.register as reg
import qcp.tensor_product as tp
from qcp.algorithms.abstract_algorithm import GeneralAlgorithm
from qcp.matrices import DefaultMatrix, Matrix


def is_unitary(input: Matrix) -> bool:
    """
    Check if matrix is Unitary (can be shifted to gates.py)

    :param Matrix: input: n x n matrix
    returns:
        bool: Whether the matrix is unitary
    """
    test = input.adjoint()*input
    identity = DefaultMatrix.identity(test.num_rows)
    for i in range(input.num_rows):
        for j in range(input.num_columns):
            if cmath.isclose(test[i][j], identity[i][j]):
                continue
            else:
                return False
    return True


def optimum_qubit_size(precision: int, error: float) -> int:
    """
    Return the number of qubit required for targeted number of decimal
    and error rate.
    """
    return math.ceil(precision + math.log2(2+1/(2*error)))


def qft_gate(size: int) -> Matrix:
    """
    Performs Quantum Fourier Transform, which change the basis

    :param int: size: number of qubits
    returns:
        Matrix: gate
    """

    gate = g.multi_gate(size, [], g.Gate.I)
    for i in range(size-1, -1, -1):
        gate = qft_rotation_gate(
            size, i)*g.multi_gate(size, [i], g.Gate.H)*gate
    for i in range(int(size/2)):
        gate = g.swap(size, i, size-1-i)*gate
    return gate


def inverse_qft_gate(size: int) -> Matrix:
    """
    Performs Inverse Quantum Fourier Transform
    :param int: size: number of qubits
    returns:
        Matrix: gate
    """
    gate = g.multi_gate(size, [], g.Gate.I)
    for i in range(int(size/2)):
        gate = g.swap(size, i, size-i-1)*gate
    for i in range(0, size):
        gate = g.multi_gate(size, [i], g.Gate.H) * \
            inverse_qft_rotation_gate(size, i)*gate
    return gate


def qft_rotation_gate(size: int, current_qubit: int) -> Matrix:
    """"
    Construct the R2...R(n-i) gate for Quantum Fourier Transform

    :param int size: total number of qubits, n
    :param intcurrent_qubit: which qubit to apply the rotation gate to, i
    returns:
        Matrix: gate
    """
    gate: Matrix = DefaultMatrix.identity(2**size)
    for i in range(1, current_qubit+1):
        phi = 2*math.pi/2**(i+1)
        control = current_qubit-i
        gate = gate * g.control_phase(size, [control], current_qubit, phi)
    return gate


def inverse_qft_rotation_gate(size: int, current_qubit: int) -> Matrix:
    """"
    Construct the R2...R(n-i) gate for Inverse Quantum Fourier Transform

    :param int size: total number of qubits, n
    :param int current_qubit: which qubit to apply the rotation gate to, i
    """
    gate: Matrix = DefaultMatrix.identity(2**size)
    for i in range(0, current_qubit):
        phi = -2*math.pi/2**(current_qubit+1-i)
        control = i
        gate = gate * g.control_phase(size, [control], current_qubit, phi)

    return gate


class PhaseEstimation(GeneralAlgorithm):

    def __init__(self, size: int, unitary: Matrix, eigenvector: Matrix):
        """
        Implement Phase Estimation, which requires a unitary matrix and one of
        its eigenvector as the input.

        :param int: size: precision of the phase output, i.e. no. of decimal
        :param Matrix unitary: a unitary matrix whose eigenvalue's phase is
            the target
        :param Matrix eigenvector: an eigenvector of the unitary matrix

        Example:
        phase = 0.125
        unitary = DefaultMatrix([[1,0],[0,exp(1j*math.pi*phase)]])
        eigenvector = DefaultMatrix([[0],[1]])
        PE = Phase_Esimation(3,unitary,eigenvector)
        PE.run()
        print(PE.measure())
        """
        assert is_unitary(unitary), "Matrix must be unitary!"
        self.unitary = unitary

        self.auxiliary = eigenvector
        self.auxsize = int(math.log2(eigenvector.num_rows))

        super().__init__(size)

    def initial_state(self) -> Matrix:
        """
        Creates a state vector corresponding to |0..0>
        :return: returns state vector
        """
        init = super().initial_state()
        return tp.tensor_product(self.auxiliary, init)

    def first_layer(self) -> Matrix:
        """
        Tensor Hadamard (first register) with Identity (auxiliary)
        """
        id = g.multi_gate(self.auxsize, [], g.Gate.I)
        return tp.tensor_product(
            id,
            g.multi_gate(self.size, [i for i in range(self.size)], g.Gate.H)
        )

    def second_layer(self) -> Matrix:
        """
        Control-U Gate applied to auxiliary register
        """
        totalsize = self.size+self.auxsize
        gate = g.multi_gate(totalsize, [], g.Gate.I)
        rep = 0
        for i in range(0, self.size):
            for j in range(2**rep):
                n = self.size-1-i
                gate = g.control_u(totalsize, n, self.unitary) * gate
            rep += 1
        return gate

    def third_layer(self):
        """"
        Inverse QFT Gate tensor for the first register
        """
        id = g.multi_gate(self.auxsize, [], g.Gate.I)
        return tp.tensor_product(
            id,
            inverse_qft_gate(self.size)
        )

    def construct_circuit(self):
        """
        Combines the layers
        """
        first = self.first_layer()
        second = self.second_layer()
        third = self.third_layer()

        return third * second * first

    def measure_probabilities(self):
        p = self._amplitude()
        n_bits = int(math.log2(2**self.size))

        for i in range(2**self.size):
            binary = bin(i)[2:].zfill(n_bits)
            print(f"|{binary}> : {p[i]:.4g}")

    def _amplitude(self):
        n = 2 ** self.size

        result = DefaultMatrix.zeros(n)
        for i in range(2**self.size):
            tp_mat = DefaultMatrix.zeros(n)
            tp_mat[i][0] = 1
            trial = tp.tensor_product(self.auxiliary, tp_mat)
            result[i] = (trial.transpose()*self.state)[0]

        p = reg.measure(result)

        return p

    def measure(self):
        """
        'measures' self.state by selecting a state weighted by its
        (amplitude ** 2)
        :return: the state observed and the probability of measuring
                said state
        """

        p = self._amplitude()
        observed = random.choices([i for i in range(len(p))], p, k=1)
        probability = p[observed[0]]

        return int(observed[0]/2**self.size), probability
