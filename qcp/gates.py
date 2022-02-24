import cmath

from matrix import Matrix
import constants as c
from tensor_product import tensor_product

'''
Multi_Gates: constructs a large circuit matrix which acts as a gate that applies a specific gate to one or more qubits 
Params:
    size - total number of qubits we're working with
    targets - the specific qubits the gate is applied to (starting from the 1st qubit)
'''


def multi_gate(size, targets, gate, phi=complex(0)):
    g = None
    if gate == "h":
        g = c.TWO_HADAMARD
    elif gate == "x":
        g = c.PAULI_X
    elif gate == "z":
        g = c.PAULI_Z
    elif gate == "p":
        g = phase_shift(phi)

    m = Matrix([1])
    t = [x - 1 for x in targets]

    for i in range(size):
        if i in t:
            m = tensor_product(g, m)
        else:
            m = tensor_product(c.IDENTITY, m)
    return m


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
            row[i] = cmath.exp(1j * phi)
        else:
            row[i] = 1
        m.append(row)
    p = Matrix(m)
    return p


def toffoli(size, control1, control2, target):
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        if binary[-control1] == "1" and binary[-control2] == "1":
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


def zeros_list(n):
    x = []
    for i in range(n):
        x.append(0 + 0j)
    return x


def phase_shift(phi):
    return Matrix([[1, 0], [0, cmath.exp(1j * phi)]])
