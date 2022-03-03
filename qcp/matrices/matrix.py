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
        pass

    @property
    def num_columns(self) -> int:
        pass

    def __getitem__(self, i: int) -> VECTOR:
        pass

    def __setitem__(self, i: int, v: VECTOR):
        pass

    def get_state(self) -> MATRIX:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __sub__(self, other: Matrix) -> Matrix:
        pass

    def columns(self) -> MATRIX:
        pass

    def transpose(self) -> Matrix:
        pass

    def conjugate(self) -> Matrix:
        pass

    def adjoint(self) -> Matrix:
        """
        Shortcut operation to calculate the transpose and conjugate of the
        current matrix.
        """
        return self.transpose().conjugate()

    def __mul__(self, other: Union[SCALARS, Matrix]) -> Matrix:
        pass

    def __rmul__(self, other: Union[SCALARS, Matrix]) -> Matrix:
        return self.__mul__(other)

    def __str__(self) -> str:
        pass
