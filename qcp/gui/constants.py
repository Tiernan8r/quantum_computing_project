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

#: The filename where the ui layout is defined in XML.
UI_FILENAME = "form.ui"
#: The widget name in the UI for the widget which the
#: graph will appear in
GRAPH_WIDGET_NAME = "graph"

#: Name of the combo box for the algorithm choices
COMBO_BOX_NAME = "algorithm_options"

#: Label to show the current algorithm choice
LABEL_TITLE = "title"
LABEL_TEXT_FORMAT = "<html><head/><body><p><span style=\" font-weight:700;\">{}:</span></p></body></html>"

COMBO_BOX_OPTION_GROVER = "Grover's Algorithm"
COMBO_BOX_OPTION_PHASE_ESTIMATION = "Phase Estimation"
COMBO_BOX_OPTION_SUDOKU = "Sudoku"

COMBO_BOX_OPTIONS = [COMBO_BOX_OPTION_GROVER,
                     COMBO_BOX_OPTION_PHASE_ESTIMATION, COMBO_BOX_OPTION_SUDOKU]

#: The layout containing input for Grover's Algorithm
GROVER_LAYOUT = "grover_frame"
#: The layout containing input for Phase Estimation
PHASE_ESTIMATION_LAYOUT = "phase_estimation_frame"
#: The layout containing input for Sudoku
SUDOKU_LAYOUT = "sudoku_frame"

ALGORITHM_LAYOUTS = [GROVER_LAYOUT, PHASE_ESTIMATION_LAYOUT, SUDOKU_LAYOUT]

COMBO_BOX_LAYOUT_MAPPING = {
    COMBO_BOX_OPTION_GROVER: GROVER_LAYOUT,
    COMBO_BOX_OPTION_PHASE_ESTIMATION: PHASE_ESTIMATION_LAYOUT,
    COMBO_BOX_OPTION_SUDOKU: SUDOKU_LAYOUT
}

LAYOUT_COMBO_MAPPING = {v: k for k, v in COMBO_BOX_LAYOUT_MAPPING.items()}

#: The widget name for the input search text box
INPUT_SEARCH_WIDGET_NAME = "input_search"
#: The widget name for the label to display any error message about search
#: input
INPUT_SEARCH_ERROR_WIDGET_NAME = "input_search_error"
#: The widget name for the input target text box
INPUT_TARGET_WIDGET_NAME = "input_target"
#: The widget name for the label to display any error message about
#: target input
INPUT_TARGET_ERROR_WIDGET_NAME = "input_target_error"

#: The widget name for the button to initialise the search
BUTTON_SEARCH_BUTTON = "search_button"
#: The widget name for the button to cancel a search simulation once
#: it is initialised
BUTTON_CANCEL_SEARCH_BUTTON = "cancel_button"
#: The widget name for the progress bar widget
BUTTON_PROGRESS_BAR = "progress_bar"
#: The tick rate in ms of the progress bar
BUTTON_PROGRESS_BAR_TICK_RATE = 100  # in milliseconds

#: The widget name for the LCD ticker to display the number of iterations
#: a classical computer would have taken to find the result on average.
LCD_CLASSICAL = "lcd_number_classic"
#: The widget name for the LCD ticker to display the number of iterations
#: our simulation of Grover's Algorithm would take on average to find the
#: result
LCD_GROVER = "lcd_number_grover"

#: The duration in seconds to wait for a thread to initialise when started.
THREAD_PAUSE = 0.01
