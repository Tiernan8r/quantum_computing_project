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
import cmath
from typing import List

from PySide6 import QtCore, QtWidgets
from qcp.gui.components import AbstractComponent
from qcp.gui.components.phase_estimation.constants import (
    EIGENVECTOR_COMBO_BOX, INPUT_EIGENVECTOR_NAME, INPUT_UNITARY_NAME,
    UNITARY_MATRIX_COMBO_BOX)
from qcp.matrices import DefaultMatrix, Matrix
from qcp.matrices.types import SPARSE
import qcp.algorithms.phase_estimation_unitary_matrices as um_ops


class PhaseComboBoxComponent(AbstractComponent):
    """
    UI component that handles the reading of input from the search and target
    text boxes
    """

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        """
        Initialise the ComboBoxComponent object

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Setup the "browse" button to open the file dialog window when clicked.
        """
        super().setup_signals()

        self.setup_unitary_options()
        self.unitary_matrix_combo_box.currentTextChanged.connect(
            self.populate_eigenvector_options)

    def _find_widgets(self):
        combo_boxes: List[QtWidgets.QComboBox] = \
            self.main_window.ui_component.findChildren(
            QtWidgets.QComboBox
        )
        for cb in combo_boxes:
            if cb.objectName() == UNITARY_MATRIX_COMBO_BOX:
                self.unitary_matrix_combo_box = cb
            elif cb.objectName() == EIGENVECTOR_COMBO_BOX:
                self.eigenvector_combo_box = cb

        tables = self.main_window.ui_component.findChildren(
            QtWidgets.QTableWidget
        )
        for tab in tables:
            if tab.objectName() == INPUT_UNITARY_NAME:
                self.unitary_table: QtWidgets.QTableWidget = tab
            elif tab.objectName() == INPUT_EIGENVECTOR_NAME:
                self.eigenvector_table: QtWidgets.QTableWidget = tab

    def setup_unitary_options(self):
        predefined_unitaries = um_ops.UnitaryMatrices.list()

        self.unitary_matrix_combo_box.clear()
        for un in predefined_unitaries:
            self.unitary_matrix_combo_box.addItem(un)

        # Force the initial refresh of the eigenvector options
        self.populate_eigenvector_options(predefined_unitaries[0])

    @QtCore.Slot(str)
    def populate_eigenvector_options(self, new_unitary: str):

        if new_unitary not in um_ops.UnitaryMatrices.list():
            print(f"'{new_unitary}' not a valid unitary matrix choice!")

        unitary_choice = um_ops.UnitaryMatrices(new_unitary)

        eigenvectors = unitary_choice.basis_names()

        self.eigenvector_combo_box.clear()
        for eig in eigenvectors:
            self.eigenvector_combo_box.addItem(eig)
