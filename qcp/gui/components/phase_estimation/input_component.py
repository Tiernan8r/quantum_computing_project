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
    INPUT_EIGENVECTOR_WIDGET_NAME, INPUT_NQBITS_WIDGET_NAME,
    INPUT_UNITARY_WIDGET_NAME)
from qcp.matrices import DefaultMatrix, Matrix


class PhaseInputComponent(AbstractComponent):
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

        self.nqbit_input.valueChanged.connect(self.resize_tables)
        # Force sizing of tables
        self.resize_tables(2)

    def _find_widgets(self):
        spin_boxes: List[QtWidgets.QSpinBox] = self.main_window.ui_component.findChildren(
            QtWidgets.QSpinBox
        )
        for spin_box in spin_boxes:
            if spin_box.objectName() == INPUT_NQBITS_WIDGET_NAME:
                self.nqbit_input = spin_box

        tables: List[QtWidgets.QTableWidget] = self.main_window.ui_component.findChildren(
            QtWidgets.QTableWidget
        )
        for t in tables:
            if t.objectName() == INPUT_UNITARY_WIDGET_NAME:
                self.unitary_table = t
            elif t.objectName() == INPUT_EIGENVECTOR_WIDGET_NAME:
                self.eigenvector_table = t

    def parse_nqbit_input(self) -> int:
        return self.unitary_table.value()

    @QtCore.Slot(int)
    def resize_tables(self, size: int):
        # The unitary table is size x size

        self.unitary_table.setRowCount(size)
        self.unitary_table.setColumnCount(size)

        for i in range(size):
            for j in range(size):
                itm = self.unitary_table.item(i, j)
                if itm is None:
                    val = lambda i, j: "1" if i == j else "0"
                    table_entry = QtWidgets.QTableWidgetItem(val(i, j))
                    self.unitary_table.setItem(i, j, table_entry)

        # The eigenvector is a column vector of 2**size
        n = 2 ** size

        self.eigenvector_table.setColumnCount(1)
        self.eigenvector_table.setRowCount(n)

        for i in range(n):
            itm = self.eigenvector_table.item(i, 0)
            if itm is None:
                val = lambda i: "1" if i == 0 else "0"
                table_entry = QtWidgets.QTableWidgetItem(val(i))
                self.eigenvector_table.setItem(i, 0, table_entry)

    def parse_nqbit_input(self):
        return self.nqbit_input.value()

    def _parse_table_input(self, table: QtWidgets.QTableWidget) -> Matrix:
        n, m = table.rowCount(), table.columnCount()
        entries = {i: {} for i in range(n)}

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
        return self._parse_table_input(self.unitary_table)

    def parse_eigenvector_table_input(self) -> Matrix:
        return self._parse_table_input(self.eigenvector_table)
