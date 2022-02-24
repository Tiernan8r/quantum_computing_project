import cmath

from matrix import Matrix
import constants as c
from tensor_product import tensor_product


# Notation note : |001> represents a 3 qubit system where the first qubit is |1> and the second and third qubit is |0>
# Targets and Controls work off this notation

def multi_gate(size: int, targets: list[int], gate: str, phi=complex(0)):
    """
    Constructs a (2**size by 2**size) gate matrix that applies a specific gate to one or more specified qubits

    :param size: total number of qubits in circuit -> int
    :param targets: list of qubits the specified gate will be applied to -> List[int]
    :param gate: string character representing which specified gate we want to apply;
                                h = hadamard, x = Pauli x, z = Pauli z, p = Phase gate
    :param phi: Phase angle for the phase gate -> complex number
    :return: Matrix([int])
    """

    if gate == "h":
        g = c.TWO_HADAMARD
    elif gate == "x":
        g = c.PAULI_X
    elif gate == "z":
        g = c.PAULI_Z
    elif gate == "p":
        g = phase_shift(phi)
    else:
        return

    m = Matrix([1])
    t = [x - 1 for x in targets]

    for i in range(size):
        if i in t:
            m = tensor_product(g, m)
        else:
            m = tensor_product(c.IDENTITY, m)
    return m


def control_x(size, controls, target):
    """
    Constructs a (2**size by 2**size) control-x gate with given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the x gate will be applied to -> int
    :return: Matrix(int)
    """
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        conditions = [binary[-i] == "1" for i in controls]

        if all(conditions):
            if binary[-target] == "0":
                binary[-target] = "1"
            else:
                binary[-target] = "0"

        num = "".join(binary)
        number = int(num, 2)

        row = zeros_list(2 ** size)
        row[number] = 1
        m.append(row)
    x = Matrix(m)
    return x


def control_z(size, controls, target):
    """
    Constructs a (2**size by 2**size) control-z gate with given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the z gate will be applied to -> int
    :return: Matrix(int)
    """
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)
        conditions = [binary[-i] == "1" for i in controls]

        if all(conditions) and binary[-target] == "1":
            row[i] = -1
        else:
            row[i] = 1
        m.append(row)
    z = Matrix(m)
    return z


def control_phase(size, controls, target, phi):
    """
    Constructs a (2**size by 2**size) control-phase gate with given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the phase gate will be applied to -> int
    :param phi: angle the target qubit will be phase shifted by -> complex
    :return: Matrix(complex)
    """

    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)
        conditions = [binary[-i] == "1" for i in controls]

        if all(conditions) and binary[-target] == "1":
            row[i] = cmath.exp(1j * phi)
        else:
            row[i] = 1
        m.append(row)
    p = Matrix(m)
    return p


def zeros_list(n):
    """
    Creates a list of size n full of zeros
    :param n: size of list
    :return: list[int]
    """
    x = []
    for i in range(n):
        x.append(0 + 0j)
    return x


def phase_shift(phi):
    """
    Creates a 2 x 2 phase shift matrix
    :param phi: angle the qubit is phase shifted by
    :return: Matrix(complex)
    """
    return Matrix([[1, 0], [0, cmath.exp(1j * phi)]])
