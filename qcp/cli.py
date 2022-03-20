#!/usr/bin/env python
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
CLI initialiser to parse CLI options for the Algorithm, and to run the
computation
"""
import re
import sys
from typing import Dict, List, Tuple

from qcp.algorithms.options import AlgorithmOption, UnitaryMatrices
from qcp.constants import (ALGORITHM_LONG, ALGORITHM_SHORT, FLAG_MAPPING,
                           HELP_LONG, HELP_SHORT, PHASE_LONG, PHASE_SHORT,
                           TARGET_LONG, TARGET_SHORT, UNITARY_LONG,
                           UNITARY_SHORT)
from qcp.matrices import DefaultMatrix, Matrix

#: The default target state the Oracle will search for
DEFAULT_TARGET = 0
DEFAULT_ALGORITHM = "g"
DEFAULT_PHASE = 0.25
DEFAULT_UNITARY = "H"

#: The CLI help text
USAGE_STR = f"""USAGE:
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
        None"""  # noqa: E501


def usage():
    """
    Prints the help text to stdout, and exits with error code 0.
    """
    print(USAGE_STR)
    exit(0)


def parse(args: List[str]) -> Tuple[Dict[str, str], List[str]]:
    d = {}  # Map the flags to the values in a dictionary
    v = []  # Store all unmapped values in a list

    flag_short_pattern = re.compile("-.+")
    flag_long_pattern = re.compile("--.+")

    n = len(args)
    i = 0
    while i < n:
        arg = args[i]

        if (flag_short_pattern.match(arg) or flag_long_pattern.match(arg)):
            val = ""
            if i + 1 < n:
                val = args[i+1]

            # Convert the short flag names to the long ones
            if arg in FLAG_MAPPING:
                arg = FLAG_MAPPING[arg]

            if arg in d:
                print(
                    f"Duplicate flag '{arg}' detected, skipping...",
                    file=sys.stderr)
                i += 2
                continue
            d[arg] = val
            i += 2
        else:
            v.append(arg)
            i += 1

    return d, v


def determine(opt: AlgorithmOption, args: List[str], flags: Dict[str, str]):
    if opt is AlgorithmOption.Grovers:
        return determine_grover(args, flags)
    elif opt is AlgorithmOption.PhaseEstimation:
        return determine_phase_estimation(args, flags)
    elif opt is AlgorithmOption.Sudoku:
        return determine_sudoku(args, flags)

    return None


def determine_grover(args: List[str], flags: Dict[str, str]
                     ) -> Tuple[int, int]:
    # Determine the number of qbits
    if len(args) < 1:
        print("Must provide the number of qbits to simulate", file=sys.stderr)
        exit(1)
    elif len(args) > 1:
        print("Too many arguments provided, discarding excess...",
              file=sys.stderr)

    nqbits_str = args[0]
    nqbits = 2
    try:
        nqbits = int(nqbits_str)
    except ValueError:
        print(
            f"Provided number of qbits '{nqbits_str}' is not an integer!",
            file=sys.stderr)
        exit(1)

    if nqbits < 2:
        print("Number of qbits to simulate must be >= 2!", file=sys.stderr)

    # Read the target value from the flag
    target = DEFAULT_TARGET
    if TARGET_LONG not in flags:
        print(
            f"No target bit provided, defaulting to {DEFAULT_TARGET}",
            file=sys.stderr)
    else:
        target_str = flags[TARGET_LONG]

        try:
            target = int(target_str)
        except ValueError:
            print(
                f"Provided target '{target_str}' is not an integer!",
                file=sys.stderr)
            exit(1)

    return nqbits, target


def determine_phase_estimation(args: List[str], flags: Dict[str, str]
                               ) -> Tuple[int, Matrix, Matrix]:
    # Determining the number of qbits:
    if len(args) < 1:
        print("Must provide the number of qbits to simulate", file=sys.stderr)
        exit(1)
    elif len(args) > 1:
        print("Too many arguments provided, discarding excess...",
              file=sys.stderr)

    nqbits_str = args[0]
    nqbits = 2
    try:
        nqbits = int(nqbits_str)
    except ValueError:
        print(
            f"Provided number of qbits '{nqbits_str}' is not an integer!",
            file=sys.stderr)
        exit(1)

    if nqbits < 2:
        print("Number of qbits to simulate must be >= 2!", file=sys.stderr)

    # Determine the phase shift to use:
    phase = DEFAULT_PHASE
    if PHASE_LONG in flags:
        phase_str = flags[PHASE_LONG]

        try:
            phase = float(phase_str)
        except ValueError:
            print(
                f"Provided phase '{phase_str}' is not a number!",
                file=sys.stderr)
            exit(1)

    # Determining the unitary matrix
    unitary_str = DEFAULT_UNITARY
    unitary_matrix = UnitaryMatrices(DEFAULT_UNITARY)
    if UNITARY_LONG not in flags:
        print(
            f"No unitary matrix type provided, defaulting to '{unitary_str}'",
            file=sys.stderr)
    else:
        unitary_str = flags[UNITARY_LONG].upper()

        if unitary_str not in UnitaryMatrices.list():
            err_str = "Unitary matrix option '{0}' is not a valid option!"
            print(
                err_str.format(unitary_str),
                file=sys.stderr)
            print(
                f"The options are: {UnitaryMatrices.list()}", file=sys.stderr)
            exit(1)

        unitary_matrix = UnitaryMatrices(unitary_str)

    # Determining the Eigenvector to use
    eigenvec = DefaultMatrix([[0], [1]])

    return nqbits, unitary_matrix.get(phase), eigenvec


def determine_sudoku(args: List[str], flags: Dict[str, str]):
    return


def parse_cli(args: List[str]):
    """
    Parses the sys.argv CLI options to read the value for the optional flags
    (if provided), and the required CLI arguments.

    :param List[str] args: The list of CLI inputs from sys.argv
    returns:
        Tuple[int, int, ~:py:obj:qcp.constants.AlgorithmOptions]: The CLI
        values, firstly the required 'nqbits' parameter, and the second
        optional 'target' parameter.
    """
    flags, vals = parse(args)

    if HELP_LONG in flags:
        usage()

    alg_opt_str = DEFAULT_ALGORITHM
    if ALGORITHM_LONG in flags:
        alg_opt_str = flags[ALGORITHM_LONG]

    if alg_opt_str not in AlgorithmOption.list():
        print(
            f"Algorithm option '{alg_opt_str}' is not a valid option!",
            file=sys.stderr)
        print(f"The options are: {AlgorithmOption.list()}", file=sys.stderr)
        exit(1)

    alg_opt = AlgorithmOption(alg_opt_str)

    if TARGET_LONG not in flags:
        flags[TARGET_LONG] = str(DEFAULT_TARGET)

    return alg_opt, determine(alg_opt, vals, flags)
