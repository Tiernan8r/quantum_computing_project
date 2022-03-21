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
import time
from typing import List

from PySide6 import QtCore, QtWidgets
from qcp.gui.components import ProgressBarComponent
from qcp.gui.components.constants import (PROGRESS_BAR,
                                          PROGRESS_BAR_TICK_RATE)
from qcp.gui.components.sudoku.constants import (CANCEL_BUTTON,
                                                 SEARCH_BUTTON)
from qcp.gui.constants import THREAD_PAUSE


class SudokuButtonComponent(ProgressBarComponent):
    """
    Component of the UI that handles button click behaviour.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 *args, **kwargs):
        """
        Initialise the ButtonComponent object, referencing the main window
        element, and the two text boxes used in the UI.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Setup what happens when the buttons in the UI are clicked.
        """
        super().setup_signals()

        self.cancel_button.hide()

        self.start_button.clicked.connect(self.initiate_simulation)
        self.cancel_button.clicked.connect(self.cancel_simulation)

    def _find_widgets(self):
        super()._find_widgets()

        buttons: List[QtWidgets.QPushButton] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QPushButton)
        for b in buttons:
            if b.objectName() == SEARCH_BUTTON:
                self.start_button = b
            if b.objectName() == CANCEL_BUTTON:
                self.cancel_button = b

    def initiate_simulation(self):
        """
        Start the running of the Quantum Computer Simulator on a
        separate QThread.

        Show the cancel button, so that the QThread can be killed before the
        calculation completes.

        Startup the QThread that updates the progress bar so that it swirls
        overtime, to visualise that the computer is running a calculation in
        the background.
        """
        self.cancel_button.show()

        self.tick_progress_bar()

        self.main_window.sudoku_simulator.run_simulation()

    def cancel_simulation(self):
        """
        Kill the Simulation QThread when the button is clicked.

        Hide and reset the progress bar.

        Then hide the cancel button as a calculation is no longer running.
        """
        if self.pb_thread.isRunning():
            self.pb_thread.exiting = True
            while self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)
        if self.main_window.sudoku_simulator.qcp_thread.isRunning():
            self.main_window.sudoku_simulator.qcp_thread.quit()
            time.sleep(THREAD_PAUSE)

        self.cancel_button.hide()
