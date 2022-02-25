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
from . import Matrix
from ._types import SCALARS, SCALARS_TYPES, SPARSE, VECTOR, MATRIX
from typing import Dict, List, Union


def _list_to_dict(vals: List[SCALARS]) -> Dict[int, SCALARS]:
    d = {}
    for i in range(len(vals)):
        entry = vals[i]

        # ignore floating points that are within 1e-9 to 0
        if cmath.isclose(entry, 0):
            continue

        d[i] = entry

    return d


class SparseVector:

    def __init__(self, entries: Union[List[SCALARS], Dict[int, SCALARS]], size: int):
        if isinstance(entries, list):
            self._entries = _list_to_dict(entries)
        else:
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

    def __init__(self, state: Union[MATRIX, SPARSE]):

        if isinstance(state, dict):

            self._entries = state

            self._row = max(state.keys()) + 1  # indexes from 0...
            self._col = 0
            for i in range(self._row):
                if i in self._entries:
                    width = max(self._entries[i].keys()) + 1
                    self._col = width if width > self._col else self._col

            return

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
            self._entries[i] = _list_to_dict(state[i])

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

        I = SparseMatrix([])
        I._row = n
        I._col = n
        I._entries = {i: {i: 1} for i in range(n)}

        return I

    @property
    def num_rows(self) -> int:
        return self._row

    @property
    def num_columns(self) -> int:
        return self._col

    @property
    def square(self) -> bool:
        return self._row == self._col

    def __len__(self) -> int:
        return self._row

    def _get_row(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"

        return SparseVector(self._entries[i], self._row)

    def __getitem__(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"
        return self._get_row(i)

    def __setitem__(self, i: int, v: Union[SparseVector, List[SCALARS], Dict[int, SCALARS]]):
        assert i < len(self), "index out of range"
        sv = None
        if isinstance(v, list):
            assert len(v) == len(self[i]), "row dimension does not match"
            sv = SparseVector(v, self.num_rows)
        elif isinstance(v, dict):
            assert max(v.keys()) + 1 < self.num_rows, "row too wide"
            sv = SparseVector(v, self.num_rows)
        else:
            sv = v

        self._entries[i] = sv._entries

    def _as_list(self) -> Matrix():
        list_representation = [
            [0 for _ in range(self.num_columns)] for _ in range(self.num_rows)
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
        assert self.num_rows == other.num_rows and self.num_columns == other.num_columns, "Matrix dimensions must be equal for addition"

        for i in range(other.num_rows):
            for j in range(other.num_columns):
                if j not in self._entries[i]:
                    self._entries[i][j] = other[i][j]
                else:
                    self._entries[i][j] += other[i][j]

        return self

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (other * -1)

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, SCALARS_TYPES):
            for i, row in self._entries.items():
                for j in row.keys():
                    self._entries[i][j] *= other

            return self

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        assert len(other) > 0, "taking dot product with empty matrix"
        assert len(self) == len(other.columns()[
            0]), "matrices don't match on their row/column dimensions"

        new_matrix = SparseMatrix([])
        new_matrix._row = self._col
        new_matrix._col = len(other[0])

        entries = {
            i: {} for i in range(self._col)
        }
        for i, row in self._entries.items():
            for j in range(new_matrix._col):
                # only need to calculate using non-zero entries
                entries[i][j] = sum([other[k][j] * row[k] for k in row.keys()])

        new_matrix._entries = entries

        return new_matrix

    def __str__(self) -> str:
        total_string = ""

        def determine_val(i, j) -> SCALARS:
            if i not in self._entries or j not in self._entries[i]:
                return 0
            return self._entries[i][j]

        for i in range(self._row):
            row_repr = [
                f"{determine_val(i, j):3.3g}" for j in range(self._col)]
            total_string += "[" + \
                ",".join(row_repr) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, self._row)
        return total_string
