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

from PySide6 import QtCore, QtWidgets
from qcp.gui.components import AbstractComponent
from qcp.gui.components.grovers.constants import (INPUT_SEARCH_WIDGET_NAME,
                                                  INPUT_TARGET_WIDGET_NAME)


class GroverInputComponent(AbstractComponent):
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

        self.input_search.valueChanged.connect(self.update_target_input_max)

    def _find_widgets(self):
        spin_boxes: List[QtWidgets.QSpinBox] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QSpinBox
        )
        for spin_box in spin_boxes:
            if spin_box.objectName() == INPUT_TARGET_WIDGET_NAME:
                self.input_target = spin_box
            elif spin_box.objectName() == INPUT_SEARCH_WIDGET_NAME:
                self.input_search = spin_box

    @QtCore.Slot(int)
    def update_target_input_max(self, val: int):
        self.input_target.setMaximum(2**val - 1)

    def parse_input(self) -> int:
        return self.input_search.value()

    def parse_target(self) -> int:
        return self.input_target.value()
