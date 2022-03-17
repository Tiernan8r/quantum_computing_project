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
import sys
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile, QIODevice
from qcp.ui.constants import UI_FILENAME
import qcp.ui.components as comp


class MainWindow(QMainWindow):
    """
    A Class to handle the behaviour of the overall UI window
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the MainWindow object

        :param *args: variable length extra arguments to pass down
            to QMainWindow
        :param **kwargs: dictionary parameters to pass to QMainWindow
        """
        super().__init__(*args, **kwargs)

        self.ui_component = self.load_ui()
        self.ui_component.setWindowTitle("Grover's Algorithm")

        self.graph_component = comp.GraphComponent(self)
        self.input_component = comp.InputComponent(self)
        self.button_component = comp.ButtonComponent(
            self, self.input_component.input_search,
            self.input_component.input_target)

        self.simulator = comp.SimulatorComponent(
            self, self.button_component, self.graph_component)

    def show(self):
        """
        Shows the loaded UI if hidden.
        """
        self.ui_component.show()

    def load_ui(self) -> QMainWindow:
        """
        Reads the UI XML file and converts it into a QT widget,
        and returns the widget

        returns:
            QMainWindow: The Main Window element of our UI, with widget
            elements laid out as defined in the UI file.
        """
        # Load in the 'form.ui' file where the ui layout is defined
        path = os.path.join(os.path.dirname(__file__), UI_FILENAME)
        ui_file = QFile(path)

        if not ui_file.open(QIODevice.ReadOnly):  # type: ignore
            print(f"Cannot open {UI_FILENAME}: {ui_file.errorString()}")
            sys.exit(-1)

        # Load the file using the QT UI loader class and return the
        # ui widget representing the layout
        loader = QUiLoader()
        ui_window = loader.load(ui_file)
        ui_file.close()
        if not ui_window:
            print(loader.errorString())
            sys.exit(-1)

        return ui_window
