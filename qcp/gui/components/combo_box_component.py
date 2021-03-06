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
from qcp.gui.components.constants import (ALGORITHM_LAYOUTS,
                                          COMBO_BOX_LAYOUT_MAPPING,
                                          COMBO_BOX_NAME, LABEL_TEXT_FORMAT,
                                          LABEL_TITLE, MEASURED_PHASE_LABEL,
                                          MEASURED_PHASE_LABEL_VALUE)


class ComboBoxComponent(AbstractComponent):
    """
    Component of the UI that handles the choice of algorithm to simulate
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 *args, **kwargs):
        """
        Initialise the ButtonComponent object, referencing the main window
        element, and the two text boxes used in the UI.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Setup what happens when the buttons in the UI are clicked.
        """
        super().setup_signals()

        self.combo_box.currentTextChanged.connect(self.update_label)
        self.combo_box.currentTextChanged.connect(self.update_window_title)
        self.combo_box.currentTextChanged.connect(self.update_ui)

        self.measured_phase_label.hide()
        self.measured_phase_label_value.hide()

        # Initially trigger a UI redraw so that only one layout is shown
        self.update_ui(self.combo_box.currentText())

    def _find_widgets(self):
        combo_boxes: List[QtWidgets.QPushButton] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QComboBox)
        for cb in combo_boxes:
            if cb.objectName() == COMBO_BOX_NAME:
                self.combo_box = cb

        labels = self.main_window.ui_component.findChildren(
            QtWidgets.QLabel)
        for lab in labels:
            if lab.objectName() == LABEL_TITLE:
                self.label_title: QtWidgets.QLabel = lab
            elif lab.objectName() == MEASURED_PHASE_LABEL:
                self.measured_phase_label = lab
            elif lab.objectName() == MEASURED_PHASE_LABEL_VALUE:
                self.measured_phase_label_value = lab

        # Dict mapping the containers for each algorithm to it's
        # name
        self.layouts = {}
        all_layouts = self.main_window.ui_component.findChildren(
            QtWidgets.QWidget)
        for layout in all_layouts:
            if layout.objectName() in ALGORITHM_LAYOUTS:
                self.layouts[layout.objectName()] = layout

    @QtCore.Slot(str)
    def update_label(self, label: str):
        self.label_title.setText(LABEL_TEXT_FORMAT.format(label))
        self.measured_phase_label.hide()
        self.measured_phase_label_value.hide()

    @QtCore.Slot(str)
    def update_window_title(self, label: str):
        self.main_window.ui_component.setWindowTitle(label)

    @QtCore.Slot(str)
    def update_ui(self, label: str):
        """
        Toggle all the other layout options, so only the one
        that works for the current algorithm choice is shown.
        """
        # We are given the string display name for the algorithm
        # we want to convert that to the widget name for the layout
        # to show
        key = COMBO_BOX_LAYOUT_MAPPING[label]
        layout = self.layouts[key]

        for layouts_to_hide in self.layouts.values():
            layouts_to_hide.hide()

        layout.show()
