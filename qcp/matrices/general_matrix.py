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
from . import Matrix
from ._types import MATRIX, VECTOR, SCALARS, SCALARS_TYPES
from typing import Union


class GeneralMatrix(Matrix):

    def __init__(self, state: MATRIX):
        assert len(
            state) > 0, "attempting to initialise matrix with no dimensions"
        assert len(state) == len(
            state[0]), "attempting to initialise non-square matrix."

        self._state = state

    @staticmethod
    def identity(n: int) -> Matrix:
        """
        Create the identity matrix with the given dimensions

        :param n int: The matrix dimension
        :raises TypeError: If input dimension is not convertable to int.
        """
        try:
            n = int(n)
        except TypeError:
            raise

        assert n > 0, "Matrix dimension must be positive"

        def determine_entry(a, b): return 1 if a == b else 0
        return GeneralMatrix([
            [
                determine_entry(i, j) for i in range(n)
            ] for j in range(n)
        ])

    def __len__(self) -> int:
        return len(self._state)

    @property
    def num_rows(self) -> int:
        return len(self._state[0]) if len(self._state) > 0 else 0

    @property
    def num_columns(self) -> int:
        return len(self._state)

    def dim(self):
        # Return the dimension of matrix, in (row,col) tuple
        # __len__ cannot return tuple, only integer
        assert not len(self.state) == 0, "Matrix cannot be empty!"
        if not isinstance(self.state[0], list):
            return (len(self.state), 1)
        else:
            return (len(self.state), len(self.state[0]))

    def __getitem__(self, i: int) -> VECTOR:
        assert i < len(self), "index out of range"
        return self._state[i]

    def __setitem__(self, i: int, v: VECTOR):
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        self._state[i] = v

    def get_state(self) -> MATRIX:
        return self._state

    def set_state(self, s: MATRIX):
        assert s is not None
        assert len(s) > 0
        assert len(s) == len(s[0]), "non square matrix state"
        self._state = s

    def rows(self) -> MATRIX:
        """Return the rows of the Matrix."""
        return self.get_state()

    def columns(self) -> MATRIX:
        """Returns the columns of the Matrix"""
        return [
            [self._state[i][j] for i in range(len(self))]
            for j in range(len(self))
        ]

    @classmethod
    def zeros(cls, nrow, ncol=1):
        # Create zero matrix with dimension (nrow,ncol)
        # Class method used to handle the creation of new object
        return cls([[0 for _ in range(nrow)] for _ in range(ncol)])

    def __iter__(self):
        return iter(self.get_state())

    def __add__(self, other: Matrix) -> Matrix:
        assert len(self) == len(other) and len(self[0]) == len(
            other[0]), "Matrix dimensions must be equal for addition"

        current_state = self.get_state().copy()

    def __sub__(self, other: Matrix):
        # Take advantage of addition method
        return self.__add__(other, -1)
        for i in range(len(self)):
            for j in range(len(self[i])):
                current_state[i][j] += other[i][j]

        return GeneralMatrix(current_state)


    def columns(self) -> MATRIX:
        pass

    def __mul__(self, other):
        # Multiplication
        # If the other input is an integer, multiply directly
        if isinstance(other, (complex, float, int)):
            nrow, ncol = self.dim()
            return Matrix([
                [
                    self.state[i][j] * other for i in range(nrow)
                ] for j in range(ncol)
            ])
        # Check if the dimensions of the two matrices are compatible
        assert self.dim()[1] == other.dim()[
            0], 'Cannot add matrices with different dimensions'
        # Product matrix is of (nrow, ncol)
        nrow = self.dim()[0]
        ncol = other.dim()[1]
        n = self.dim()[1]
        # declare empty matrix
        mul = Matrix.zeros(nrow, ncol)
        for i in range(nrow):
            for j in range(ncol):
                for k in range(n):
                    mul[i][j] += self.state[i][k] * other.state[k][j]
        return mul

# Handle right multiplication, e.g. 5*M
# Since rmul is not called if two matrices multiply,
# no need to worry about commutation
    __rmul__ = __mul__

    def __str__(self) -> str:
        pass

    def conjugate(self):
        # conjugation of matrix
        nrow, ncol = self.dim()
        for i in range(nrow):
            for j in range(ncol):
                if isinstance(self.state[i][j], complex):
                    self.state[i][j] = self.state[i][j].conjugate()
        return self.state

    def transpose(self):
        # transpose of matrix
        nrow, ncol = self.dim()
        self.state = \
            [[self.state[j][i] for i in range(nrow)] for j in range(ncol)]
        return self

    def adjoint(self):
        # dagger operation
        self.transpose()
        self.conjugate()
        return self

    def __repr__(self):
        # print list instead of object address
        return (f"{self.state}")
