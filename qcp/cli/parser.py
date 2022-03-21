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
Code to parse CLI options for the Algorithm, to determing the flags and
arguments given
"""
import re
import sys
from typing import Dict, List, Tuple

import qcp.cli.interpret as i
import qcp.cli.usage as u
from qcp.cli.constants import (ALGORITHM_LONG, DEFAULT_ALGORITHM,
                               DEFAULT_TARGET, FLAG_MAPPING, HELP_LONG,
                               TARGET_LONG)
from qcp.cli.options import AlgorithmOption


def parse_input(args: List[str]) -> Tuple[Dict[str, str], List[str]]:
    """
    Convert the given list of cli arguments into a mapping between the
    CLI flags and their value, and a list or CLI arguments

    :param List[str] args: The CLI arguments

    returns:
        Tuple[Dict[str, str], List[str]]: A tuple of the flags dictionary
            and the arguments list.
    """
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


def read_cli(args: List[str]):
    """
    Parses the sys.argv CLI options to read the value for the optional flags
    (if provided), and the required CLI arguments.

    :param List[str] args: The list of CLI inputs from sys.argv
    returns:
        Tuple[~:py:obj:qcp.cli.constants.AlgorithmOptions, Any...]: The CLI
            values, firstly the algorithm chosen to run, and then a tuple of
            the parameters required to run that algorithm.
    """
    flags, vals = parse_input(args)

    if HELP_LONG in flags:
        u.usage()

    if ALGORITHM_LONG not in flags:
        flags[ALGORITHM_LONG] = DEFAULT_ALGORITHM

    alg_opt_str = flags[ALGORITHM_LONG]

    # Show the help message on no args provided, but only if sudoku algorithm
    # not chosen
    if len(vals) == 0 and flags[ALGORITHM_LONG] != "s":
        u.usage()

    if alg_opt_str not in AlgorithmOption.list():
        print(
            f"Algorithm option '{alg_opt_str}' is not a valid option!",
            file=sys.stderr)
        print(f"The options are: {AlgorithmOption.list()}", file=sys.stderr)
        exit(1)

    alg_opt = AlgorithmOption(alg_opt_str)

    if TARGET_LONG not in flags:
        flags[TARGET_LONG] = str(DEFAULT_TARGET)

    return alg_opt, i.interpret_arguments(alg_opt, vals, flags)
