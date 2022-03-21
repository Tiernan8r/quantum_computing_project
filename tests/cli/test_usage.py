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
import qcp.cli.usage as u

EXPECTED_USAGE = u.USAGE_STR + "\n"


def test_usage(capsys):
    with pytest.raises(SystemExit) as se:
        u.usage()

    assert se.match("0")
    # Capture the output of stdout (the print() statements...)
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_USAGE
