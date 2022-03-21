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
File where all constants related to UI functionality are defined.
"""

#: The widget name for the input search text box
INPUT_SEARCH_NAME = "input_search"
#: The widget name for the input target text box
INPUT_TARGET_NAME = "input_target"

#: The widget name for the button to initialise the search
SEARCH_BUTTON = "search_button"
#: The widget name for the button to cancel a search simulation once
#: it is initialised
CANCEL_BUTTON = "cancel_button"

#: The widget name for the LCD ticker to display the number of iterations
#: a classical computer would have taken to find the result on average.
LCD_CLASSICAL = "lcd_number_classic"
#: The widget name for the LCD ticker to display the number of iterations
#: our simulation of Grover's Algorithm would take on average to find the
#: result
LCD_GROVER = "lcd_number_grover"
