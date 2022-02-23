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
from typing import Union
from . import Matrix


class SquareMatrix(Matrix):

    def __init__(self, state):
        self._state = state

    def __len__(self):
        return len(self._state)

    def __getitem__(self, i):
        return self._state[i]

    def set_state(self, s: list):
        pass

    def get_state(self) -> list:
        return self._state

    def __add__(self, other: Matrix):
        pass

    def __sub__(self, other: Matrix):
        pass

    def __mul__(self, other: Union[float, Matrix]):
        pass

    def __str__(self):
        total_string = ""
        for i in range(len(self._state)):
            row_string = "["
            for j in range(len(self._state[i])):
                row_string += f"{self._state[i][j]:2d},"
            row_string += "]\n"
            total_string += row_string
        return total_string
