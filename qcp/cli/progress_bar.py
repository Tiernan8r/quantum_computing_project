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
File containing the code to add an animated progress bar
"""
import sys
import time

#: List of the ASCII art tickers
_ticks = ["-", "\\", "|", "/"]


def ticker(tick_rate=0.2, prefix="", file=sys.stdout):
    """
    Shows a swirling ticker on the terminal to indicate that an operation
    is in progress.

    :param float tick_rate: The interval to sleep between refreshes in seconds.
    :parma str prefix: An optional prefix to show before the ticker.
    :param TextIO file: Override for the default I/O printed to.
    """

    def show(j):
        i = j % len(_ticks)  # Loop through the ticks
        file.write(f"{prefix}{_ticks[i]}\r")  # write to the same line
        file.flush()

    i = 0
    while True:
        show(i)
        i += 1
        time.sleep(tick_rate)
