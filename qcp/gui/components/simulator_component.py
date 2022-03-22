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
from qcp.gui.components.abstract_component import AbstractComponent
from qcp.gui.components.constants import (OUTPUT_STATE_PROBABILITY,
                                          OUTPUT_STATE_PROBABILITY_TEXT_LABEL,
                                          OUTPUT_VALUE_FORMAT,
                                          OUTPUT_VALUE_LABEL,
                                          OUTPUT_VALUE_TEXT_LABEL)
from qcp.gui.components.graph_component import GraphComponent
from qcp.gui.components.threaded_compute import SimulateAlgorithmThread


class SimulatorComponent(AbstractComponent):
    """
    UI Component that handles the the task of setting up and handling the
    QThread that runs the simulation, and showing the measured
    states and probabilities on the UI.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 graph_component: GraphComponent, *args, **kwargs):
        """
        Initialise the SimulatorComponent object, referencing the main window
        element, and the the graph UI components required for it to function.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param GraphComponent graph_component: The target graph in the UI
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        self.graph_component = graph_component
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Initialise the QThread to run the simulation on and have it ready
        to run when the input parameters are provided.

        Setup signals to display the graph when the calculation completes,
        and to hide the cancel button and progress bar.
        """
        super().setup_signals()

        self.qcp_thread = SimulateAlgorithmThread()
        self.qcp_thread.simulation_result_signal.connect(
            self._simulation_results)

        self.qcp_thread.finished.connect(self.update_results_displays)
        self.qcp_thread.finished.connect(self.simulation_finished)

        # Hide the widgets that show the results
        self.output_value_label.hide()
        self.output_state_probability_label.hide()
        self.output_value_text_label.hide()
        self.output_state_probability.hide()

    def _find_widgets(self):
        labels = self.main_window.ui_component.findChildren(QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == OUTPUT_VALUE_LABEL:
                self.output_value_label: QtWidgets.QLabel = lab
            elif lab.objectName() == OUTPUT_STATE_PROBABILITY_TEXT_LABEL:
                self.output_state_probability_label: QtWidgets.QLabel = lab
            elif lab.objectName() == OUTPUT_VALUE_TEXT_LABEL:
                self.output_value_text_label: QtWidgets.QLabel = lab

        progress_bars = self.main_window.ui_component.findChildren(
            QtWidgets.QProgressBar)
        for pb in progress_bars:
            if pb.objectName() == OUTPUT_STATE_PROBABILITY:
                self.output_state_probability: QtWidgets.QProgressBar = pb

    def run_simulation(self, tuple_input):
        """
        Pass the input parameters to the QThread, and start up the
        simulation
        """
        self.tuple_input = tuple_input
        self.qcp_thread.simulation_input_signal.emit(tuple_input)

    @QtCore.Slot(tuple)
    def _simulation_results(self, result_tuple):
        """
        Signal catcher to read in the simulation results from the
        QThread that it is calculated in.
        """
        self.algorithm: alg.Sudoku = result_tuple[0]
        self.results = result_tuple[1:]

        # Update the graph
        self.probabilities = self.results[0]
        self.qregister = self.results[1]
        self.graph_component.display(self.probabilities)

    def simulation_finished(self):
        """
        Function to handle behaviour when the QThread completes successfully

        Shows the quantum state on the matplotlib graph
        """
        self.graph_component.show()

    def update_results_displays(self):
        """
        Show the measured state from the calculation, and the probability
        of measuring that state.
        """
        if not self.algorithm:
            return

        # Show the widgets that show the results
        self.output_value_label.show()
        self.output_state_probability_label.show()
        self.output_value_text_label.show()
        self.output_state_probability.show()

        state, probability = self.algorithm.measure()

        self.output_value_label.setText(OUTPUT_VALUE_FORMAT.format(state))

        prob = math.floor(probability * 100)
        self.output_state_probability.setValue(prob)
