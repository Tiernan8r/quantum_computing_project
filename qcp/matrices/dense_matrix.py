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


class DenseMatrix(Matrix):

    def __init__(self, state: MATRIX):
        assert len(
            state) > 0, "attempting to initialise matrix with no dimensions"
        assert len(state) == len(
            state[0]), "attempting to initialise non-square matrix."

        self._state = state

        self._col = len(state)
        self._row = len(state[0]) if len(state) > 0 else 0

    @staticmethod
    def identity(n: int) -> Matrix:
        """
        Create the identity matrix with the given dimensions

        :param n int: The matrix dimension
        """
        assert isinstance(n, int), "must provide integer dimension"
        assert n > 0, "Matrix dimension must be positive"

        def determine_entry(a, b): return 1 if a == b else 0
        return DenseMatrix([
            [
                determine_entry(i, j) for i in range(n)
            ] for j in range(n)
        ])

    def __len__(self) -> int:
        return self.num_columns

    @property
    def num_rows(self) -> int:
        return self._row

    @property
    def num_columns(self) -> int:
        return self._col

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

        for i in range(len(self)):
            for j in range(len(self[i])):
                current_state[i][j] += other[i][j]

        return DenseMatrix(current_state)

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (other * -1)

    def columns(self) -> MATRIX:
        pass

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, SCALARS_TYPES):
            current_state = self.get_state().copy()

            for i in range(len(current_state)):
                for j in range(len(current_state[i])):
                    current_state[i][j] *= other

            return DenseMatrix(current_state)

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        assert len(other) > 0, "taking dot product with empty matrix"
        assert len(self) == len(other.columns()[
            0]), "matrices don't match on their row/column dimensions"

        n = len(self)
        current_state: MATRIX = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                current_state[i][j] = sum(
                    [self[i][k] * other[k][j] for k in range(n)])

        return DenseMatrix(current_state)

    def __str__(self) -> str:
        total_string = ""
        N = len(self._state)
        for i in range(N):
            total_string += "[" + \
                ",".join([f"{c:3.3g}" for c in self._state[i]]) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, N)
        return total_string

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
