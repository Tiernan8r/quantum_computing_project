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
from multiprocessing.sharedctypes import Value
from PySide6 import QtWidgets
from qcp.ui.components import AbstractComponent
from qcp.ui.constants import INPUT_SEARCH_WIDGET_NAME, \
    INPUT_TARGET_WIDGET_NAME, INPUT_SEARCH_ERROR_WIDGET_NAME, \
    INPUT_TARGET_ERROR_WIDGET_NAME
from typing import List


class InputComponent(AbstractComponent):
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

        self.input_search_error.hide()
        self.input_target_error.hide()

    def setup_signals(self):
        """
        Setup the "browse" button to open the file dialog window when clicked.
        """
        super().setup_signals()

    def _find_widgets(self):
        line_edits: List[QtWidgets.QLineEdit] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QLineEdit
        )
        for line_edit in line_edits:
            if line_edit.objectName() == INPUT_TARGET_WIDGET_NAME:
                self.input_target = line_edit
            elif line_edit.objectName() == INPUT_SEARCH_WIDGET_NAME:
                self.input_search = line_edit

        error_labels: List[QtWidgets.QLabel] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QLabel
        )
        for error_label in error_labels:
            if error_label.objectName() == INPUT_SEARCH_ERROR_WIDGET_NAME:
                self.input_search_error = error_label
            elif error_label.objectName() == INPUT_TARGET_ERROR_WIDGET_NAME:
                self.input_target_error = error_label

    def _search_input_error(self, error: ValueError):
        self.input_search_error.show()

        self.input_search_error.setText(str(error))


    def _target_input_error(self, error: ValueError):
        self.input_target_error.show()

        self.input_target_error.setText(str(error))

    def parse_input(self) -> int:
        self.input_search_error.hide()

        input_str = self.input_search.text()
        input = 0
        try:
            input = int(input_str)
        except ValueError as ve:
            self._search_input_error(str(ve))
            raise ve

        if input < 2:
            ve = ValueError("need a minimum of two qbits")
            self._search_input_error(str(ve))
            raise ve

        return input

    def parse_target(self, nqbits) -> int:
        self.input_target_error.hide()

        target_str = self.input_target.text()
        target = 0
        try:
            target = int(target_str)
        except ValueError as ve:
            self._target_input_error(str(ve))
            raise ve

        if target < 0 or target > 2**nqbits:
            ve = ValueError("target must be within qbit state size range")
            self._target_input_error(str(ve))
            raise ve

        return target
