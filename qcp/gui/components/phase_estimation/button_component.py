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

from PySide6 import QtWidgets
from qcp.gui.components import ProgressBarComponent
from qcp.gui.components.phase_estimation.constants import (
    BUTTON_CANCEL, BUTTON_START, EIGENVECTOR_ERROR_LABEL, UNITARY_ERROR_LABEL)
from qcp.gui.components.phase_estimation.input_component import \
    PhaseInputComponent
from qcp.gui.constants import THREAD_PAUSE


class PhaseButtonComponent(ProgressBarComponent):
    """
    Component of the UI that handles button click behaviour.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 input_component: PhaseInputComponent,
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

        self.progress_bar.hide()
        self.progress_bar.reset()

        self.cancel_button.hide()

        self.unitary_error_label.hide()
        self.eigenvector_error_label.hide()

        self.start_button.clicked.connect(self.initiate_simulation)
        self.cancel_button.clicked.connect(self.cancel_simulation)

    def _find_widgets(self):
        super()._find_widgets()

        buttons: List[QtWidgets.QPushButton] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QPushButton)
        for b in buttons:
            if b.objectName() == BUTTON_START:
                self.start_button = b
            if b.objectName() == BUTTON_CANCEL:
                self.cancel_button = b

        labels = self.main_window.ui_component.findChildren(
            QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == UNITARY_ERROR_LABEL:
                self.unitary_error_label: QtWidgets.QLabel = lab
            elif lab.objectName() == EIGENVECTOR_ERROR_LABEL:
                self.eigenvector_error_label: QtWidgets.QLabel = lab

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
        self.unitary_error_label.hide()
        self.eigenvector_error_label.hide()

        nqbits = self.input_component.parse_nqbit_input()
        try:
            unitary_matrix = self.input_component.parse_unitary_table_input()
        except ValueError as ve1:
            self._unitary_input_error(ve1)
            return

        try:
            eigenvector = self.input_component.parse_eigenvector_table_input()
        except ValueError as ve2:
            self._eigenvector_input_error(ve2)
            return

        self.cancel_button.show()

        self.tick_progress_bar()

        self.main_window.pe_simulator.run_simulation(
            nqbits, unitary_matrix, eigenvector)

    def _generic_input_error(self, label: QtWidgets.QLabel, ve: ValueError):
        label.show()
        label.setText(str(ve))

    def _unitary_input_error(self, ve: ValueError):
        self._generic_input_error(self.unitary_error_label, ve)

    def _eigenvector_input_error(self, ve: ValueError):
        self._generic_input_error(self.eigenvector_error_label, ve)

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
        if self.main_window.pe_simulator.qcp_thread.isRunning():
            self.main_window.pe_simulator.qcp_thread.quit()
            time.sleep(THREAD_PAUSE)

        self.cancel_button.hide()
