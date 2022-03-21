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
import time

from PySide6 import QtCore, QtWidgets
from qcp.gui.components import AbstractComponent
from qcp.gui.components.constants import (PROGRESS_BAR,
                                          PROGRESS_BAR_TICK_RATE)
from qcp.gui.constants import THREAD_PAUSE


class ProgressBarComponent(AbstractComponent):
    """
    Component of the UI that handles button click behaviour.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 *args, **kwargs):
        """
        Initialise the ButtonComponent object, referencing the main window
        element, and the two text boxes used in the UI.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param QtWidgets.QTextEdit search: The search input box of the UI
        :param QtWidgets.QLineEdit target: The target input box of the UI
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

        self.progress_bar.hide()
        self.progress_bar.reset()

        self.pb_thread = ProgressBarThread(self.progress_bar.minimum(),
                                           self.progress_bar.maximum())
        self.pb_thread.progress_bar_value_change.connect(self._draw_progress)
        self.pb_thread.finished.connect(self._hide_progress_bar)

    def _find_widgets(self):

        progress_bars = self.main_window.ui_component.findChildren(
            QtWidgets.QProgressBar)
        for pb in progress_bars:
            if pb.objectName() == PROGRESS_BAR:
                self.progress_bar: QtWidgets.QProgressBar = pb

    def tick_progress_bar(self):
        """
        Set up the QThread to increment the progress bar widget every
        tick, and reset it when it fills, to visualise that a calculation
        is being run by the UI.
        """
        if not self.pb_thread.isRunning():
            self.pb_thread.exiting = False
            self.pb_thread.start()
            # wait until the thread has started
            while not self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)

    @QtCore.Slot(int)
    def _draw_progress(self, val: int):
        """
        Set the progress bar widget to the provided value whenever the
        signal is called.

        :param int val: The value to set the progress bar to, no checks
        are performed on it's value.
        """
        if self.progress_bar.isHidden():
            self.progress_bar.show()
        self.progress_bar.setValue(val)

    def _hide_progress_bar(self):
        """
        Hide the progress bar widget.
        """
        self.progress_bar.hide()


class ProgressBarThread(QtCore.QThread):
    """
    Thread that handles visually updating the progress bar value
    every tick, so that it fills slowly, then resets to zero when
    full.
    """
    progress_bar_value_change = QtCore.Signal(int)

    def __init__(self, min: int, max: int, parent=None):
        """
        Setup the ProgressBarThread QThread, to calculate the progress
        bar ticker value every iteration.

        :param int min: The minimum value allowed for the progress bar
        :param int max: The maximum allowed value for the progress bar
        """
        super().__init__(parent)
        self.exiting = False
        self.min = min
        self.max = max
        self.pb_val = 0

    def run(self):
        """
        Startup the thread, and run the desired actions every loop.
        """
        self.pb_val = 0
        while not self.exiting:
            val = (self.pb_val + 1) % self.max
            if val < self.min:
                val = self.min

            self.progress_bar_value_change.emit(val)
            self.pb_val = val
            self.msleep(PROGRESS_BAR_TICK_RATE)

        self.quit()
