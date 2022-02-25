from matrices import DefaultMatrix
import math

IDENTITY = DefaultMatrix([[1, 0], [0, 1]])
TWO_HADAMARD = DefaultMatrix([[1, 1], [1, -1]]) * (1/math.sqrt(2))
ZERO_VECTOR = DefaultMatrix([[1], [0]])
ONE_VECTOR = DefaultMatrix([[0], [1]])
PAULI_X = DefaultMatrix([[0, 1], [1, 0]])
PAULI_Z = DefaultMatrix([[1, 0], [0, -1]])
