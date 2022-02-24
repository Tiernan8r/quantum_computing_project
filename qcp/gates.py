from matrix import Matrix
import constants as c
from tensor_product import tensor_product
import math

'''
Multi_Gates: constructs a large circuit matrix which acts as a gate that applies a specific gate to one or more qubits 
Params:
    size - total number of qubits we're working with
    targets - the specific qubits the gate is applied to (starting from the 1st qubit)
'''


def multi_hadamard(size: int, targets: list[int]):
    h = Matrix([[1]])

    t = [x - 1 for x in targets]
    for i in range(size):
        if i in t:
            h = tensor_product(c.TWO_HADAMARD, h)
        else:
            h = tensor_product(c.IDENTITY, h)

    return h


def multi_x(size: int, targets: list[int]):
    x = Matrix([1])

    t = [x - 1 for x in targets]
    for i in range(size):
        if i in t:
            x = tensor_product(c.PAULI_X, x)
        else:
            x = tensor_product(c.IDENTITY, x)
    return x


def multi_z(size: int, targets: list[int]):
    z = Matrix([1])
    t = [x - 1 for x in targets]

    for i in range(size):
        if i in t:
            z = tensor_product(c.PAULI_Z, z)
        else:
            z = tensor_product(c.IDENTITY, z)
    return z


def multi_phase_shift(size, targets, phi):
    p = Matrix([1])
    t = [x - 1 for x in targets]

    for i in range(size):
        if i in t:
            p = tensor_product(phase_shift(phi), p)
        else:
            p = tensor_product(c.IDENTITY, p)
    return p


def control_x(size, control, target):
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        if binary[-control] == "1":
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


def control_z(size, control, target):
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)

        if binary[-control] == "1" and binary[-target] == "1":
            row[i] = -1
        else:
            row[i] = 1
        m.append(row)
    z = Matrix(m)
    return z


def control_phase(size, control, target, phi):
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)

        if binary[-control] == "1" and binary[-target] == "1":
            row[i] = math.e ** (1j * phi)
        else:
            row[i] = 1
        m.append(row)
    p = Matrix(m)
    return p


def toffoli(size, control1, control2, target):
    pass


def zeros_list(n):
    x = []
    for i in range(n):
        x.append(0)
    return x


def phase_shift(phi):
    return Matrix([[1, 0], [0, math.e ** (1j * phi)]])
