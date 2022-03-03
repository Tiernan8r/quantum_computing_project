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
from ._types import SCALARS, SCALARS_TYPES, SPARSE, MATRIX
from typing import Dict, List, Union


def _list_to_dict(vals: List[SCALARS], limit: int = -1) -> Dict[int, SCALARS]:
    """Convert a given list of values into a dictionary mapping indices
    to non-zero values

    :param vals list: List of vector values.
    :param limit int: Optional iteration limit for fixed sized rows.
    :returns dict: dict of key/value pairs for non-zero entries in the list.
    """
    # If the SparseMatrix dimensions have been explicitly set, will only
    # convert list entries up to that hard limit into the dict.
    lim = limit if limit > 0 else len(vals)

    d = {}
    for i in range(lim):
        if i >= len(vals):
            continue
        entry = vals[i]

        # ignore floating points that are within 1e-9 to 0
        if cmath.isclose(entry, 0):
            continue

        d[i] = entry

    return d


class SparseVector:
    """Sparse representation of a row vector"""

    def __init__(self, entries:
                 Union[List[SCALARS], Dict[int, SCALARS]], size: int):
        if isinstance(entries, list):
            self._entries = _list_to_dict(entries, limit=size)
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

    def __init__(self, state: Union[MATRIX, SPARSE], w: int = -1, h: int = -1):
        """Initialise a SparseMatrix, using either a List[List[]] object,
        or a pre-indexed dictionary mapping indices to non-zero values.

        :param state: List[List[SCALAR]] or Dict[int, Dict[int, SCALAR]] used
                        to determine the matrix content
        :param w int: Optional overload of the Matrix width dimension
        :param h int: Optional overload of the Matrix height dimension
        """
        given_width = w > 0
        if given_width:
            self._col = w
        given_height = h > 0
        if given_height:
            self._row = h

        # If the given 'state' is already a dict mapping, no need
        # to convert it
        if isinstance(state, dict):

            self._entries = state

            if not given_height:
                self._row = max(state.keys()) + 1  # indexes from 0...

            if not given_width:
                self._col = 0
                # Find the highest row index in the dictionary, and assume
                # that the matrix is that wide
                for i in range(self._row):
                    if i in self._entries:
                        width = max(self._entries[i].keys()) + 1
                        self._col = width if width > self._col else self._col

            return

        if not given_height:
            n = len(state)
            self._row = n
        if not given_width:
            m = len(state[0]) if self._row > 0 else 0
            self._col = m

        entries: SPARSE = {
            k: {} for k in range(self._row)
        }

        for i in range(self._row):
            s = []
            if i < len(state):
                s = state[i]
            entries[i] = _list_to_dict(s, limit=self._col)
        self._entries = entries

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

        return SparseMatrix({i: {i: 1} for i in range(n)}, w=n, h=n)

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

        entry = {}
        if i in self._entries:
            entry = self._entries[i]

        return SparseVector(entry, self._row)

    def __getitem__(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"
        return self._get_row(i)

    def __setitem__(self, i: int, v:
                    Union[SparseVector, List[SCALARS], Dict[int, SCALARS]]
                    ):
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

    def _as_list(self) -> Matrix:
        list_representation: MATRIX = [
            [0 for _ in range(self.num_columns)] for _ in range(self.num_rows)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[i][j] = v

        return list_representation

    def get_state(self) -> MATRIX:
        return self._as_list()

    def rows(self) -> MATRIX:
        """Return the rows of the Matrix."""
        return self.get_state()

    def columns(self) -> MATRIX:
        """Returns the columns of the Matrix"""
        list_representation: MATRIX = [
            [0 for _ in range(self._row)] for _ in range(self._col)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[j][i] = v

        return list_representation

    def transpose(self) -> Matrix:
        entries = {}
        for i, row in self._entries.items():
            for j, v in row.items():
                if j not in entries:
                    entries[j] = {i: v}
                else:
                    entries[j][i] = v
        return SparseMatrix(entries, h=self.num_columns, w=self.num_rows)

    def conjugate(self) -> Matrix:
        for i, row in self._entries.items():
            for j, v in row.items():
                if isinstance(v, complex):
                    self._entries[i][j] = v.conjugate()
        return self

    def __add__(self, other: Matrix) -> Matrix:
        row_match = self.num_rows == other.num_rows
        column_match = self.num_columns == other.num_columns
        assert row_match and \
            column_match, "Matrix dimensions must be equal for addition"

        for i in range(other.num_rows):
            for j in range(other.num_columns):
                # Don't bother trying to add zero values
                other_val = other[i][j]
                if cmath.isclose(other_val, 0):
                    continue
                # Since the SparseMatrix only keeps track of non-zero
                # entries, track this new entry if it becomes non-zero
                if j not in self._entries[i]:
                    self._entries[i][j] = other_val
                else:
                    self._entries[i][j] += other_val

        return self

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (-1 * other)

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, SCALARS_TYPES):
            for i, row in self._entries.items():
                for j in row.keys():
                    self._entries[i][j] *= other

            return self

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        assert other.num_rows > 0, "taking dot product with empty matrix"
        assert self.num_columns == other.num_rows, \
            "matrices don't match on their row/column dimensions"

        new_matrix = SparseMatrix([], w=other.num_columns, h=self.num_rows)

        entries: SPARSE = {
            i: {} for i in range(self.num_columns)
        }

        for i, row in self._entries.items():
            for j in range(new_matrix.num_columns):
                # only need to calculate using the non-zero entries of self
                # TODO: Can further optimise this 'other' is also a
                # SparseMatrix by only using it's non-zero entries too
                entries[i][j] = sum([other[k][j] * row[k] for k in row.keys()])

        new_matrix._entries = entries

        return new_matrix

    def __str__(self) -> str:
        total_string = ""

        for i in range(self._row):
            row_repr = [
                f"{self[i][j]:3.3g}" for j in range(self._col)]
            total_string += "[" + \
                ",".join(row_repr) + "]"
            # Don't add newline for last row:
            total_string += (lambda i, N: "\n" if i <
                             N - 1 else "")(i, self._row)
        return total_string
