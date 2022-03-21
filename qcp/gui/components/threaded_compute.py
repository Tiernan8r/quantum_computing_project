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
from PySide6 import QtCore
from qcp.matrices import Matrix


class SimulateAlgorithmThread(QtCore.QThread):
    """
    QThread object to handle the running of the Quantum Computer
    Simulation, input/output is passed back to the main thread by pipes.
    """
    simulation_result_signal = QtCore.Signal(tuple)
    simulation_input_signal = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        """
        Setup the SimulateQuantumComputerThread QThread.
        """
        super().__init__(parent)
        self.simulation_input_signal.connect(self.input)
        self.exiting = False

    @QtCore.Slot(tuple)
    def input(self, tuple_input):
        if not self.isRunning():
            self.constructor = tuple_input[0]
            self.tuple_input = tuple_input[1:]
            self.exiting = False
            self.start()
        else:
            print("simulation already running!")

    def run(self):
        """
        Run the simulation
        """
        algorithm: alg.GeneralAlgorithm = self.constructor(*self.tuple_input)
        qregister = None
        try:
            qregister = algorithm.run()
        except AssertionError as ae:
            print(ae)

        results = (algorithm, qregister)
        self.simulation_result_signal.emit(results)
        self.quit()
