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
from qcp.tensor_product import _tensor_product_sparse as tps
import qcp.constants as c
import qcp.tensor_product as tp
from typing import List
import enum
import math


class Gate(enum.Enum):
    """Enum class to encode gate options in multi_gates"""
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
    :return Matrix: Matrix representing the composite gate
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
        return DefaultMatrix.identity(2**size)

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
    invertor = sum(2**i for i in range(size))
    flip_mask = mask ^ invertor

    # Find the bit index of the target
    target_bit = 2**target

    # Iterate over states in the gate
    for i in range(0, n):
        # If the bits are targeted and meet the mask condition, it needs
        # to be flipped
        condition = (i & target_bit) & flip_mask

        x = i
        if condition:
            # bit flip the targetted bit by the control bits
            x ^= mask

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
    invertor = sum(2**i for i in range(size))
    flip_mask = mask ^ invertor

    target_bit = 2**target

    for i in range(0, n):
        condition = (i & target_bit) == target_bit and i ^ mask == flip_mask

        val = 1
        # Modulo 2 filters out an bits that don't meet the condition,
        # Any number that is of the form of all ones, like 3 = 11, or 7 = 111
        # Can be determined by taking their modulus with 2, since binary is in
        # powers of 2.
        if condition:
            val = -1
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


def control_phase(size: int, controls: List[int], target: int,
                  phi: complex) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-phase gate with
     given controls and target
    :param size int: total number of qubits in circuit
    :param controls List[int]: List of control qubits
    :param target int: target qubit the phase gate will be
                    applied to
    :param phi complex: angle the target qubit will be phase
                    shifted by
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

    target_bit = 2**target

    for i in range(0, n):
        condition = (i & target_bit) == target_bit

        val = 1+0j
        if condition:
            val = cmath.exp(1j * phi)
        m[i] = {i: val}

    return DefaultMatrix(m, h=n, w=n)


def phase_shift(phi: complex) -> Matrix:
    """
    Creates a 2 x 2 phase shift matrix
    :param phi: angle the qubit is phase shifted by
    :return: Matrix(complex)
    """
    return DefaultMatrix([[1, 0], [0, cmath.exp(1j * phi)]])

def swap(size: int, target: List[int]) -> Matrix: 
    """
    Construct swap gate which swaps two states
    :param size int: total number of qubits in circuit
    :param target int: 2 target states the swap gate will be applied to
    :return Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two states"
    assert len(target) == 2, 'Invalid swap targets!'
    
    swapgate = multi_gate(size,[],Gate.I)
    temp = swapgate[target[1]-1]
    swapgate[target[1]-1] = swapgate[target[0]+1]
    swapgate[target[0]+1] = temp
    return swapgate

def control_U(size: int,control: int,unitary: DefaultMatrix):
    """
    Implement the control U gate
    :param size int: number of qubits
    :param control int: control qubit 
    :param unitary DefaultMatrix: Unitary gate to apply 
    :return Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two qubits"
    n = 2 ** size
    targetsize = int(math.log2(unitary.num_rows))
    # Make sure the control/target bits are within the qbit size
    assert control in range(size), "control bit out of range"
    assert control not in range(size,size+unitary.num_rows), "control bit cannot be in auxiliary register"

    gate0 = DefaultMatrix([[1,0],[0,0]])
    gate1 = DefaultMatrix([[0,0],[0,1]])
    cu_gate = tps(multi_gate(control,[],Gate.I),tps(gate0,multi_gate(size-1-control,[],Gate.I)))
    cu_gate += tps(tps(tps(multi_gate(control,[],Gate.I),gate1),multi_gate(size-1-targetsize-control,[],Gate.I)),unitary)
    return cu_gate