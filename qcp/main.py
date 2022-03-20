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

# Required to make sure the module 'qcp' is accessible when the
# main.py file is run directly
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import qcp.cli as cli
from qcp.algorithms import GeneralAlgorithm, Grovers, PhaseEstimation, Sudoku
from qcp.cli.options import AlgorithmOption
import qcp.cli.progress_bar as pb
from qcp.matrices import Matrix


def main():
    """
    The entrypoint for the CLI, parses the cli options and passes the read
    options to the function to run the computation.
    """
    # Ignore the first entry in sys.argv as it is just the program name
    alg_opt, parsed_tuple = cli.read_cli(sys.argv[1:])

    if alg_opt is AlgorithmOption.Grovers:
        compute_grovers(*parsed_tuple)
    elif alg_opt is AlgorithmOption.PhaseEstimation:
        compute_phase_estimation(*parsed_tuple)
    elif alg_opt is AlgorithmOption.Sudoku:
        compute_sudoku()
    else:
        print("D'oh!")  # This is an impossible scenario...


def compute_grovers(nqbits: int, target: int):
    """
    Run the Grover's Algorithm simulation and print the observed state to
    stdout with the probability of observing that state.

    :param int nqbits: The number of qbits to simulate in the simulator
    :param int target: The index of the target qbit state
    """
    print("Simulating Grover's Algorithm...")

    # Start up the progress bar ticker
    progress_ticker = threaded_progress_bar()

    try:
        grover = Grovers(nqbits, target)
        threaded_compute(grover)
    except AssertionError as ae:
        print(ae, file=sys.stderr)

    # Stop the ticker before printing the results
    progress_ticker.terminate()

    m, p = grover.measure()

    print("Observed state: |" + bin(m)[2:] + ">")
    print("With probability: " + str(p))


def compute_phase_estimation(nqbits: int, unitary: Matrix, eigenvec: Matrix):
    """
    Run the Phase Estimation Algorithm simulation and print the observed state
    to stdout with the probability of observing that state.

    :param int nqbits: The number of qbits to simulate in the simulator
    :param Matrix unitary: The unitary matrix to use in the algorithm
    :param Matrix eigenvec: The eigenvector to use in the algorithm
    """
    print("Simulating the Phase Estimation Algorithm...")

    # Start up the progress bar ticker
    progress_ticker = threaded_progress_bar()

    try:
        phase_est = PhaseEstimation(nqbits, unitary, eigenvec)
        threaded_compute(phase_est)
    except AssertionError as ae:
        print(ae, file=sys.stderr)

    # Stop the ticker before printing the results
    progress_ticker.terminate()

    m, p = phase_est.measure()

    print("Observed state: |" + bin(int(m))[2:] + ">")
    print("With probability: " + str(p))


def compute_sudoku():
    """
    Run the Sudoku simulation and print the observed state to
    stdout with the probability of observing that state.
    """
    print("Beginning the Sudoku solver simulation...")

    # Start up the progress bar ticker
    progress_ticker = threaded_progress_bar()

    try:
        sudoku = Sudoku()
        threaded_compute(sudoku)
    except AssertionError as ae:
        print(ae, file=sys.stderr)

    # Stop the ticker before printing the results
    progress_ticker.terminate()

    m, p = sudoku.measure()

    print("Observed state: |" + bin(m)[2:] + ">")
    print("With probability: " + str(p))


def threaded_compute(alg: GeneralAlgorithm):

    def comp(alg):
        alg.run()

    thread = multiprocessing.Process(target=comp, args=(alg,))
    thread.start()

    return thread


def threaded_progress_bar() -> multiprocessing.Process:
    ticker_process = multiprocessing.Process(
        target=pb.ticker,
        args=(0.5, "Simulating: ",)
    )
    ticker_process.start()

    return ticker_process


if __name__ == "__main__":
    main()
