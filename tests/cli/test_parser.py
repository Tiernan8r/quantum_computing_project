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
import pytest
from qcp import cli
from tests.cli.test_usage import EXPECTED_USAGE


def test_read_cli(capsys):
    # No args provided just shows the help message
    dummy_args0 = []
    with pytest.raises(SystemExit) as se0:
        cli.read_cli(dummy_args0)
    assert se0.match("0")
    captured0 = capsys.readouterr()
    assert "USAGE" in captured0.out

    # Non-integer qbits number:
    dummy_args1 = ["ten"]
    with pytest.raises(SystemExit) as se1:
        cli.read_cli(dummy_args1)
    assert se1.match("1")
    captured1 = capsys.readouterr()
    assert "Provided number of qbits 'ten' is not an integer!" in captured1.err

    # "-h" or "--help" shows usage:
    dummy_args2_1 = ["-h"]
    with pytest.raises(SystemExit) as se2_1:
        cli.read_cli(dummy_args2_1)
    assert se2_1.match("0")
    captured2_1 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_1.out

    dummy_args2_2 = ["--help"]
    with pytest.raises(SystemExit) as se2_2:
        cli.read_cli(dummy_args2_2)
    assert se2_2.match("0")
    captured2_2 = capsys.readouterr()
    assert EXPECTED_USAGE in captured2_2.out

    # --target must be an integer:
    dummy_args3 = ["-t", "one", "2"]
    with pytest.raises(SystemExit) as se3:
        cli.read_cli(dummy_args3)
    assert se3.match("1")
    captured3 = capsys.readouterr()
    assert "Provided target 'one' is not an integer" in captured3.err

    # Values are read correctly:
    dummy_args4 = ["-t", "1", "2"]
    opt, (n4, t4) = cli.read_cli(dummy_args4)
    assert opt.value == "g"
    assert n4 == 2
    assert t4 == 1
