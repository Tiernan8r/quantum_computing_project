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
import math

import qcp.algorithms as alg
from PySide6 import QtCore, QtWidgets
from qcp.gui.components import (GraphComponent, SimulateAlgorithmThread,
                                SimulatorComponent)
from qcp.gui.components.grovers import GroverButtonComponent
from qcp.gui.components.grovers.constants import LCD_CLASSICAL, LCD_GROVER


class GroverSimulatorComponent(SimulatorComponent):
    """
    UI Component that handles the background task of running the Quantum
    Computer Simulator code on a separate QThread.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 button_component: GroverButtonComponent,
                 graph_component: GraphComponent, *args, **kwargs):
        """
        Initialise the SimulatorComponent object, referencing the main window
        element, and the two UI components required for it to function.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param ButtonComponent button_component: The search input box of the
            UI
        :param GraphComponent graph_component: The target input box of the UI
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        self.button_component = button_component
        super().__init__(main_window, graph_component, *args, **kwargs)

    def setup_signals(self):
        """
        Initialise the QThread to run the simulation on and have it ready
        to run when the input parameters are provided.

        Setup signals to display the graph when the calculation completes,
        and to hide the cancel button and progress bar.
        """
        super().setup_signals()

        # Hide the cancel button if the calculation finishes
        self.qcp_thread.finished.connect(
            self.button_component.cancel_button.hide)

    def _find_widgets(self):
        super()._find_widgets()

        lcds = self.main_window.ui_component.findChildren(QtWidgets.QLCDNumber)
        for lcd in lcds:
            if lcd.objectName() == LCD_CLASSICAL:
                self.lcd_classical = lcd
            elif lcd.objectName() == LCD_GROVER:
                self.lcd_grover = lcd

    @QtCore.Slot(tuple)
    def _simulation_results(self, tuple_results):
        """
        Signal catcher to read in the simulation results from the
        QThread that it is calculated in.
        """
        super()._simulation_results(tuple_results)

        self.button_component.pb_thread.exiting = True

    def update_results_displays(self):
        """
        Show the comparison between the number of iterations a classical
        computer would have needed to run the search, versus the number
        of iterations our quantum simulation took.
        """
        super().update_results_displays()

        if not self.tuple_input:
            return

        self.nqbits = self.tuple_input[1]

        # TODO: Don't know if this reasoning makes sense...
        number_entries = math.log2(self.nqbits)
        classical_average = math.ceil(number_entries / 2)
        quantum_average = math.ceil(math.sqrt(number_entries))

        self.lcd_classical.display(classical_average)
        self.lcd_grover.display(quantum_average)
