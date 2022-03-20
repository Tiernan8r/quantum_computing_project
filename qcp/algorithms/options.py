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
import enum
from typing import Type, Union

from qcp.algorithms import Grovers, PhaseEstimation, Sudoku


class AlgorithmOptions(enum.Enum):
    """
    Enum of the different algorithms to simulate
    """

    Grovers = "g"
    PhaseEstimation = "pe"
    Sudoku = "s"

    def get_constructor(self) -> Union[
        Type[Grovers], Type[PhaseEstimation], Type[Sudoku], None
    ]:

        if self is AlgorithmOptions.Grovers:
            return Grovers

        elif self is AlgorithmOptions.PhaseEstimation:
            return PhaseEstimation

        elif self is AlgorithmOptions.Sudoku:
            return Sudoku
