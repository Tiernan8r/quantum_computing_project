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
from typing import List, Union


class Matrix(ABC):

    def __init__(self, state: List[List[float]]):
        pass

    def __len__(self) -> int:
        pass

    def __getitem__(self, i: int) -> List[float]:
        pass

    def __setitem__(self, i: int, v: float):
        pass

    def set_state(self, s: List[List[float]]):
        pass

    def get_state(self) -> List[List[float]]:
        pass

    def __add__(self, other: Matrix):
        pass

    def __sub__(self, other: Matrix):
        pass

    def __mul__(self, other: Union[float, Matrix]):
        pass
