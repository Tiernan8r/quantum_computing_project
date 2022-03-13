from qcp.ui.components import AbstractComponent
from PySide6 import QtWidgets
from PySide6 import QtCore
import time
from qcp.ui.constants import THREAD_PAUSE


class SimulatorComponent(AbstractComponent):

    def __init__(self, main_window: QtWidgets.QMainWindow, button_component, graph_component, *args, **kwargs):
        self.button_component = button_component
        self.graph_component = graph_component
        super().__init__(main_window, *args, **kwargs)

        self.graph_component.hide()

    def setup_signals(self):
        self.qcp_thread = SimulateQuantumComputerThread()

        self.qcp_thread.finished.connect(
            self.button_component.update_lcd_displays)
        # Hide the cancel button if the calculation finishes
        self.qcp_thread.finished.connect(
            self.button_component.cancel_button.hide)

        self.qcp_thread.finished.connect(self.simulation_finished)

    def run_simulation(self):
        # Code to initialise the qcp simulation on the qthread
        if not self.qcp_thread.isRunning():
            self.qcp_thread.exiting = False
            self.qcp_thread.start()
            while not self.qcp_thread.isRunning():
                time.sleep(THREAD_PAUSE)

    def simulation_finished(self):
        self.graph_component.show()


class SimulateQuantumComputerThread(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def run(self):
        self.quit()
