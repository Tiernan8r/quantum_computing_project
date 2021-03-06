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
from typing import List

import qcp.algorithms as alg
from PySide6 import QtCore, QtWidgets
from qcp.gui.components import GraphComponent, SimulatorComponent
from qcp.gui.components.phase_estimation import PhaseButtonComponent
from qcp.gui.components.constants import (
    MEASURED_PHASE_LABEL, MEASURED_PHASE_LABEL_VALUE)


class PhaseSimulatorComponent(SimulatorComponent):
    """
    UI Component that handles the background task of running the Quantum
    Computer Simulator code on a separate QThread.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 button_component: PhaseButtonComponent,
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

        labels: List[QtWidgets.QLabel] = \
            self.main_window.ui_component.findChildren(QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == MEASURED_PHASE_LABEL:
                self.measured_phase_label = lab
            elif lab.objectName() == MEASURED_PHASE_LABEL_VALUE:
                self.measured_phase_label_value = lab

    @QtCore.Slot(tuple)
    def _simulation_results(self, results_tuple):
        """
        Signal catcher to read in the simulation results from the
        QThread that it is calculated in.
        """
        super()._simulation_results(results_tuple)

        self.algorithm: alg.PhaseEstimation = results_tuple[0]

        phase = self.algorithm.measure_phase()
        self.measured_phase_label.show()
        self.measured_phase_label_value.show()
        self.measured_phase_label_value.setText(str(phase))

        self.button_component.pb_thread.exiting = True

    def simulation_finished(self):
        """
        Function to handle behaviour when the QThread completes successfully

        Shows the quantum state on the matplotlib graph
        """
        self.graph_component.show()
