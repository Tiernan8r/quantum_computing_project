# Copyright 2022 Tiernan8r
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import cmath
from qcp.matrices import Matrix, DefaultMatrix, SPARSE
import constants as c
from tensor_product import tensor_product
from typing import List


# Notation note : |001> represents a 3 qubit system where the first qubit is
# |1> and the second and third qubit is |0>
# Targets and Controls work off this notation but you only need to enter the
# number of the qubit you want to target/control
def multi_gate(size: int, targets: List[int], gate: str, phi=complex(0)) \
        -> Matrix:
    """
    Constructs a (2**size by 2**size) gate matrix that applies a
    specific gate to one or more specified qubits

    :param size: total number of qubits in circuit -> int
    :param targets: list of qubits the specified gate will be
                    applied to -> List[int]
    :param gate: string character representing which specified gate we
            want to apply;
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
        return c.IDENTITY

    m = DefaultMatrix([[1]])
    t = [x - 1 for x in targets]

    for i in range(size):
        if i in t:
            m = tensor_product(g, m)
        else:
            m = tensor_product(c.IDENTITY, m)
    return m

# NOTE:
# The way the control/target bit is indexed is by indexing the
# control bit in the byte notation:
# E.g: 13 = 1101 in bit notation, so this is indexed as
#       +---+---+---+---+
# BITS  | 1 | 1 | 0 | 1 |
#       +---+---+---+---+
# INDEX | 3 | 2 | 1 | 0 |
#       +---+---+---+---+
# in the usual little endian indexing notation
# Therefore, in this example, the target/control bits are in the index
# range [0, 3]


def control_x(size: int, controls: List[int], target: int) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-x gate with
    given controls and target
    :param size int: total number of qubits in circuit
    :param controls List[int]: List of control qubits, if empty, 0th bit is
                                used as the control.
    :param target int: target qubit the x gate will be applied to
    :returns Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two qubits"
    n = 2 ** size
    assert isinstance(controls, list)

    # Make sure the control/target bits are within the qbit size
    bit_bounds = range(size)
    for con in controls:
        assert con in bit_bounds, "control bit out of range"
    assert target in bit_bounds, "target bit out of range"

    assert target not in \
        controls, "control bits and target bit cannot be the same"

    m: SPARSE = {}

    # Use set() to ignore repeat control bits, as we are only interested in
    # unique control bits
    # since the controls are the bit positions, we can convert this to a
    # bitmask by summing them at 2**idx
    # EG: controls = [0, 2, 4]
    # corresponds to 0, 4, 16 as numbers,
    # bitmask is 10101 in binary notation
    mask = sum(2**c for c in set(controls))

    # Invert all bits in place in the bitmask
    flip_mask = sum(2**i for i in range(size))
    mask ^= flip_mask

    # Iterate over states in the gate
    for i in range(0, n):
        # If the bits pass the mask condition, they need to be flipped
        condition = (i & mask) >> target

        x = i
        # Modulo 2 filters out an bits that don't meet the condition,
        # Any number that is of the form of all ones, like 3 = 11, or 7 = 111
        # Can be determined by taking their modulus with 2, since binary is in
        # powers of 2.
        # We bitshift right by the target index, as we want to ignore that bit
        if condition % 2:
            # The bit to target is indexed in Big Endian notation,
            # so need to shift the target relative to the last bit index
            shift = size - 1 - target
            # bit flip the targetted bit when it meets the criteria
            x = i ^ (1 << shift)

        m[i] = {x: 1}

    return DefaultMatrix(m, h=n, w=n)

# NOTE:
# The way the control/target bit is indexed is by indexing the
# control bit in the byte notation:
# E.g: 13 = 1101 in bit notation, so this is indexed as
#       +---+---+---+---+
# BITS  | 1 | 1 | 0 | 1 |
#       +---+---+---+---+
# INDEX | 3 | 2 | 1 | 0 |
#       +---+---+---+---+
# in the usual little endian indexing notation
# Therefore, in this example, the target/control bits are in the index
# range [0, 3]


def control_z(size: int, controls: List[int], target: int) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-z gate with
     given controls and target
    :param size int: total number of qubits in circuit
    :param controls List[int]: List of control qubits
    :param target int: target qubit the z gate will be
                    applied to
    :return Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two qubits"
    n = 2 ** size
    assert isinstance(controls, list)

    # Make sure the control/target bits are within the qbit size
    bit_bounds = range(size)
    for con in controls:
        assert con in bit_bounds, "control bit out of range"
    assert target in bit_bounds, "target bit out of range"

    assert target not in \
        controls, "control bits and target bit cannot be the same"

    m: SPARSE = {}

    # Use set() to ignore repeat control bits, as we are only interested in
    # unique control bits
    # since the controls are the bit positions, we can convert this to a
    # bitmask by summing them at 2**idx
    # EG: controls = [0, 2, 4]
    # corresponds to 0, 4, 16 as numbers,
    # bitmask is 10101 in binary notation
    mask = sum(2**c for c in set(controls))

    target_bit = 2**target

    for i in range(0, n):
        condition = i & (mask | target_bit)

        val = 1
        # Modulo 2 filters out an bits that don't meet the condition,
        # Any number that is of the form of all ones, like 3 = 11, or 7 = 111
        # Can be determined by taking their modulus with 2, since binary is in
        # powers of 2.
        if condition % 2 and i//size not in controls:
            val = -1
        m[i] = {i: val}

    return DefaultMatrix(m, h=n, w=n)


def control_phase(size: int, controls: List[int], target: int,
                  phi: complex) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-phase gate with
     given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the phase gate will be
                    applied to -> int
    :param phi: angle the target qubit will be phase
                    shifted by -> complex
    :return: Matrix(complex)
    """

    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)
        conditions = [binary[-j] == "1" for j in controls]

        if all(conditions) and binary[-target] == "1":
            row[i] = cmath.exp(1j * phi)
        else:
            row[i] = 1
        m.append(row)
    p = DefaultMatrix(m)
    return p


def zeros_list(n: int):
    """
    Creates a list of size n full of zeros
    :param n: size of list
    :return: list[int]
    """
    return [(0 + 0j) for _ in range(n)]


def phase_shift(phi: complex) -> Matrix:
    """
    Creates a 2 x 2 phase shift matrix
    :param phi: angle the qubit is phase shifted by
    :return: Matrix(complex)
    """
    return DefaultMatrix([[1, 0], [0, cmath.exp(1j * phi)]])
