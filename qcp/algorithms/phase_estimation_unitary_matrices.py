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
"""
Defines the enum that encodes the predefined Unitary matrices
"""
import cmath
import enum
from typing import Tuple

import qcp.constants as c
from qcp.matrices import DefaultMatrix, Matrix


class UnitaryMatrices(enum.Enum):
    """
    Enum of all the available unitary matrices to use in the Phase
    Estimation algorithm
    """
    # TODO: Populate properly
    HADAMARD = "hadamard"
    PHASE_SHIFT = "phase_shift"

    @classmethod
    def list(cls):
        """
        Return all the enum options' values

        returns:
            List[str]: All the strings the enums correspond to
        """
        return list(map(lambda um: um.value, cls))  # type: ignore

    def get(self, val1: float = 0.0, val2: float = 0.0) -> Matrix:
        """
        Get the actual Unitary Matrix the enum corresponds to

        :param float val: Optional value required when creating certain
            matrix types

        returns:
            Matrix: The Unitary Matrix
        """
        if self is UnitaryMatrices.HADAMARD:
            return c.TWO_HADAMARD
        elif self is UnitaryMatrices.PHASE_SHIFT:
            phi1 = cmath.exp(2j * cmath.pi * val1)
            phi2 = cmath.exp(2j * cmath.pi * val2)
            return DefaultMatrix([[phi1, 0], [0, phi2]])

        return None

    def basis_names(self) -> Tuple[str, str]:
        """
        Return the basis names used for the Unitary matrix choice

        returns:
            Tuple[str, str]: A two entry tuple of the 2 qbit
                basis names.
        """
        if self is UnitaryMatrices.HADAMARD:
            return "|+>", "|->"
        elif self is UnitaryMatrices.PHASE_SHIFT:
            return "|0>", "|1>"
        else:
            return ()

    def basis(self) -> Tuple[Matrix, Matrix]:
        """
        Return the basis used for the Unitary matrix choice

        returns:
            Tuple[Matrix, Matrix]: A two entry tuple of the 2 qbit
                basis.
        """
        if self is UnitaryMatrices.HADAMARD:
            return c.PLUS_VECTOR, c.MINUS_VECTOR
        elif self is UnitaryMatrices.PHASE_SHIFT:
            return c.ZERO_VECTOR, c.ONE_VECTOR
        else:
            return ()
