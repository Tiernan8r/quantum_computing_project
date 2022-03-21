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
import qcp.algorithms as alg
from PySide6 import QtCore, QtWidgets
from qcp.gui.components import (AbstractComponent, GraphComponent,
                                SimulateAlgorithmThread)
from qcp.gui.components.sudoku import SudokuButtonComponent, SudokuResultsTable
from qcp.gui.components.sudoku.constants import (PROBABILITY_DISPLAY,
                                                 PROBABILITY_LABEL,
                                                 RESULT_TABLE)
from qcp.matrices import Matrix


class SudokuSimulatorComponent(AbstractComponent):
    """
    UI Component that handles the background task of running the Quantum
    Computer Simulator code on a separate QThread.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 button_component: SudokuButtonComponent,
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

        # Hide the widgets that show the results
        self.probability_display.hide()
        self.probability_label.hide()
        self.result_table.hide()

        self.qcp_thread = SimulateAlgorithmThread()
        self.qcp_thread.simulation_result_signal.connect(
            self._simulation_result)

        # Hide the cancel button if the calculation finishes
        self.qcp_thread.finished.connect(
            self.button_component.cancel_button.hide)

        self.qcp_thread.finished.connect(self.simulation_finished)

    def _find_widgets(self):
        tables = self.main_window.ui_component.findChildren(
            QtWidgets.QTableView)
        for t in tables:
            if t.objectName() == RESULT_TABLE:
                self.result_table: QtWidgets.QTableView = t

        labels = self.main_window.ui_component.findChildren(
            QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == PROBABILITY_LABEL:
                self.probability_label: QtWidgets.QLabel = lab

        progress_bars = self.main_window.ui_component.findChildren(
            QtWidgets.QProgressBar)
        for pb in progress_bars:
            if pb.objectName() == PROBABILITY_DISPLAY:
                self.probability_display: QtWidgets.QProgressBar = pb

    def run_simulation(self):
        """
        Pass the input parameters to the QThread, and start up the
        simulation
        """
        input_tuple = (
            alg.Sudoku,
        )
        self.qcp_thread.simulation_input_signal.emit(input_tuple)

    @QtCore.Slot(tuple)
    def _simulation_result(self, result_tuple):
        """
        Signal catcher to read in the simulation results from the
        QThread that it is calculated in.
        """
        algorithm: alg.Sudoku = result_tuple[0]
        qregister = result_tuple[1]

        # Update the graph
        self.graph_component.display(qregister)

        # update the table
        solutions = algorithm.measure_solution()
        self.table_model = SudokuResultsTable(solutions[0])
        self.result_table.setModel(self.table_model)
        self.result_table.show()

        solution_probability = solutions[1] * 100
        self.probability_label.show()

        self.probability_display.setValue(solution_probability)
        self.probability_display.show()

        # Stop the progress bar thread
        self.button_component.pb_thread.exiting = True

    def simulation_finished(self):
        """
        Function to handle behaviour when the QThread completes successfully

        Shows the quantum state on the matplotlib graph
        """
        self.graph_component.show()
