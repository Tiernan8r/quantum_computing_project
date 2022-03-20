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
DEFAULT_ALGORITHM = "g"
DEFAULT_PHASE = 0.25
DEFAULT_UNITARY = "H"

#: CLI flag values:
HELP_SHORT = "-h"
HELP_LONG = "--help"
ALGORITHM_SHORT = "-a"
ALGORITHM_LONG = "--algorithm"
TARGET_SHORT = "-t"
TARGET_LONG = "--target"
UNITARY_SHORT = "-u"
UNITARY_LONG = "--unitary"
PHASE_SHORT = "-p"
PHASE_LONG = "--phase"

#: All the flags accepted by the CLI, mapping their short name to
#: the more verbose one
FLAG_MAPPING = {
    HELP_SHORT: HELP_LONG,
    ALGORITHM_SHORT: ALGORITHM_LONG,
    TARGET_SHORT: TARGET_LONG,
    UNITARY_SHORT: UNITARY_LONG,
    PHASE_SHORT: PHASE_LONG
}
