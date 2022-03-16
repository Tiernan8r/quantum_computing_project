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
from qcp.matrices.types import SCALARS, VECTOR, MATRIX


class Matrix(ABC):
    """
    Method stubs for an immutable implementation of a matrix.
    """

    def __init__(self, state: MATRIX):
        pass

    def __len__(self) -> int:
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

    def __getitem__(self, i: int) -> VECTOR:
        pass

    def __setitem__(self, i: int, v: VECTOR):
        pass

    def get_state(self) -> MATRIX:
        """
        Returns the matrix values as a nested list, indexed by the
        row/column indices.

        returns:
            MATRIX: A nested list of the matrix values
        """
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __sub__(self, other: Matrix) -> Matrix:
        pass

    def columns(self) -> MATRIX:
        """
        Return the transpose of the matrix as a nested list

        returns:
            MATRIX: The nested list of matrix elements, indexed by
            column/row.
        """
        pass

    def transpose(self) -> Matrix:
        """
        Mirror a square matrix along it's diagonal, and return a new
        matrix of these elements

        returns:
            Matrix: The transpose of the current matrix.
        """
        pass

    def conjugate(self) -> Matrix:
        """
        Calculate the complex conjugate of each matrix element and return a
        new matrix of these conjugated elements

        returns:
            Matrix: The matrix with each element conjugates of the current
            Matrix
        """
        pass

    def adjoint(self) -> Matrix:
        """
        Shortcut operation to calculate the transpose and conjugate of the
        current matrix.

        returns:
            Matrix: The new matrix that is transposed and then conjugated of
            the current matrix
        """
        return self.transpose().conjugate()

    def trace(self) -> SCALARS:
        """
        The sum of the diagonal elements of a square matrix

        returns:
            SCALARS: The sum of the diagonal of the matrix
        """
        pass

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:
        pass

    def __rmul__(self, other: Union[SCALARS, Matrix]) -> Matrix:
        return self.__mul__(other)

    def __str__(self) -> str:
        pass

    def _optional_newline(self, i: int, N: int) -> str:
        return "\n" if i < N - 1 else ""
