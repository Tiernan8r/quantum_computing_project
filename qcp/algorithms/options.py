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
import cmath
import enum
from typing import List, Type, Union

import qcp.constants as c
from qcp.algorithms import Grovers, PhaseEstimation, Sudoku
from qcp.matrices import DefaultMatrix, Matrix


class AlgorithmOption(enum.Enum):
    """
    Enum of the different algorithms to simulate
    """

    Grovers = "g"
    PhaseEstimation = "pe"
    Sudoku = "s"

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda ao: ao.value, cls))

    def get_constructor(self) -> Union[
        Type[Grovers], Type[PhaseEstimation], Type[Sudoku], None
    ]:

        if self is AlgorithmOption.Grovers:
            return Grovers

        elif self is AlgorithmOption.PhaseEstimation:
            return PhaseEstimation

        elif self is AlgorithmOption.Sudoku:
            return Sudoku


class UnitaryMatrices(enum.Enum):
    # TODO: Populate properly
    HADAMARD = "H"
    PHASE_SHIFT = "P"

    @classmethod
    def list(cls):
        return list(map(lambda um: um.value, cls))

    def get(self, val: float = 0.0) -> Matrix:
        if self is UnitaryMatrices.HADAMARD:
            return c.TWO_HADAMARD
        elif self is UnitaryMatrices.PHASE_SHIFT:
            return DefaultMatrix([[1, 0], [0, cmath.exp(2j*cmath.pi*val)]])

        return None
