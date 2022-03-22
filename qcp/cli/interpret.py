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
Convert the given CLI arguments and flags into usable input for the algorithms
"""
import sys
from typing import Dict, List, Tuple

from qcp.cli.constants import (DEFAULT_PHASE, DEFAULT_TARGET, DEFAULT_UNITARY,
                               PHASE_LONG, TARGET_LONG, UNITARY_LONG)
from qcp.cli.options import AlgorithmOption
from qcp.algorithms.phase_estimation_unitary_matrices import UnitaryMatrices
from qcp.matrices import DefaultMatrix, Matrix


def interpret_arguments(opt: AlgorithmOption,
                        args: List[str],
                        flags: Dict[str, str]):
    """
    Parse the CLI arguments/flags based off of the algorithm
    type to simulate

    :param AlgorithmOption opt: The algorithm chosen
    :param List[str]: The CLI arguments provided
    :param Dict[str, str]: The CLI flags provided
    """
    if opt is AlgorithmOption.Grovers:
        return determine_grover(args, flags)
    elif opt is AlgorithmOption.PhaseEstimation:
        return determine_phase_estimation(args, flags)
    elif opt is AlgorithmOption.Sudoku:
        return determine_sudoku(args, flags)

    return ()


def _determine_qbits(args: List[str]) -> int:
    """
    Read the number of qbits to simulate from the CLI arguments list

    :param List[str] args: The CLI arguments

    returns:
        int: The number of qbits
    """
    # Determine the number of qbits
    if len(args) < 1:
        print("Must provide the number of qbits to simulate", file=sys.stderr)
        exit(1)
    elif len(args) > 1:
        print("Too many arguments provided, ignoring extras...",
              file=sys.stderr)

    # Take the number to interpret to be the first value in the arguments
    # list
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
        exit(1)

    return nqbits


def determine_grover(args: List[str], flags: Dict[str, str]
                     ) -> Tuple[int, int]:
    """
    Read the given flags dictionary and arguments map and convert to usable
    input for the Grover's algorithm.

    The Grover's Algorithm needs two input. The first is the number of
    qbits to simulate, and the second is the target state to search for.

    :param List[str] args: The CLI arguments
    :param Dict[str,str] flags: The CLI flags

    returns:
        Tuple[int, int]: Tuple of the parameters for the constructor, the
            first is the number of qbits, the second the target bit.
    """
    # Determine the number of qbits
    nqbits = _determine_qbits(args)

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
    """
    Read the given flags dictionary and arguments map and convert to usable
    input for the PhaseEstimation algorithm.

    The PhaseEstimation algorithm needs the number of qbits to simulate,
    and two matrices. The first to use as the unitary matrix in the algorithm
    and the second to use as the eigenvector.

    :param List[str] args: The CLI arguments
    :param Dict[str,str] flags: The CLI flags

    returns:
        Tuple[int, Matrix, Matrix]: Tuple of the parameters for the
            constructor, the first is the number of qbits to simulate,
            the second the Unitary Matrix to use, and the third the
            eigenvector.
    """
    # Determine the number of qbits:
    nqbits = _determine_qbits(args)

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
    """
    Read the given flags dictionary and arguments map and convert to usable
    input for the Sudoku algorithm.

    The sudoku algorithm takes no input...

    :param List[str] args: The CLI arguments
    :param Dict[str,str] flags: The CLI flags
    """
    return ()
