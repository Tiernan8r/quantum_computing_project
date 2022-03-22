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
from __future__ import annotations

import cmath
from typing import Union

from qcp.matrices import Matrix
from qcp.matrices.types import MATRIX, SCALARS, SCALARS_T, VECTOR


class DenseMatrix(Matrix):
    """
    Implementation of a Dense Matrix class, where each matrix entry is stored
    in memory, including entries of value zero.
    """

    def __init__(self, state: MATRIX):
        """
        Initialise the dense matrix, using the given nested list as our matrix
        content

        :param MATRIX state: A nested list containing values for each entry in
            the matrix.
        """
        assert len(
            state) > 0, "attempting to initialise matrix with no dimensions"

        row_widths = [len(row) for row in state]
        for i in range(len(row_widths)):
            assert row_widths[0] ==\
                row_widths[i], "matrix rows must have equal dimension"

        self._state = state

    @staticmethod
    def identity(n: int) -> DenseMatrix:
        """
        Create the identity matrix with the given dimensions

        :param int n: The matrix dimension
        returns:
            DenseMatrix: The identity matrix of given dimension
        """
        assert isinstance(n, int), "must provide integer dimension"
        assert n > 0, "Matrix dimension must be positive"

        def determine_entry(a, b): return 1 if a == b else 0
        return DenseMatrix([
            [
                determine_entry(i, j) for i in range(n)
            ] for j in range(n)
        ])

    @staticmethod
    def zeros(nrow: int, ncol: int = 1) -> DenseMatrix:
        """
        Create a DenseMatrix of given dimensions, where each value of the
        matrix is zero.

        :param int nrow: The row dimension of the DenseMatrix
        :param int ncol: The (optional) column dimenion of the DenseMatrix
            defaults to 1, to be a column vector.
        returns:
            DenseMatrix: The matrix object of our given size.
        """
        # Create zero matrix with dimension (nrow,ncol)
        # Class method used to handle the creation of new object
        return DenseMatrix([[0 for _ in range(ncol)] for _ in range(nrow)])

    def __len__(self) -> int:
        """
        Return the horizontal size of the DenseMatrix.

        returns:
            int: The number of columns in the DenseMatrix
        """
        return self.num_columns

    @property
    def num_rows(self) -> int:
        """
        Return the number of rows in the DenseMatrix.

        returns:
            int: The number of rows
        """
        return len(self._state[0]) if len(self._state) > 0 else 0

    @property
    def num_columns(self) -> int:
        """
        Return the number of columns in the DenseMatrix.

        returns:
            int: The number of columns.
        """
        return len(self._state)

    
    @property
    def unitary(self) -> bool:
        """
        Check if matrix is Unitary (can be shifted to gates.py)

        :param Matrix: input: n x n matrix
        returns:
            bool: Whether the matrix is unitary
        """
        test = self.adjoint()*self
        identity = identity(test.num_rows)
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if cmath.isclose(test[i][j], identity[i][j]):
                    continue
                else:
                    return False
        return True

    def __getitem__(self, i: int) -> VECTOR:
        """
        Get the List representation of the row of index i.

        :param int i: The row index to get.
        returns:
            :py:obj:`~qcp.matrices.types.VECTOR`: List representation of the
            row.
        """
        assert i < len(self), "index out of range"
        return self._state[i]

    def __setitem__(self, i: int, v: VECTOR):
        """
        Set the given row inplace to the new row values in the given list.

        :param int i: The row index to modify
        :param VECTOR v: The list of values to set the row to
        """
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        self._state[i] = v

    def get_state(self) -> MATRIX:
        """
        Return the matrix values as a nested list

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: A nested list of the matrix
            values indexed by row/column
        """
        return self._state

    def rows(self) -> MATRIX:
        """
        Equivalent to
        :py:meth:`qcp.matrices.dense_matrix.DenseMatrix.get_state()`.

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: A nested list of the matrix
            values indexed by row/column
        """
        return self.get_state()

    def columns(self) -> MATRIX:
        """
        The transpose of the matrix as a nested list

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: A nested list of the matrix
            values transposed, indexed by column/row.
        """
        return [
            [self._state[i][j] for i in range(len(self))]
            for j in range(len(self[0]))
        ]

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
        if isinstance(other, SCALARS_T):
            state = self.get_state().copy()

            for i in range(len(state)):
                for j in range(len(state[i])):
                    state[i][j] *= other

            return DenseMatrix(state)

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        """
        Calculate the dot product between this Matrix, and another Matrix.

        :param Matrix other: The matrix to dot product with this one.

        returns:
            Matrix: A new matrix that conforms to the rules of matrix
            dot producting.
        """
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
                self._optional_newline(i, N)
        return total_string

    def conjugate(self) -> DenseMatrix:
        """
        Create a new :py:obj:`qcp.matrices.dense_matrix.DenseMatrix` where
        each value in the matrix is the complex conjugate of the current
        matrix values.

        returns:
            DenseMatrix: A DenseMatrix object of the same dimensions of the
            current matrix, with each value conjugated in place.
        """
        state = self.get_state().copy()

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if isinstance(state[i][j], complex):
                    state[i][j] = state[i][j].conjugate()
        return DenseMatrix(state)

    def transpose(self) -> DenseMatrix:
        """
        Flips the matrix elements along the diagonal, and return a new
        :py:obj:`qcp.matrices.dense_matrix.DenseMatrix` containing these
        values.

        returns:
            DenseMatrix: The transpose of the current matrix.
        """
        return DenseMatrix(self.columns())

    def trace(self) -> SCALARS:
        """
        Calculate the sum of the diagonal elements of the matrix

        returns:
            :py:obj:`~qcp.matrices.types.SCALARS`: The sum of all diagonal
            elements, with type determined by the value types.
        """
        assert self.square, "can only take the trace of square matrices"
        tr: SCALARS = 0
        for i in range(self.num_rows):
            tr += self[i][i]

        return tr
