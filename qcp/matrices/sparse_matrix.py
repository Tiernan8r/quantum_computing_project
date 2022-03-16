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
from copy import deepcopy
from qcp.matrices import Matrix
from qcp.matrices.types import SCALARS, SCALARS_T, SPARSE, MATRIX
from typing import Dict, List, Union


def _list_to_dict(vals: List[SCALARS], limit: int = -1) -> Dict[int, SCALARS]:
    """Convert a given list of values into a dictionary mapping indices
    to non-zero values

    :param vals list: List of vector values.
    :param limit int: Optional iteration limit for fixed sized rows.
    returns:
        dict: dict of key/value pairs for non-zero entries in the list.
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
    """
    Sparse implementation of a row vector, where only the non-zero elements
    are stored in memory, and any non saved index is taken to be zero.
    """

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
        return self._entries.get(i, 0)

    def __setitem__(self, i: int, v: SCALARS):
        assert i < self._size, "index out of range"
        self._entries[i] = v


class SparseMatrix(Matrix):
    """
    Implementation of a Sparse Matrix object, where only the non-zero matrix
    elements are stored in memory, and if a matrix element is not indexed, it
    is taken to be zero.
    """

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
                        # max() errors on calls with empty lists
                        if len(self._entries[i].keys()) == 0:
                            continue
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
    def identity(n: int) -> SparseMatrix:
        """
        Create the identity matrix with the given dimensions

        :param int n: The matrix dimension
        returns:
            SparseMatrix: The SparseMatrix identity matrix object.
        """
        assert isinstance(n, int), "matrix dimension must be an integer"
        assert n > 0, "Matrix dimension must be positive"

        return SparseMatrix({i: {i: 1} for i in range(n)}, w=n, h=n)

    @property
    def num_rows(self) -> int:
        """
        Return the number of rows in the SparseMatrix.

        returns:
            int: The number of rows
        """
        return self._row

    @property
    def num_columns(self) -> int:
        """
        Return the number of columns in the SparseMatrix.

        returns:
            int: The number of columns.
        """
        return self._col

    def __len__(self) -> int:
        """
        Return the horizontal size of the SparseMatrix.

        returns:
            int: The number of columns in the SparseMatrix
        """
        return self._row

    def _get_row(self, i: int) -> SparseVector:  # type: ignore[override]
        assert i < self.num_rows, "index out of range"

        entry = self._entries.get(i, {})

        return SparseVector(entry, self.num_columns)

    def __getitem__(self, i: int) -> SparseVector:  # type: ignore[override]
        return self._get_row(i)

    def __setitem__(self, i: int, v:  # type: ignore[override]
                    Union[SparseVector, List[SCALARS], Dict[int, SCALARS]]
                    ):
        assert i < self.num_rows, "index out of range"
        sv = None
        if isinstance(v, list):
            assert len(v) == self.num_columns, "row dimension does not match"
            sv = SparseVector(v, self.num_rows)
        elif isinstance(v, dict):
            assert max(v.keys()) + 1 < self.num_rows, "row too wide"
            sv = SparseVector(v, self.num_rows)
        else:
            sv = v

        self._entries[i] = sv._entries

    def _as_list(self) -> MATRIX:
        list_representation: MATRIX = [
            [0 for _ in range(self.num_columns)] for _ in range(self.num_rows)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[i][j] = v

        return list_representation

    def get_state(self) -> MATRIX:
        """
        Return the matrix values as a nested list

        returns:
            MATRIX: A nested list of the matrix values indexed by
            row/column
        """
        return self._as_list()

    def rows(self) -> MATRIX:
        """
        Equivalent to get_state().

        returns:
            MATRIX: A nested list of the matrix values indexed by
            row/column
        """
        return self.get_state()

    def columns(self) -> MATRIX:
        """
        The transpose of the matrix as a nested list

        returns:
            MATRIX: A nested list of the matrix values transposed,
            indexed by column/row
        """
        list_representation: MATRIX = [
            [0 for _ in range(self._row)] for _ in range(self._col)
        ]

        for i, row in self._entries.items():
            for j, v in row.items():
                list_representation[j][i] = v

        return list_representation

    def transpose(self) -> SparseMatrix:
        """
        Flips the matrix elements along the diagonal, and return a new
        SparseMatrix containing these values.

        returns:
            SparseMatrix: The transpose of the current matrix.
        """
        entries: SPARSE = {
            k: {} for k in range(self._col)
        }
        for i, row in self._entries.items():
            for j, v in row.items():
                if j not in entries:
                    entries[j] = {i: v}
                else:
                    entries[j][i] = v
        return SparseMatrix(entries, h=self.num_columns, w=self.num_rows)

    def conjugate(self) -> SparseMatrix:
        """
        Create a new SparseMatrix where each value in the matrix is the
        complex conjugate of the current matrix values.

        returns:
            SparseMatrix: A SparseMatrix object of the same dimensions of the
            current matrix, with each value conjugated in place.
        """
        entries = deepcopy(self._entries)
        for i, row in self._entries.items():
            for j, v in row.items():
                if isinstance(v, complex):
                    entries[i][j] = v.conjugate()
                else:
                    entries[i][j] = v
        return SparseMatrix(entries, h=self.num_rows, w=self.num_columns)

    def trace(self) -> SCALARS:
        """
        Calculate the sum of the diagonal elements of the matrix

        returns:
            SCALARS: The sum of all diagonal elements, with type determined
            by the value types.
        """
        assert self.square, "can only take the trace of square matrices"
        tr: SCALARS = 0
        for i in range(self.num_rows):
            if i not in self._entries:
                continue
            if i not in self._entries[i]:
                continue
            tr += self._entries[i][i]

        return tr

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

        if isinstance(other, SCALARS_T):
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

        if isinstance(other, SparseMatrix):
            return self._dot_sparse(other)

        entries: SPARSE = {
            i: {} for i in range(self.num_rows)
        }

        for i, row in self._entries.items():
            for j in range(other.num_columns):
                # only need to calculate using the non-zero entries of self
                # Don't save entries that are ~= 0
                val = sum([other[k][j] * row[k] for k in row.keys()])
                if cmath.isclose(val, 0):
                    continue
                entries[i][j] = val

        return SparseMatrix(entries, w=other.num_columns, h=self.num_rows)

    def _dot_sparse(self, other: SparseMatrix) -> SparseMatrix:
        # Don't need to check dimensions, as the _dot() method has already
        # done it for us.
        entries: SPARSE = {
            i: {} for i in range(self.num_rows)
        }

        other_entries = other._entries

        # Multiply entries in row/columns by each other
        for i, row in self._entries.items():
            for j in range(other.num_columns):

                for k in row.keys():
                    # If the entry doesn't exist in the other
                    # dictionary row/column, skip the entry
                    if k not in other_entries:
                        continue
                    if j not in other_entries[k]:
                        continue
                    # row[k] is guaranteed to be non-zero since we're iterating
                    # over row.keys()
                    val = other_entries[k][j] * row[k]
                    # Don't add on the value if it is ~= 0
                    if cmath.isclose(val, 0):
                        continue

                    if j not in entries[i]:
                        entries[i][j] = val
                    else:
                        entries[i][j] += val

        return SparseMatrix(entries, w=other.num_columns, h=self.num_rows)

    def __str__(self) -> str:
        total_string = ""

        for i in range(self.num_rows):
            row_repr = [
                f"{self[i][j]:3.3g}" for j in range(self.num_columns)]
            total_string += "[" + \
                ",".join(row_repr) + "]"
            # Don't add newline for last row:
            total_string += self._optional_newline(i, self.num_rows)
        return total_string
