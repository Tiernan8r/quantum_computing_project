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

import qcp.algorithms.phase_estimation_unitary_matrices as um_opt
from PySide6 import QtCore, QtWidgets
from qcp.gui.components.phase_estimation.combo_box_component import \
    PhaseComboBoxComponent
from qcp.gui.components.phase_estimation.constants import (
    INPUT_NQBITS_NAME, PHI_ONE_LABEL, PHI_ONE_SPIN_BOX, PHI_TWO_LABEL,
    PHI_TWO_SPIN_BOX, PRECISION_SPIN_BOX, SUCCESS_RATE_SPIN_BOX)
from qcp.matrices import DefaultMatrix, Matrix
from qcp.matrices.types import SPARSE


class PhaseInputComponent(PhaseComboBoxComponent):
    """
    UI component that handles the reading of input from the search and target
    text boxes
    """

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        """
        Initialise the InputComponent object

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

        # Update the unitary matrix displayed when the combo box changes.
        self.unitary_matrix_combo_box.currentTextChanged.connect(
            self.display_unitary)
        self.unitary_matrix_combo_box.currentTextChanged.connect(
            self.redisplay_eigenvector
        )
        self.unitary_matrix_combo_box.currentTextChanged.connect(
            self.toggle_phi)

        # Update the eigenvector matrix when the combo box changes
        self.eigenvector_combo_box.currentTextChanged.connect(
            self.display_eigenvector
        )

        # Hide the phi inputs initially
        self.phi1_spin_box.hide()
        self.phi2_spin_box.hide()
        self.phi1_label.hide()
        self.phi2_label.hide()

        self.phi1_spin_box.valueChanged.connect(self.update_phi)
        self.phi2_spin_box.valueChanged.connect(self.update_phi)

        # Force initial population of UI elements:
        self.force_refresh()

    def _find_widgets(self):
        super()._find_widgets()

        spin_boxes = self.main_window.ui_component.findChildren(
            QtWidgets.QSpinBox
        )
        for spin_box in spin_boxes:
            if spin_box.objectName() == INPUT_NQBITS_NAME:
                self.nqbit_input: QtWidgets.QSpinBox = spin_box
            if spin_box.objectName() == PRECISION_SPIN_BOX:
                self.precision_spinbox: QtWidgets.QSpinBox = spin_box

        double_spin_boxes: List[QtWidgets.QDoubleSpinBox] = \
            self.main_window.ui_component.findChildren(
            QtWidgets.QDoubleSpinBox
        )
        for double_spin in double_spin_boxes:
            if double_spin.objectName() == PHI_ONE_SPIN_BOX:
                self.phi1_spin_box = double_spin
            elif double_spin.objectName() == PHI_TWO_SPIN_BOX:
                self.phi2_spin_box = double_spin
            elif double_spin.objectName() == SUCCESS_RATE_SPIN_BOX:
                self.success_rate_spin_box = double_spin

        labels = self.main_window.ui_component.findChildren(QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == PHI_ONE_LABEL:
                self.phi1_label = lab
            elif lab.objectName() == PHI_TWO_LABEL:
                self.phi2_label = lab

    def force_refresh(self):
        current_unitary_str = self.unitary_matrix_combo_box.currentText()
        self.display_unitary(current_unitary_str)

        current_eigenvector_str = self.eigenvector_combo_box.currentText()
        self.display_eigenvector(current_eigenvector_str)

    @QtCore.Slot(str)
    def display_unitary(self, choice: str):
        unitary_choice = um_opt.UnitaryMatrices(choice)

        phi1, phi2 = 0.0, 0.0
        if unitary_choice is um_opt.UnitaryMatrices.PHASE_SHIFT:
            phi1 = self.parse_phi_one()
            phi2 = self.parse_phi_two()

        unitary_matrix = unitary_choice.get(phi1, phi2)

        self._display_table(self.unitary_table, unitary_matrix)

    @QtCore.Slot(str)
    def redisplay_eigenvector(self, choice: str):
        unitary_choice = um_opt.UnitaryMatrices(choice)
        default_basis = unitary_choice.basis_names()[0]
        self.display_eigenvector(default_basis)

    @QtCore.Slot(str)
    def display_eigenvector(self, choice: str):
        # When the combo box gets repopulated, this event can
        # be trigerred with an empty string...
        if choice == "":
            return

        unitary_choice_str = self.unitary_matrix_combo_box.currentText()
        unitary_choice = um_opt.UnitaryMatrices(unitary_choice_str)

        basis_names = unitary_choice.basis_names()
        if choice not in basis_names:
            print(f"'{choice}' is not a valid eigenvector!")
            return

        choice_idx = basis_names.index(choice)
        eigenvector = unitary_choice.basis()[choice_idx]

        self._display_table(self.eigenvector_table, eigenvector)

    def _display_table(self, table: QtWidgets.QTableWidget, mat: Matrix):
        n, m = mat.num_rows, mat.num_columns
        table.setRowCount(n)
        table.setColumnCount(m)

        for i in range(n):
            for j in range(m):
                val = mat[i][j]
                table_item = QtWidgets.QTableWidgetItem(str(val))

                table.setItem(i, j, table_item)

        table.show()

    @QtCore.Slot(str)
    def toggle_phi(self, choice: str):
        unitary_matrix = um_opt.UnitaryMatrices(choice)
        if unitary_matrix is um_opt.UnitaryMatrices.PHASE_SHIFT:
            self.phi1_label.show()
            self.phi1_spin_box.show()
            self.phi2_label.show()
            self.phi2_spin_box.show()
        else:
            self.phi1_spin_box.hide()
            self.phi2_spin_box.hide()
            self.phi1_label.hide()
            self.phi2_label.hide()

    @QtCore.Slot(float)
    def update_phi(self, val: float):
        self.display_unitary(self.unitary_matrix_combo_box.currentText())

    def parse_nqbit_input(self) -> int:
        return self.nqbit_input.value()

    def _parse_table_input(self, table: QtWidgets.QTableWidget) -> Matrix:
        n, m = table.rowCount(), table.columnCount()
        entries: SPARSE = {i: {} for i in range(n)}

        for i in range(n):
            for j in range(m):
                itm = table.item(i, j)
                if itm is None:
                    raise ValueError(f"Item at ({i + 1}, {j + 1}) unset!")

                str_val = itm.text()
                val = 0+0j
                try:
                    val = complex(str_val)
                except ValueError as ve:
                    raise ValueError(
                        f"Issue with entry ({i + 1}, {j + 1}): " + str(ve))

                if cmath.isclose(val, 0):
                    continue

                entries[i][j] = val

        return DefaultMatrix(entries)

    def parse_unitary_table_input(self) -> Matrix:
        unitary_matrix = self._parse_table_input(self.unitary_table)

        if not unitary_matrix.unitary:
            raise ValueError("input matrix is not unitary!")

        return unitary_matrix

    def parse_eigenvector_table_input(self) -> Matrix:
        return self._parse_table_input(self.eigenvector_table)

    def parse_phi_one(self) -> float:
        return self.phi1_spin_box.value()

    def parse_phi_two(self) -> float:
        return self.phi2_spin_box.value()

    def parse_nqbits_precision(self) -> int:
        return self.precision_spinbox.value()

    def parse_nqbits_success_rate(self) -> float:
        return self.success_rate_spin_box.value()
