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
import multiprocessing
import os
import sys

# Required to guarantee that the 'qcp' module is accessible when
# this file is run directly.
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import qcp.cli as cli
from qcp.algorithms import GeneralAlgorithm
import qcp.cli.progress_bar as pb


def main():
    """
    The entrypoint for the CLI, parses the cli options and passes the read
    options to the function to run the computation.
    """
    # Ignore the first entry in sys.argv as it is just the program name
    alg_opt, parsed_tuple = cli.read_cli(sys.argv[1:])

    compute(alg_opt.get_constructor(), alg_opt.get_name(), *parsed_tuple)


def compute(constructor, alg_name, *args):
    """
    Run the Grover's Algorithm simulation and print the observed state to
    stdout with the probability of observing that state.

    :param int nqbits: The number of qbits to simulate in the simulator
    :param int target: The index of the target qbit state
    """
    print(f"Simulating {alg_name} Algorithm...")

    # Start up the progress bar ticker
    progress_ticker = threaded_progress_bar()

    alg: GeneralAlgorithm = None
    try:
        alg = constructor(*args)
        alg.run()
    except AssertionError as ae:
        print(ae, file=sys.stderr)
        exit(1)

    # Stop the ticker before printing the results
    progress_ticker.terminate()

    m, p = alg.measure()

    print("Observed state: |" + bin(m)[2:] + ">")
    print("With probability: " + str(p))


def threaded_progress_bar() -> multiprocessing.Process:
    ticker_process = multiprocessing.Process(
        target=pb.ticker,
        args=(0.5, "Simulating: ",)
    )
    ticker_process.start()

    return ticker_process


if __name__ == "__main__":
    main()
