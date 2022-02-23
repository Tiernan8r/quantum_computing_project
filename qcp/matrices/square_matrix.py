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
from typing import List, Union


class SquareMatrix(Matrix):

    def __init__(self, state: List[List[Union[complex, float]]]):
        self._state = state

    def __len__(self) -> int:
        return len(self._state)

    def __getitem__(self, i: int) -> List[Union[complex, float]]:
        assert i < len(self), "index out of range"
        return self._state[i]

    def __setitem__(self, i: int, v: List[Union[complex, float]]):
        assert i < len(self), "index out of range"
        assert len(v) == len(self), "row dimension does not match"

        self._state[i] = v

    def get_state(self) -> List[List[Union[complex, float]]]:
        return self._state

    def set_state(self, s: List[List[Union[complex, float]]]):
        assert s is not None
        assert len(s) > 0
        assert len(s) == len(s[0]), "non square matrix state"
        self._state = s

    def rows(self) -> List[List[Union[complex, float]]]:
        """Return the rows of the Matrix."""
        return self.get_state()

    def columns(self) -> List[List[Union[complex, float]]]:
        """Returns the columns of the Matrix"""
        return [
            [self._state[i][j] for i in range(len(self))]
            for j in range(len(self))
        ]

    def __iter__(self):
        return iter(self.get_state())

    def __add__(self, other: Matrix) -> Matrix:
        assert len(self) == len(other) and len(self[0]) == len(
            other[0]), "Matrix dimensions must be equal for addition"

        current_state = self.get_state().copy()

        for i in range(len(self)):
            for j in range(len(self[i])):
                current_state[i][j] += other[i][j]

        return SquareMatrix(current_state)

    def __sub__(self, other: Matrix) -> Matrix:
        return self + (other * -1)

    def __mul__(self, other: Union[complex, float, int, Matrix]) -> Matrix:

        if isinstance(other, (complex, float, int)):
            current_state = self.get_state().copy()

            for i in range(len(current_state)):
                for j in range(len(current_state[i])):
                    current_state[i][j] *= other

            return SquareMatrix(current_state)

        elif isinstance(other, Matrix):
            return self._dot(other)

    def _dot(self, other: Matrix) -> Matrix:
        n = len(self)
        current_state = [[0 for i in range(n)] for j in range(n)]

        for i in range(n):
            for j in range(n):
                current_state[i][j] = sum([self[i][k] * other[k][j] for k in range(n)])

        return SquareMatrix(current_state)

    def __str__(self) -> str:
        total_string = ""
        N = len(self._state)
        for i in range(N):
            total_string += "[" + \
                ",".join([f"{c:2d}" for c in self._state[i]]) + "]" + \
                (lambda i, N: "\n" if i < N - 1 else "")(i, N)
        return total_string
