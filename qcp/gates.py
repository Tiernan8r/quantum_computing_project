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
"""
Contains the code required calculate the required gates used to construct
Grover's Algorithm
"""
import math
import cmath
from qcp.matrices import Matrix, DefaultMatrix, SPARSE
import qcp.constants as c
from qcp.matrices.types import MATRIX, SCALARS
import qcp.tensor_product as tp
from typing import List
import enum


class Gate(enum.Enum):
    """
    Enums of the options of gate types to use in qcp.gates.multi_gates()
    """

    H = "h"
    X = "x"
    Z = "z"
    P = "p"
    I = "i"  # noqa: E741


# Notation note : |001> represents a 3 qubit system where the first qubit is
# |1> and the second and third qubit is |0>
# Targets and Controls work off this notation but you only need to enter the
# number of the qubit you want to target/control


def multi_gate(size: int, targets: List[int], gate: Gate, phi=0j) -> Matrix:
    """
    Constructs a (2**size by 2**size) gate matrix that applies a
    specific gate to one or more specified qubits

    :param size int: total number of qubits in circuit
    :param targets List[int]: list of qubits the specified gate will be
                    applied to, indexing from 0.
    :param gate Gate: Enum of which gate we want to apply
    :param phi complex: Phase angle for the phase gate
    returns:
        Matrix: Matrix representing the composite gate
    """

    if gate is Gate.H:
        g = c.TWO_HADAMARD
    elif gate is Gate.X:
        g = c.PAULI_X
    elif gate is Gate.Z:
        g = c.PAULI_Z
    elif gate is Gate.P:
        g = phase_shift(phi)
    else:
        return DefaultMatrix.identity(2 ** size)

    m: Matrix = DefaultMatrix([[1]])

    for i in range(size):
        if i in targets:
            m = tp.tensor_product(g, m)
        else:
            m = tp.tensor_product(c.IDENTITY, m)
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

    :param int size: total number of qubits in circuit
    :param List[int] controls: List of control qubits,
        if empty, 0th bit is used as the control.
    :param int target: target qubit the x gate will be applied to
    returns:
        Matrix: Matrix representing the gate
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
    mask = sum(2 ** c for c in set(controls))

    # Find the bit index of the target
    target_bit = 2 ** target

    # Iterate over states in the gate
    for i in range(0, n):
        # If the bits are targeted and meet the mask condition, it needs
        # to be flipped
        condition = i & mask

        x = i
        if condition >= mask:
            # bit flip the targetted bit by the control bits
            x ^= target_bit

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


def _generic_control(size: int, controls: List[int],
                     target: int, cval: SCALARS) -> Matrix:
    """
    Constructs a (2**size by 2**size) control gate with
    given controls, target and the control value.
    This is a generic implementation of the logic used for
    :py:meth:`qcp.gates.control_z` and :py:meth:`qcp.gates.control_phase`

    :param int size: total number of qubits in circuit
    :param List[int] controls: List of control qubits
    :param int target: target qubit the gate will be applied to
    :param SCALARS cval: The control value in the gate
    returns:
        Matrix: Matrix representing the gate
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
    mask = sum(2 ** c for c in set(controls))

    target_bit = 2 ** target

    for i in range(0, n):
        condition1 = (i & target_bit)
        condition2 = i & mask
        val: SCALARS = 1
        # Modulo 2 filters out an bits that don't meet the condition,
        # Any number that is of the form of all ones, like 3 = 11, or 7 = 111
        # Can be determined by taking their modulus with 2, since binary is in
        # powers of 2.
        if condition1 == target_bit and condition2 >= mask:
            val = cval
        m[i] = {i: val}

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

    :param int size: total number of qubits in circuit
    :param List[int] controls: List of control qubits
    :param int target: target qubit the z gate will be applied to
    returns:
        Matrix: Matrix representing the gate
    """
    return _generic_control(size, controls, target, -1)


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


def control_phase(size: int, controls: List[int], target: int,
                  phi: complex) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-phase gate with
    given controls and target

    :param int size: total number of qubits in circuit
    :param List[int] controls: List of control qubits
    :param int target: target qubit the phase gate will be applied to
    :param complex phi: angle the target qubit will be phase shifted by
    returns:
        Matrix: Matrix representing the gate
    """
    val = cmath.exp(1j * phi)
    return _generic_control(size, controls, target, val)


def phase_shift(phi: complex) -> Matrix:
    """
    Creates a 2 x 2 phase shift matrix

    :param complex phi: angle the qubit is phase shifted by
    returns:
        Matrix: Matrix representing the phase shift gate.
    """
    return DefaultMatrix([[1, 0], [0, cmath.exp(1j * phi)]])


def swap(size: int, target0: int, target1: int) -> Matrix:
    """
    Construct swap gate which swaps two states

    :param int size: total number of qubits in circuit
    :param int target0: The first target bit to swap
    :param int target1: The second target bit to swap

    returns:
        Matrix: Matrix representing the gate
    """
    # Can be optimized further

    assert size > 1, "need minimum of two qbits"
    assert target0 != target1, "swap targets must be different"

    bit_bounds = range(size)
    assert target0 in bit_bounds, "first target bit out of range"
    assert target1 in bit_bounds, "second target bit out of range"

    target0, target1 = sorted((target0, target1))

    n = 2 ** size
    swapgate: Matrix = DefaultMatrix.zeros(n, n)

    for i in range(2**size):
        bit_str = (bin(i)[2:].zfill(size))
        swapbit_str = (
            bit_str[0:target0] +
            bit_str[target1] +
            bit_str[target0+1:target1] +
            bit_str[target0] +
            bit_str[target1+1:]
        )

        bit = int(bit_str, 2)
        swapbit = int(swapbit_str, 2)
        vec_entries: MATRIX = [[0] for _ in range(2**size)]
        swapvec_entries: MATRIX = [[0] for _ in range(2**size)]
        vec_entries[bit] = [1]
        swapvec_entries[swapbit] = [1]
        vector = DefaultMatrix(vec_entries)
        swapvector = DefaultMatrix(swapvec_entries)
        # Outer product to create matrix
        swapgate += swapvector*vector.transpose()

    return swapgate


def control_U(size: int, control: int, unitary: Matrix):
    """
    Implement the control U gate

    :param int size: number of qubits
    :param int control: control qubit
    :param Matrix unitary: Unitary gate to apply
    returns:
        Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two qubits"

    targetsize = int(math.log2(unitary.num_rows))
    # Make sure the control/target bits are within the qbit size
    assert control in range(size), "control bit out of range"
    assert control not in range(
        size, size+unitary.num_rows), \
        "control bit cannot be in auxiliary register"

    gate0 = DefaultMatrix([[1, 0], [0, 0]])
    gate1 = DefaultMatrix([[0, 0], [0, 1]])

    cu_gate = tp.tensor_product(
        multi_gate(control+targetsize, [], Gate.I),
        tp.tensor_product(
            gate0,
            multi_gate(size-1-control-targetsize, [], Gate.I)
        )
    )

    cu_gate += tp.tensor_product(
        unitary,
        tp.tensor_product(
            tp.tensor_product(
                multi_gate(control, [], Gate.I),
                gate1
            ),
            multi_gate(size-1-targetsize-control, [], Gate.I)
        )
    )

    return cu_gate
