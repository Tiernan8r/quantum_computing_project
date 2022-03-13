from qcp.ui.components import AbstractComponent
from PySide6 import QtWidgets
from PySide6 import QtCore
from qcp.ui.constants import BUTTON_CANCEL_SEARCH_BUTTON, BUTTON_SEARCH_BUTTON, BUTTON_PROGRESS_BAR, BUTTON_PROGRESS_BAR_TICK_RATE, LCD_CLASSICAL, LCD_GROVER, THREAD_PAUSE
import time


class ButtonComponent(AbstractComponent):

    def __init__(self, main_window: QtWidgets.QMainWindow, search: QtWidgets.QTextEdit, target: QtWidgets.QLineEdit, *args, **kwargs):
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
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

        progressBars = self.main_window.ui_component.findChildren(
            QtWidgets.QProgressBar)
        for pb in progressBars:
            if pb.objectName() == BUTTON_PROGRESS_BAR:
                self.progress_bar = pb


    def initiate_search(self):
        self.cancel_button.show()

        self.tick_progress_bar()
        self.main_window.simulator.run_simulation()
        time.sleep(THREAD_PAUSE)

        self.pb_thread.exiting = True

        return

    def cancel_search(self):
        if self.pb_thread.isRunning():
            self.pb_thread.exiting = True
            while self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)
        if self.main_window.simulator.qcp_thread.isRunning():
            self.qcp_thread.quit()
            time.sleep(THREAD_PAUSE)

        self.cancel_button.hide()

    def tick_progress_bar(self):
        if not self.pb_thread.isRunning():
            self.pb_thread.exiting = False
            self.pb_thread.start()
            # wait until the thread has started
            while not self.pb_thread.isRunning():
                time.sleep(THREAD_PAUSE)


class ProgressBarThread(QtCore.QThread):

    def __init__(self, progress_bar: QtWidgets.QProgressBar, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.pb = progress_bar
        self.exiting = False

    def run(self):
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
