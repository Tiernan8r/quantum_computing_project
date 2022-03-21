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
CLI help messages live here
"""
import sys

from qcp.cli.constants import (ALGORITHM_LONG, ALGORITHM_SHORT,
                               DEFAULT_ALGORITHM, DEFAULT_PHASE,
                               DEFAULT_TARGET, DEFAULT_UNITARY, GUI_LONG, GUI_SHORT, HELP_LONG,
                               HELP_SHORT, PHASE_LONG, PHASE_SHORT,
                               TARGET_LONG, TARGET_SHORT, UNITARY_LONG,
                               UNITARY_SHORT)

#: The CLI help text
USAGE_STR = f"""USAGE:
{sys.argv[0]} [FLAGS] nqbits
FLAGS:
    {ALGORITHM_SHORT}/{ALGORITHM_LONG}  The quantum algorithm to simulate, can be one of:
                        g   = Grover's Algorithm
                        pe  = Phase Estimation
                        s   = Toy Sudoku solver
                    Defaults to '{DEFAULT_ALGORITHM}' if unset
    {HELP_SHORT}/{HELP_LONG}       Display this prompt
    {GUI_SHORT}/{GUI_LONG}      Display the GUI.

The CLI options vary by choice of algorithm:

GROVERS:
    USAGE:
    {sys.argv[0]} {ALGORITHM_LONG} g [FLAGS] nqbits
    ARGS:
        nqbits          The number of qbit states to simulate, must be >= 2.
    FLAGS:
        {TARGET_SHORT}/{TARGET_LONG}     The target state, defaults to {DEFAULT_TARGET}

PHASE ESTIMATION:
    USAGE:
    {sys.argv[0]} {ALGORITHM_LONG} pe [FLAGS] nqbits
    ARGS:
        nqbits          The number of qbit states to simulate, must be >= 2.
    FLAGS:
        {PHASE_SHORT}/{PHASE_LONG}      The phase to use for the Phase Shift Gate (if using).
                        defaults to {DEFAULT_PHASE}.
        {UNITARY_SHORT}/{UNITARY_LONG}    The choice of unitary gate to simulate with, can be
                        one of the following:
                            * H = Hadamard Gate
                            * P = Phase Shift Gate (requires the {PHASE_SHORT} flag)
                        Defaults to '{DEFAULT_UNITARY}' if unset
SUDOKU:
    USAGE:
    {sys.argv[0]} {ALGORITHM_LONG} s
    ARGS:
        None
    FLAGS:
        None"""  # noqa: E501


def usage():
    """
    Prints the help text to stdout, and exits with error code 0.
    """
    print(USAGE_STR)
    exit(0)
