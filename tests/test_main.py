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
from qcp import main
import pytest
import sys


def test_usage(capsys):
    default_target = 5
    expected_str = f"""USAGE:
{sys.argv[0]} [FLAGS] nqbits

ARGS:
    nqbits          The number of qbit states to simulate
FLAGS:
    -t/--target     The target state, defaults to {default_target}
    -h/--help       Display this prompt
"""

    with pytest.raises(SystemExit) as se:
        main.usage()

    assert se.match("0")
    captured = capsys.readouterr()
    assert captured.out == expected_str


def test_main():
    with pytest.raises(SystemExit) as se:
        main.main()
    assert se.match("1")
