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

from abc import ABC
from typing import Union

from qcp.matrices.types import MATRIX, SCALARS, VECTOR


class Matrix(ABC):
    """
    Method stubs for an implementation of a matrix.
    """

    def __init__(self, state: MATRIX):
        """
        Initialise the Matrix object, setting the matrix elements based off of
        the given nested list, and inferring the matrix dimensions from the
        list dimensions

        :param MATRIX state: The nested list containing the matrix elements
        """
        pass

    def __len__(self) -> int:
        """
        Return the horizontal width of the matrix.

        returns:
            int: The width of the matrix
        """
        pass

    @property
    def num_rows(self) -> int:
        """
        The number of rows in the Matrix

        returns:
            int: The number of rows in the matrix
        """
        pass

    @property
    def num_columns(self) -> int:
        """
        The number of columns in the Matrix

        returns:
            int: The number of columns in the matrix
        """
        pass

    @property
    def square(self) -> bool:
        """
        Whether the matrix is square or not.

        returns:
            bool: Whether the matrix row/column dimensions match.
        """
        return self.num_columns == self.num_rows

    @property
    def unitary(self) -> bool:
        """
        Check if matrix is Unitary (can be shifted to gates.py)

        :param Matrix: input: n x n matrix
        returns:
            bool: Whether the matrix is unitary
        """
        pass

    def __getitem__(self, i: int) -> VECTOR:
        """
        Return the row elements for the given row index in a list
        representation

        :param int i: The index of the row to get the elements of

        returns:
            :py:obj:`~qcp.matrices.types.VECTOR`: A list containing the row
            elements
        """
        pass

    def __setitem__(self, i: int, v: VECTOR):
        """
        Set the given row in the matrix to the given elements in the list

        :param int i: The index of the row to modify
        :param VECTOR v: The new elements as a list to set the row to.
        """
        pass

    def get_state(self) -> MATRIX:
        """
        Returns the matrix values as a nested list, indexed by the
        row/column indices.

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: A nested list of the matrix
            values
        """
        pass

    def __add__(self, other: Matrix) -> Matrix:
        """
        Add the matching elements of the other matrix to the entries in this
        matrix, and return a new matrix containing the resultant values.

        :param Matrix other: The matrix to add to this one.

        returns:
            Matrix: A new matrix where the elements are the addition of the
            current and applied matrix elements.
        """
        pass

    def __sub__(self, other: Matrix) -> Matrix:
        """
        Subtract the matching elements of the other matrix to the entries in
        this matrix, and return a new matrix containing the resultant values.

        :param Matrix other: The matrix to subtract from this one.

        returns:
            Matrix: A new matrix where the elements are the subtraction of the
            current and applied matrix elements.
        """
        pass

    def columns(self) -> MATRIX:
        """
        Return the transpose of the matrix as a nested list

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: The nested list of matrix
            elements, indexed by column/row.
        """
        pass

    def transpose(self) -> Matrix:
        """
        Mirror a square matrix along it's diagonal, and return a new
        matrix of these elements

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: The transpose of the current
            matrix.
        """
        pass

    def conjugate(self) -> Matrix:
        """
        Calculate the complex conjugate of each matrix element and return a
        new matrix of these conjugated elements

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: The matrix with each element
            conjugates of the current :py:obj:`qcp.matrices.matrix.Matrix`
        """
        pass

    def adjoint(self) -> Matrix:
        """
        Shortcut operation to calculate the transpose and conjugate of the
        current matrix.

        returns:
            :py:obj:`~qcp.matrices.types.MATRIX`: The new matrix that is
            transposed and then conjugated of the current matrix.
        """
        return self.transpose().conjugate()

    def trace(self) -> SCALARS:
        """
        The sum of the diagonal elements of a square matrix

        returns:
            :py:obj:`~qcp.matrices.types.SCALARS`: The sum of the diagonal
            of the matrix
        """
        pass

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:
        """
        Override of the behaviour of the `*` multiplication operator.

        If the operator is applied using a scalar value to this matrix, the
        matrix elements are each scaled by this number and a new matrix is
        returned containing these scaled elements.

        If a :py:obj:`~qcp.matrices.matrix.Matrix` object is applied using the
        `*` operator, the dot product of the two matrices is calculated, with
        the current matrix being the first Matrix, and the applied one the
        second, as order matters for matrix multiplication.

        :param Union[SCALARS, Matrix] other: The object being applied to this
            matrix

        returns:
            Matrix: A new matrix containing the calculated values as
            appropriate.
        """
        pass

    def __rmul__(self, s: SCALARS) -> Matrix:
        """
        Shim layer for the :py:meth:`~qcp.matrices.matrix.Matrix.__mul__`
        operation, so that we can pre-mulitply matrices with a scalar and
        get the expected behaviour.

        :param SCALARS other: The scalar to multiply against the matrix

        returns:
            Matrix: A new matrix where the elements are scaled by other
        """
        return self.__mul__(s)

    def __str__(self) -> str:
        """
        Create a string representation of the Matrix, with rows separated by
        newlines, and bounded by '['/']' characters.

        returns:
            str: A string representation of the matrix suitable for printing.
        """
        pass

    def _optional_newline(self, i: int, N: int) -> str:
        """
        Helper function for :py:meth:`~qcp.matrices.matrix.Matrix.__str__` to
        determine which rows require a newline character appended to them.

        :param int i: The current row index under consideration.
        :param int N: The total number of rows.

        returns:
            str: A newline character, or empty string depending on the
            condition.
        """
        return "\n" if i < N - 1 else ""
