# Quantum Computing Project:

[![Tox](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/tox.yml/badge.svg)](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/tox.yml)
[![CodeQL](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/codeql-analysis.yml)
[![Pages](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://github.com/Tiernan8r/quantum_computing_project/actions/workflows/sphinx_docs_to_gh_pages.yaml)

An implementation of a quantum computer simulator in Python to simulate the 
running of [Grover's Algorithm](https://qiskit.org/textbook/ch-algorithms/grover.html).

## Table of Contents:

* [Setup](#setup)
    * [Clone the Repository](#clone-the-repository)
    * [Optional - Run Tests](#optional---run-tests)
* [CLI](#cli-usage)
* [GUI](#gui)
    * [Search Input](#search-input)
    * [Target](#target)
    * [Search Button](#search-button)

## Setup:

To get started with the repository, you need to do the following:

### Clone the Repository:
Clone the repository to your system:
```console
$ git clone https://github.com/Tiernan8r/quantum_computing_project
```

Move into the cloned repository:
```console
$ cd quantum_computing_project
```

Setup a python virtual environment:
```console
$ python -m virtualenv venv
```

Activate the new virtualenvironment
```console
$ source venv/bin/activate
```

Download the PyPi program requirements:
```console
$ pip install -r requirements.txt
```

---
#### Optional - Run Tests:
Verify that all the tests are working, by running:
```console
$ pip install -r test-requirements.txt
```
```console
$ tox
```
There are three test actions configured for the repository, `tests`/`pep8`/
`mypy`.
The individual actions can be run using
```console
$ tox -e [action]
```
where `[action]` is one of `tests`/`pep8`/`mypy`

---
Once you have the repository set up on your system, you can run the code using
one of the following:

* [CLI Usage](#cli-usage)
* [GUI](#gui)
## CLI Usage:

The Help message for the CLI gives an overview of the program usage

```console
$ ./qcp/main.py -h
USAGE:
./qcp/main.py [FLAGS] nqbits
FLAGS:
    -a/--algorithm  The quantum algorithm to simulate, can be one of:
                        g   = Grover's Algorithm
                        pe  = Phase Estimation
                        s   = Toy Sudoku solver
                    Defaults to 'g' if unset
    -h/--help       Display this prompt
    -g/--gui      Display the GUI.

The CLI options vary by choice of algorithm:

GROVERS:
    USAGE:
    ./qcp/main.py --algorithm g [FLAGS] nqbits
    ARGS:
        nqbits          The number of qbit states to simulate, must be >= 2.
    FLAGS:
        -t/--target     The target state, defaults to 0

PHASE ESTIMATION:
    USAGE:
    ./qcp/main.py --algorithm pe [FLAGS] nqbits
    ARGS:
        nqbits          The number of qbit states to simulate, must be >= 2.
    FLAGS:
        -p/--phase      The phase to use for the Phase Shift Gate (if using).
                        defaults to 0.25.
        -u/--unitary    The choice of unitary gate to simulate with, can be
                        one of the following:
                            * H = Hadamard Gate
                            * P = Phase Shift Gate (requires the -p flag)
                        Defaults to 'H' if unset
SUDOKU:
    USAGE:
    ./qcp/main.py --algorithm s
    ARGS:
        None
    FLAGS:
        None
```

As you can see, the program is capable of simulating three different quantum algorithms and use cases.

* [Grover's Algorithm](#grovers-algorithm)
* [Phase Estimation Algorithm](#phase-estimation-algorithm)
* [Sample Sudoku Application](#sudoku-application)

## Grover's Algorithm

`nqbits`: is a required parameter, and controls the number of qbibts to simulate in the simulator
> **Note:**
> The quantum simulator simulates matrices of size `2^nqbits`, so be aware that
> The simulation takes exponentially longer for each extra qbit simulated.

`-t`/`--target`: is the target state to search for, must be bounded within `1 < t < 2^nqbits`

## Phase Estimation Algorithm:

`nqbits`: is a required parameter, and controls the number of qbibts to simulate in the simulator
> **Note:**
> The quantum simulator simulates matrices of size `2^nqbits`, so be aware that
> The simulation takes exponentially longer for each extra qbit simulated.

`-u`/`--unitary` is the unitary matrix to use in the phase estimation algorithm, currently there are two choices:
    * H = Hadamard Gate
    * P = Phase Shift Gate
> **Note:**
> When the Phase Shift Gate is chosen, the phase to shift by can be
> overwritten using the `-p`/`--phase` flag.

## Sudoku Application

A sample application of Grover's Algorithm, where we solve the toy problem of a 2x2 sudoku. Takes no input

## GUI:

A Graphical User Interface (GUI) is provided with the program to make interaction with it
easier.

The GUI can be initialised with the following command:
```console
$ ./qcp/main.py -g
```

This will bring up the GUI, defaulting to Grover's Algorithm.

At the top of the GUI is a drop down list, with the options for the algorithms to simulate, choosing each algorithm in sequence will update the GUI to reflect the input parameters of that algorithm

### Grover's Algorithm

![Initial UI](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_overview_grovers.png)

Grover's Algorithm has two input fields.

The first field sets the number of qbits to simulate.

The second is the target state, and is bounded within `0 < t < 2**nqbits`

### Phase Estimation

![Phase Estimation Overview](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_overview_phase_estimation.png)

The phase estimation is the most complicated GUI element.

As with Grover's Algorithm, the first input is the number of qbits to simulate.

The next two input elements allow the user to draw in matrices to use for the unitary matrix and the eigenvector. These matrix sizes are determined by the number of qbits.

The unitary matrix gets automatically populated as an identity matrix, but this can be manually changed by the user, where any `integer`/`float`/`complex` is an acceptable parameter.

The eigenvector input operates the same way, except that is is automaticaly populated as a column vector with the first entry `= 1`.

If there are any issues with the inputs of the two matrices once the simulation is set to start, the simulation will quit and a useful error message will appear beside the matrix at fault with a message pin-pointing the entry at fault.

### Sudoku

![Sudoku Overview](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_overview_sudoku.png)

The sudoku has no explicit input, which segues nicely to:

### Search Button:

Once ready to begin running the quantum algorithm simulation, click the button at the bottom of the GUI labeled "search" or "start".

This will begin the simulation of the chosen algorithm in the background.

While the simulation is running, a visual indicator will appear to show that the simulation is still in progress

![Simulation in Progress](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_calculation_inprogress_sudoku.png)

Once the search is completed, a plot of the probability of the quantum state 
being in the target state will be shown on the right.

![Sample Calculated Result](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_calculation_grovers.png)

**Grover's Algorithm**

As shown in the figure above, the simulation results for Grover's Algorithm also outputs the number of iterations that the quantum simulator took to find the result, and compares it to the equivalent for a classical algorithm.

**Phase Estimation**

![Phase Estimation Result](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_calculation_phase_estimation.png)

When the phase estimation result is computed, the probabilities are shown in the graph on the right for each state.

**Sudoku**

![Sudoku Result](https://github.com/Tiernan8r/quantum_computing_project/blob/master/docs/images/gui_calculation_phase_estimation.png)

Sudoku also outputs a probability distribution in the graph on the right.

For the simple 2x2 sudoku problem, a sample layout is also shown in a table, with the probability calculated by the algorithm for that state to be the accepted result.