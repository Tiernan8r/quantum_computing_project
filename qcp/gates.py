from Matrix import Matrix
import consts
from tensor_product import tensor_product


def hadamard(size, targets):
    m = consts.IDENTITY

    for i in range(size):
        if i in targets:
            m = tensor_product(m, consts.TWO_HADAMARD)
        else:
            m = tensor_product(m, consts.IDENTITY)

    h = Matrix(m.get_state())
    return h

# TODO: ORACLE - AKA Controlled z Gate
# TODO: X Gate
# TODO: CNOT Gate
