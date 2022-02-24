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
from io import UnsupportedOperation
from typing_extensions import Self
from . import Matrix
from ._types import SCALARS, SPARSE, VECTOR, MATRIX
from typing import Dict, List, Union


class SparseVector:

    def __init__(self, entries: Dict[SCALARS], size: int):
        self._entries = entries
        self._size = size

    def __len__(self):
        return self._size

    def __getitem__(self, i: int) -> SCALARS:
        assert i < self._size, "index out of range"
        if i not in self._entries:
            return 0
        return self._entries[i]


class SparseMatrix(Matrix):

    def __init__(self, state: MATRIX):
        n = len(state)
        m = 0
        if n > 0:
            m = len(state[0])
        self._row = n
        self._col = m

        self._entries: SPARSE = {
            k: {} for k in range(n)
        }

        for i in range(len(state)):
            for j in range(len(state[i])):
                entry = state[i][j]

                # ignore floating points that are within 1e-9 to 0
                if cmath.isclose(entry, 0):
                    continue

                self._entries[i][j] = entry

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

        I = SparseMatrix()
        I._row = n
        I._col = n
        I._entries = {i: {i: 1} for i in range(n)}

        return I

    def __len__(self) -> int:
        return self._row

    def _get_row(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"

        return SparseVector(self._entries[i], self._row)

    def __getitem__(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"
        return self._get_row(i)

    def __setitem__(self, i: int, v: SparseVector):
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        self._entries[i] = v._entries

    def _as_list(self) -> Matrix():
        list_representation = [
            [0 for _ in range(self._row)] for _ in range(self._col)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[i][j] = v

        return list_representation

    def get_state(self) -> MATRIX:
        return self._as_list()

    def set_state(self, s: MATRIX):
        raise UnsupportedOperation("SparseMatrix is immutable")

    def rows(self) -> MATRIX:
        """Return the rows of the Matrix."""
        return self.get_state()

    def columns(self) -> MATRIX:
        """Returns the columns of the Matrix"""
        list_representation = [
            [0 for _ in range(self._row)] for _ in range(self._col)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[j][i] = v

        return list_representation

    def __add__(self, other: Matrix) -> Matrix:
        assert self._row == len(other) and self._col == len(
            other[0]), "Matrix dimensions must be equal for addition"

        for i in range(len(self)):
            for j in range(len(self[i])):
                self._entries[i][j] += other[i][j]

        return self

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (other * -1)

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, SCALARS):
            for i, row in self._entries:
                for j in row.keys():
                    self._entries[i][j] *= other

            return self

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        assert len(other) > 0, "taking dot product with empty matrix"
        assert len(self) == len(other.columns()[
            0]), "matrices don't match on their row/column dimensions"

        new_matrix = SparseMatrix()
        new_matrix._row = self._col
        new_matrix._col = len(other[0])

        entries = {
            i: {} for i in range(self._col)
        }
        for i, row in self._entries.items():
            for j in range(new_matrix._col):
                # only need to calculate using non-zero entries
                entries[i][j] = sum([other[i][k] * row[k] for k in row.keys()])

        new_matrix._entries = entries
        # return SquareMatrix(current_state)
        return new_matrix

    def __str__(self) -> str:
        total_string = ""

        def determine_val(i, j) -> SCALARS:
            if i not in self._entries and j not in self._entries[i]:
                return 0
            return self._entries[i][j]

        for i in range(self._row):
            row_repr = [
                f"{determine_val(i, j):3.3g}" for j in range(self._col)]
            total_string += "[" + \
                ",".join(row_repr) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, self._row)
        return total_string
