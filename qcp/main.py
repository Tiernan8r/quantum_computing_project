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
from qcp.grovers_algorithm import Grovers
from typing import List, Tuple
import sys

#: The default target state the Oracle will search for
TARGET_DEF = 5
#: The CLI help text
USAGE_STR = f"""USAGE:
{sys.argv[0]} [FLAGS] nqbits

ARGS:
    nqbits          The number of qbit states to simulate
FLAGS:
    -t/--target     The target state, defaults to {TARGET_DEF}
    -h/--help       Display this prompt"""


def main():
    """
    The entrypoint for the CLI, parses the cli options and passes the read
    options to the function to run the computation.
    """
    nqbits, target = parse_cli(sys.argv)
    assert nqbits > 1, "must have a minimum of a 2 qbit state"

    compute(nqbits, target)


def usage():
    """
    Prints the help text to stdout, and exits with error code 0.
    """
    print(USAGE_STR)
    exit(0)


def parse_cli(args: List[str]) -> Tuple[int, int]:
    """
    Parses the sys.argv CLI options to read the value for the optional flags
    (if provided), and the required CLI arguments.

    :param args List[str]: The list of CLI inputs from sys.argv
    :returns Tuple[int, int]: The two CLI values,
        firstly the required 'nqbits' parameter,
        and the second optional 'target' parameter.
    """
    num_args = len(args)
    vals = []
    targ = TARGET_DEF

    # ignore the 1st arg as it is the program name
    i = 1
    while i < num_args:
        arg = args[i]
        if arg == "-h" or arg == "--help":
            usage()
        elif arg == "-t" or arg == "--target":
            if i + 1 > num_args:
                print("Must provide a target value!", file=sys.stderr)
                exit(1)
            try:
                targ = int(args[i+1])
            except ValueError:
                print("target state must be an integer", file=sys.stderr)
                exit(1)
            i += 1
        # Falls into the everything else category
        else:
            vals.append(arg)
        i += 1

    nqbits = 1
    if len(vals) > 0:
        try:
            nqbits = int(vals[0])
        except ValueError:
            print("number of qbits must be an integer", file=sys.stderr)
            exit(1)
    else:
        print("Must provide the number of qbits to simulate", file=sys.stderr)
        exit(1)

    return (nqbits, targ)


def compute(nqbits: int, target: int):
    """
    Run the Grover's Algorithm simulation and print the observed state to
    stdout with the probability of observing that state.

    :param int nqbits: The number of qbits to simulate in the simulator
    :param int target: The index of the target qbit state
    """
    grover = Grovers(nqbits, target)
    grover.run()

    m, p = grover.measure()
    print("Observed state: |" + bin(m)[2:] + ">")
    print("With probability: " + str(p))


if __name__ == "__main__":
    main()
