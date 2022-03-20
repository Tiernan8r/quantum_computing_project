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
import sys

import pytest
from qcp import cli
from qcp.constants import (ALGORITHM_LONG, ALGORITHM_SHORT, HELP_LONG,
                           HELP_SHORT, PHASE_LONG, PHASE_SHORT, TARGET_LONG,
                           TARGET_SHORT, UNITARY_LONG, UNITARY_SHORT)

DEFAULT_TARGET = 0
DEFAULT_ALGORITHM = "g"
DEFAULT_PHASE = 0.25
DEFAULT_UNITARY = "H"


EXPECTED_USAGE = f"""USAGE:
{sys.argv[0]} [FLAGS] nqbits
FLAGS:
    {ALGORITHM_SHORT}/{ALGORITHM_LONG}  The quantum algorithm to simulate can be one of:
                        g   = Grover's Algorithm
                        pe  = Phase Estimation
                        s   = Toy Sudoku solver
                    Defaults to '{DEFAULT_ALGORITHM}' if unset
    {HELP_SHORT}/{HELP_LONG}       Display this prompt

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
        {PHASE_SHORT}/{PHASE_LONG}      The Phase to use for the Phase Shift Gate (if using).
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
        None
"""  # noqa: E501


def test_usage(capsys):
    with pytest.raises(SystemExit) as se:
        cli.usage()

    assert se.match("0")
    # Capture the output of stdout (the print() statements...)
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_USAGE


def test_parse_cli(capsys):
    # No args provided (except for 'program name') errors with missing number
    # of qbits:
    dummy_args0 = []
    with pytest.raises(SystemExit) as se0:
        cli.parse_cli(dummy_args0)
    assert se0.match("1")
    captured0 = capsys.readouterr()
    assert "Must provide the number of qbits to simulate" in captured0.err

    # Non-integer qbits number:
    dummy_args1 = ["ten"]
    with pytest.raises(SystemExit) as se1:
        cli.parse_cli(dummy_args1)
    assert se1.match("1")
    captured1 = capsys.readouterr()
    assert "Provided number of qbits 'ten' is not an integer!" in captured1.err

    # "-h" or "--help" shows usage:
    dummy_args2_1 = ["-h"]
    with pytest.raises(SystemExit) as se2_1:
        cli.parse_cli(dummy_args2_1)
    assert se2_1.match("0")
    captured2_1 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_1.out

    dummy_args2_2 = ["--help"]
    with pytest.raises(SystemExit) as se2_2:
        cli.parse_cli(dummy_args2_2)
    assert se2_2.match("0")
    captured2_2 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_2.out

    # --target must be an integer:
    dummy_args3 = ["-t", "one", "2"]
    with pytest.raises(SystemExit) as se3:
        cli.parse_cli(dummy_args3)
    assert se3.match("1")
    captured3 = capsys.readouterr()
    assert "Provided target 'one' is not an integer" in captured3.err

    # Values are read correctly:
    dummy_args4 = ["-t", "1", "2"]
    opt, (n4, t4) = cli.parse_cli(dummy_args4)
    assert opt.value == "g"
    assert n4 == 2
    assert t4 == 1
