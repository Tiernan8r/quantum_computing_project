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
from ._types import SCALARS, VECTOR, MATRIX
from typing import List, Union


class _Entry:

    def __init__(self, i: int, j: int, val: SCALARS, next: _Entry):
        self._row = i
        self._col = j
        self._value = val
        self.next = next

    def __iter__(self) -> _Entry:
        return self

    def __next__(self) -> _Entry:
        if self.next is None:
            raise StopIteration
        else:
            return self.next


class SparseVector:
    """A subset of the SparseMatrix containing only entries found in a row"""

    def __init__(self, entries: List[_Entry], size: int):
        self._start, self._end = None, None
        self._size = size

        # all _Entry types in entries are assumed to be correctly linked already
        if len(entries) > 0:
            self._start = entries[0]
            self._end = entries[-1]

    def __len__(self):
        return self._size

    def __iter__(self):
        return self._start


class SparseMatrix(Matrix):

    def __init__(self, state: MATRIX):
        self._start, self._end = None, None

        n = len(state)
        m = 0
        if n > 0:
            m = len(state[0])
        self._row = n
        self._col = m

        for i in range(len(state)):
            for j in range(len(state[i])):
                entry = state[i][j]

                # ignore floating points that are within 1e-9 to 0
                if cmath.isclose(entry, 0):
                    continue

                tmp = _Entry(i, j, entry, None)
                if self._start is None:
                    self._start = tmp
                    self._end = tmp
                else:
                    self._end.next = tmp
                    self._end = tmp

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

        I = SparseMatrix([[1]])  # initialise as 1x1 to begin with
        for i in range(n):
            node = _Entry(i, i, 1, None)
            I._end.next = node
            I._end = node

        return I

    def __len__(self) -> int:
        return self._row

    def _get_row(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"

        entries = []
        for itr in self._start:
            if itr._row == i:
                entries.append(itr)

        return SparseVector(entries, self._row)

    def __getitem__(self, i: int) -> SparseVector:
        assert i < len(self), "index out of range"
        return self._get_row(i)

    def __setitem__(self, i: int, v: SparseVector):
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        for itr in self._start:
            # ignore all existing entries not referencing the desired row to modify
            current_next = itr.next
            if current_next._row != i:
                continue

            prev_row = itr

            # Find where the row after the one we're modifying starts
            next_row = current_next.next
            while next_row._row == i:
                next_row = next_row.next

            prev_row.next = v._start
            v._end.next = next_row

    def _as_list(self) -> Matrix():
        list_representation = [
            [0 for i in range(self._row)] for j in range(self._col)
        ]

        for e in self._start:
            list_representation[e._row][e._col] = e._value

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
        pass

    def __iter__(self):
        return iter(self._start)

    def __add__(self, other: Matrix) -> Matrix:
        assert self._row == len(other) and self._other == len(
            other[0]), "Matrix dimensions must be equal for addition"

        current_state = self.get_state().copy()

        for i in range(len(self)):
            for j in range(len(self[i])):
                current_state[i][j] += other[i][j]

        return SparseMatrix(current_state)

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (other * -1)

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:

        if isinstance(other, (complex, float, int)):
            current_state = self.get_state().copy()

            for i in range(len(current_state)):
                for j in range(len(current_state[i])):
                    current_state[i][j] *= other

            return SquareMatrix(current_state)

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

        return SquareMatrix(current_state)

    def __str__(self) -> str:
        total_string = ""
        N = len(self._state)
        for i in range(N):
            total_string += "[" + \
                ",".join([f"{c:3.3g}" for c in self._state[i]]) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, N)
        return total_string
