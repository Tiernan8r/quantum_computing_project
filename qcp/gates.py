from matrix import matrix
import constants as c
from tensor_product import tensor_product

'''
Multi_Gates: constructs a large circuit matrix which acts as a gate that applies a specific gate to one or more qubits 
Params:
    size - total number of qubits we're working with
    targets - the specific qubits the gate is applied to (starting from the 0th qubit)
'''


def multi_hadamard(size, targets):
    h = matrix([[1]])

    for i in range(size):
        if i in targets:
            h = tensor_product(h, c.TWO_HADAMARD)
        else:
            h = tensor_product(h, c.IDENTITY)

    return h


def multi_x(size, targets):
    x = matrix([1])

    for i in range(size):
        if i in targets:
            x = tensor_product(x, c.PAULI_X)
        else:
            x = tensor_product(x, c.IDENTITY)
    return x


def multi_z(size, targets):
    z = matrix([1])

    for i in range(size):
        if i in targets:
            z = tensor_product(z, c.PAULI_Z)
        else:
            z = tensor_product(z, c.IDENTITY)
    return z


def control_x(size, control, target):
    pass


def control_z(size, control, target):
    pass


def toffoli(size, control1, control2, target):
    pass
