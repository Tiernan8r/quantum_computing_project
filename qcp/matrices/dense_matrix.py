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
from qcp.matrices import Matrix
from qcp.matrices.types import MATRIX, VECTOR, SCALARS, SCALARS_TYPES
from typing import Union


class DenseMatrix(Matrix):

    def __init__(self, state: MATRIX):
        assert len(
            state) > 0, "attempting to initialise matrix with no dimensions"

        row_widths = [len(row) for row in state]
        for i in range(len(row_widths)):
            assert row_widths[0] ==\
                row_widths[i], "matrix rows must have equal dimension"

        self._state = state

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
        return len(self._state[0]) if len(self._state) > 0 else 0

    @property
    def num_columns(self) -> int:
        return len(self._state)

    def __getitem__(self, i: int) -> VECTOR:
        assert i < len(self), "index out of range"
        return self._state[i]

    def __setitem__(self, i: int, v: VECTOR):
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        self._state[i] = v

    def get_state(self) -> MATRIX:
        return self._state

    def rows(self) -> MATRIX:
        """Return the rows of the Matrix."""
        return self.get_state()

    def columns(self) -> MATRIX:
        """Returns the columns of the Matrix"""
        return [
            [self._state[i][j] for i in range(len(self))]
            for j in range(len(self[0]))
        ]

    @classmethod
    def zeros(cls, nrow, ncol=1):
        # Create zero matrix with dimension (nrow,ncol)
        # Class method used to handle the creation of new object
        return cls([[0 for _ in range(ncol)] for _ in range(nrow)])

    def __iter__(self):
        return iter(self.get_state())

    def __add__(self, other: Matrix) -> Matrix:
        assert len(self) == len(other) and len(self[0]) == len(
            other[0]), "Matrix dimensions must be equal for addition"

        state = self.get_state().copy()

        for i in range(len(self)):
            for j in range(len(self[i])):
                state[i][j] += other[i][j]

        return DenseMatrix(state)

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (-1 * other)

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, SCALARS_TYPES):
            state = self.get_state().copy()

            for i in range(len(state)):
                for j in range(len(state[i])):
                    state[i][j] *= other

            return DenseMatrix(state)

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        assert len(other) > 0, "taking dot product with empty matrix"
        assert len(self) == len(other.columns()[
            0]), "matrices don't match on their row/column dimensions"

        n = len(self)
        state: MATRIX = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                state[i][j] = sum(
                    [self[i][k] * other[k][j] for k in range(n)])

        return DenseMatrix(state)

    def __str__(self) -> str:
        total_string = ""
        N = len(self._state)
        for i in range(N):
            total_string += "[" + \
                ",".join([f"{c:3.3g}" for c in self._state[i]]) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, N)
        return total_string

    def conjugate(self) -> Matrix:
        """Calculate the conjugate of the matrix"""
        state = self.get_state().copy()

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if isinstance(state[i][j], complex):
                    state[i][j] = state[i][j].conjugate()
        return DenseMatrix(state)

    def transpose(self) -> Matrix:
        """Create a new Matrix that is the transpose of the current one."""
        return DenseMatrix(self.columns())
