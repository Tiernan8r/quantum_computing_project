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
import tensor_product as tp
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
                    applied to, indexing from 0.
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
        return DefaultMatrix.identity(2**size)

    m = DefaultMatrix([[1]])

    for i in range(size):
        if i in targets:
            m = tp.tensor_product(m, g)
        else:
            m = tp.tensor_product(m, c.IDENTITY)
    return m


def control_x(size: int, controls: List[int], target: int) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-x gate with
    given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the x gate will be applied to -> int
    :return: Matrix(int)
    """
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        conditions = [binary[-j] == "1" for j in controls]

        if all(conditions):
            if binary[-target] == "0":
                binary[-target] = "1"
            else:
                binary[-target] = "0"

        num = "".join(binary)
        number = int(num, base=2)

        row = zeros_list(2 ** size)
        row[number] = 1
        m.append(row)
    x = DefaultMatrix(m)
    return x


def control_z(size: int, controls: List[int], target: int) -> Matrix:
    """
    Constructs a (2**size by 2**size) control-z gate with
     given controls and target
    :param size: total number of qubits in circuit ->
    :param controls: List of control qubits -> List[int]
    :param target: target qubit the z gate will be
                    applied to -> int
    :return: Matrix(int)
    """
    m = []

    for i in range(0, 2 ** size):
        f = '0' + str(size) + 'b'
        binary = list(format(i, f))

        row = zeros_list(2 ** size)
        conditions = [binary[-j] == "1" for j in controls]

        if all(conditions) and binary[-target] == "1":
            row[i] = -1
        else:
            row[i] = 1
        m.append(row)
    z = DefaultMatrix(m)
    return z


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
