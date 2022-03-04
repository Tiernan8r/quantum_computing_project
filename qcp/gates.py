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
from qcp.matrices import Matrix, DefaultMatrix
import constants as c
from qcp.matrices import SPARSE
from tensor_product import tensor_product
from typing import List
from enum import Enum


class Gate(Enum):
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
                    applied to
    :param gate Gate: Enum of which gate we want to apply
    :param phi complex: Phase angle for the phase gate
    :return Matrix: Matrix representing the composite gate
    """

    if gate == Gate.H:
        g = c.TWO_HADAMARD
    elif gate == Gate.X:
        g = c.PAULI_X
    elif gate == Gate.Z:
        g = c.PAULI_Z
    elif gate == Gate.P:
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


def control_x(size: int, controls: List[int], target: int) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-x gate with
    given controls and target
    :param size int: total number of qubits in circuit
    :param controls List[int]: List of control qubits
    :param target int: target qubit the x gate will be applied to
    :returns Matrix: Matrix representing the gate
    """
    assert size > 1, "need minimum of two qubits"
    n = 2 ** size
    assert isinstance(controls, list)
    for con in controls:
        assert con < n, "control bit out of range"
    assert len(controls) <= n, "too many control bits provided."

    assert target not in \
        controls, "control bits and target bit cannot be the same"

    m: SPARSE = {}

    mask = sum(2**c for c in set(controls))
    diff = size - mask.bit_length()
    mask <<= diff

    for i in range(0, n):
        condition = i & mask

        x = i
        if (condition >> diff) % 2:
            x = i ^ (1 << (target - 1))

        m[i] = {x: 1}

    return DefaultMatrix(m, h=n, w=n)


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
    for con in controls:
        assert con < n, "control bit out of range"
    assert len(controls) <= n, "too many control bits provided."

    assert target not in \
        controls, "control bits and target bit cannot be the same"

    m: SPARSE = {}

    mask = sum(2**c for c in set(controls))
    diff = size - mask.bit_length()
    mask <<= diff

    for i in range(0, n):
        condition = i | mask

        val = 1
        if condition % 2 and ((i ^ target) >> diff) % 2:
            val = -1
        m[i] = {i: val}

    return DefaultMatrix(m, h=n, w=n)


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
    for con in controls:
        assert con < n, "control bit out of range"
    assert len(controls) <= n, "too many control bits provided."

    assert target not in \
        controls, "control bits and target bit cannot be the same"

    m: SPARSE = {}

    mask = sum(2**c for c in set(controls))
    diff = size - mask.bit_length()
    mask <<= diff

    for i in range(0, n):
        condition = i | mask

        val = 1+0j
        if condition % 2 and ((i ^ target) >> diff) % 2:
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
