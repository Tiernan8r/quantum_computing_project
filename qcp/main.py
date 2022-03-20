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
Entrypoint for the Simulator
"""
import sys
import os

# Required to make sure the module 'qcp' is accessible when the
# main.py file is run directly
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import qcp.cli as cli
from qcp.algorithms.grovers_algorithm import Grovers

def main():
    """
    The entrypoint for the CLI, parses the cli options and passes the read
    options to the function to run the computation.
    """
    nqbits, target = cli.parse_cli(sys.argv)
    assert nqbits > 1, "must have a minimum of a 2 qbit state"

    compute(nqbits, target)


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
