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
from PySide6 import QtWidgets
from PySide6 import QtCore
from qcp.ui.components import AbstractComponent
from qcp.ui.constants import BUTTON_CANCEL_SEARCH_BUTTON, \
    BUTTON_SEARCH_BUTTON, BUTTON_PROGRESS_BAR, BUTTON_PROGRESS_BAR_TICK_RATE, \
    THREAD_PAUSE


class ButtonComponent(AbstractComponent):
    """
    Component of the UI that handles button click behaviour.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 search: QtWidgets.QTextEdit, target: QtWidgets.QLineEdit,
                 *args, **kwargs):
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Setup what happens when the buttons in the UI are clicked.
        """
        self._find_widgets()

        self.progress_bar.hide()
        self.progress_bar.reset()

        self.cancel_button.hide()

        self.pb_thread = ProgressBarThread(self.progress_bar)

        self.search_button.clicked.connect(self.initiate_search)
        self.cancel_button.clicked.connect(self.cancel_search)

    def _find_widgets(self):
        buttons = self.main_window.ui_component.findChildren(
            QtWidgets.QPushButton)
        for b in buttons:
            if b.objectName() == BUTTON_SEARCH_BUTTON:
                self.search_button = b
            if b.objectName() == BUTTON_CANCEL_SEARCH_BUTTON:
                self.cancel_button = b

        progress_bars = self.main_window.ui_component.findChildren(
            QtWidgets.QProgressBar)
        for pb in progress_bars:
            if pb.objectName() == BUTTON_PROGRESS_BAR:
                self.progress_bar = pb

    def initiate_search(self):
        """
        Start the running of the Quantum Computer Simulator on a
        separate QThread.

        Show the cancel button, so that the QThread can be killed before the
        calculation completes.

        Startup the QThread that updates the progress bar so that it swirls
        overtime, to visualise that the computer is running a calculation in
        the background.
        """
        self.cancel_button.show()

        self.tick_progress_bar()
        self.main_window.simulator.run_simulation()
        time.sleep(THREAD_PAUSE)

        self.pb_thread.exiting = True

    def cancel_search(self):
        """
        Kill the Simulation QThread when the button is clicked.

        Hide and reset the progress bar.

        Then hide the cancel button as a calculation is no longer running.
        """
        if self.pb_thread.isRunning():
            self.pb_thread.exiting = True
            while self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)
        if self.main_window.simulator.qcp_thread.isRunning():
            self.qcp_thread.quit()
            time.sleep(THREAD_PAUSE)

        self.cancel_button.hide()

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


class ProgressBarThread(QtCore.QThread):
    """
    Thread that handles visually updating the progress bar value
    every tick, so that it fills slowly, then resets to zero when
    full.
    """

    def __init__(self, progress_bar: QtWidgets.QProgressBar, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.pb = progress_bar
        self.exiting = False

    def run(self):
        """
        Startup the thread, and run the desired actions every loop.
        """
        self.pb.setVisible(True)
        self.pb.reset()
        while not self.exiting:
            val = (self.pb.value() + 1) % self.pb.maximum()
            if val < self.pb.minimum():
                val = self.pb.minimum()

            self.pb.setValue(val)
            self.msleep(BUTTON_PROGRESS_BAR_TICK_RATE)

        self.pb.reset()
        self.pb.hide()
        self.quit()
