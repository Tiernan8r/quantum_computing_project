from matrix import matrix
import constants as c
from tensor_product import tensor_product


def hadamard(size, targets):
    m = c.IDENTITY

    for i in range(size):
        if i in targets:
            m = tensor_product(m, c.TWO_HADAMARD)
        else:
            m = tensor_product(m, c.IDENTITY)

    h = matrix(m.get_state())
    return h


def control_x():
    pass


def control_z():
    pass
