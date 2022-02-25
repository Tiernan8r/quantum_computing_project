from matrix import Matrix
import math

IDENTITY = Matrix([[1, 0], [0, 1]])
TWO_HADAMARD = Matrix([[1, 1], [1, -1]]) * (1/math.sqrt(2))
ZERO_VECTOR = Matrix([[1], [0]])
ONE_VECTOR = Matrix([[0], [1]])
PAULI_X = Matrix([[0, 1], [1, 0]])
PAULI_Z = Matrix([[1, 0], [0, -1]])
