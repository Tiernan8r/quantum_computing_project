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

DEFAULT_TARGET = 5
EXPECTED_USAGE = f"""USAGE:
{sys.argv[0]} [FLAGS] nqbits

ARGS:
    nqbits          The number of qbit states to simulate
FLAGS:
    -t/--target     The target state, defaults to {DEFAULT_TARGET}
    -h/--help       Display this prompt
"""


def test_usage(capsys):
    with pytest.raises(SystemExit) as se:
        main.usage()

    assert se.match("0")
    # Capture the output of stdout (the print() statements...)
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_USAGE


def test_parse_cli(capsys):
    # No args provided (except for 'program name') errors with missing number
    # of qbits:
    dummy_args0 = ["main.py"]
    with pytest.raises(SystemExit) as se0:
        main.parse_cli(dummy_args0)
    assert se0.match("1")
    captured0 = capsys.readouterr()
    assert "Must provide the number of qbits to simulate" in captured0.err

    # Non-integer qbits number:
    dummy_args1 = ["main.py", "ten"]
    with pytest.raises(SystemExit) as se1:
        main.parse_cli(dummy_args1)
    assert se1.match("1")
    captured1 = capsys.readouterr()
    assert "number of qbits must be an integer" in captured1.err

    # "-h" or "--help" shows usage:
    dummy_args2_1 = ["main.py", "-h"]
    with pytest.raises(SystemExit) as se2_1:
        main.parse_cli(dummy_args2_1)
    assert se2_1.match("0")
    captured2_1 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_1.out

    dummy_args2_2 = ["main.py", "--help"]
    with pytest.raises(SystemExit) as se2_2:
        main.parse_cli(dummy_args2_2)
    assert se2_2.match("0")
    captured2_2 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_2.out

    # --target must be an integer:
    dummy_args3 = ["main.py", "-t", "one", "2"]
    with pytest.raises(SystemExit) as se3:
        main.parse_cli(dummy_args3)
    assert se3.match("1")
    captured3 = capsys.readouterr()
    assert "target state must be an integer" in captured3.err

    # Values are read correctly:
    dummy_args4 = ["main.py", "-t", "1", "2"]
    n4, t4 = main.parse_cli(dummy_args4)
    assert n4 == 2
    assert t4 == 1


def test_main():
    with pytest.raises(SystemExit) as se:
        main.main()
    assert se.match("1")
