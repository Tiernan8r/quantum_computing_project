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

#: The default target state the Oracle will search for
DEFAULT_TARGET = 0
#: The default algorithm type to simulate
DEFAULT_ALGORITHM = "g"
#: The default phase to use in the unitary matrix, if required
DEFAULT_PHASE = 0.25
#: The default unitary matrix type to use.
DEFAULT_UNITARY = "hadamard"
#: The index of the default eigenvector to use:
DEFAULT_EIGENVECTOR_IDX = 0

# CLI flag values:

#: The short flag for the help message
HELP_SHORT = "-h"
#: The long flag for the help message
HELP_LONG = "--help"
#: The short flag the GUI initialiser
GUI_SHORT = "-g"
#: The long flag for the GUI initialiser
GUI_LONG = "--gui"
#: The short flag for the algorithm choice
ALGORITHM_SHORT = "-a"
#: The long flag for the algorithm choice
ALGORITHM_LONG = "--algorithm"
#: The short flag for the target
TARGET_SHORT = "-t"
#: The long flag for the target
TARGET_LONG = "--target"
#: The short flag for the unitary matrix choice
UNITARY_SHORT = "-u"
#: The long flag for the unitary matrix choice
UNITARY_LONG = "--unitary"
#: The short flag for the phase value
PHASE_SHORT = "-p"
#: The long flag for the phase value
PHASE_LONG = "--phase"
#: The short flag for the eigenvector choice
EIGENVECTOR_SHORT = "-e"
#: The long flag for the eigenvector choice
EIGENVECTOR_LONG = "--eigen"

#: All the flags accepted by the CLI, mapping their short name to
#: the more verbose one
FLAG_MAPPING = {
    HELP_SHORT: HELP_LONG,
    GUI_SHORT: GUI_LONG,
    ALGORITHM_SHORT: ALGORITHM_LONG,
    TARGET_SHORT: TARGET_LONG,
    UNITARY_SHORT: UNITARY_LONG,
    PHASE_SHORT: PHASE_LONG,
    EIGENVECTOR_SHORT: EIGENVECTOR_LONG
}
