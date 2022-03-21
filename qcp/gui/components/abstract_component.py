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
from PySide6 import QtCore, QtWidgets


class AbstractComponent(QtCore.QObject):
    """
    A generalised Abstract component of out UI, in which the section
    of the UI that the component controls is setup, with it's behaviour
    defined in the code.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        """
        Setup the UI component, referencing the MainWindow UI element

        :param QtWidgets.QMainWindow main_window: The main window
            element of our UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.setup_signals()

    def setup_signals(self):
        """
        Setup any UI signals and events associated with interacting with
        this part of the UI.
        """
        self._find_widgets()

    def _find_widgets(self):
        """
        Searches the UI elements to get python object references to the ones
        that are relevant to the operation of this UI component.
        """
        pass
