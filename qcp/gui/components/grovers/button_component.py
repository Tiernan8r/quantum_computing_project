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

import qcp.algorithms as alg
from PySide6 import QtWidgets
from qcp.gui.components import ProgressBarComponent
from qcp.gui.components.grovers.constants import CANCEL_BUTTON, SEARCH_BUTTON
from qcp.gui.components.grovers.input_component import GroverInputComponent
from qcp.gui.constants import THREAD_PAUSE


class GroverButtonComponent(ProgressBarComponent):
    """
    Component of the UI that handles button click behaviour.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 input_component: GroverInputComponent,
                 *args, **kwargs):
        """
        Initialise the ButtonComponent object, referencing the main window
        element, and the two text boxes used in the UI.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param QtWidgets.QTextEdit search: The search input box of the UI
        :param QtWidgets.QLineEdit target: The target input box of the UI
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

        self.input_component = input_component

    def setup_signals(self):
        """
        Setup what happens when the buttons in the UI are clicked.
        """
        super().setup_signals()

        self.cancel_button.hide()

        self.search_button.clicked.connect(self.initiate_search)
        self.cancel_button.clicked.connect(self.cancel_search)

    def _find_widgets(self):
        super()._find_widgets()

        buttons: List[QtWidgets.QPushButton] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QPushButton)
        for b in buttons:
            if b.objectName() == SEARCH_BUTTON:
                self.search_button = b
            if b.objectName() == CANCEL_BUTTON:
                self.cancel_button = b

    def initiate_search(self):
        """
        Start the running of the Quantum Computer Simulator on a
        separate QThread.

        Show the cancel button, so that the QThread can be killed before the
        calculation completes.

        Startup the QThread that updates the progress bar so that it swirls
        overtime, to visualise that the computer is running a calculation in
        the background.
        """
        nqbits = self.input_component.parse_input()
        target = self.input_component.parse_target()

        self.cancel_button.show()

        self.tick_progress_bar()

        input_tuple = (
            alg.Grovers,
            nqbits,
            target
        )

        self.main_window.grov_simulator.run_simulation(input_tuple)

    def cancel_search(self):
        """
        Kill the Simulation QThread when the button is clicked.

        Hide and reset the progress bar.

        Then hide the cancel button as a calculation is no longer running.
        """
        if self.pb_thread.isRunning():
            self.pb_thread.exiting = True
            while self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)
        if self.main_window.grov_simulator.qcp_thread.isRunning():
            self.main_window.grov_simulator.qcp_thread.quit()
            time.sleep(THREAD_PAUSE)

        self.cancel_button.hide()
