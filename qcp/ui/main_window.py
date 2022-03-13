# File: main.py
import sys
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile, QIODevice
from qcp.ui.constants import UI_FILENAME
import qcp.ui.components as comp


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui_component = self.load_ui()
        self.ui_component.setWindowTitle("Grover's Algorithm")

        self.graph_component = comp.GraphComponent(self)
        self.input_component = comp.InputComponent(self)
        self.button_component = comp.ButtonComponent(
            self, self.input_component.input_search, self.input_component.input_target)

        self.simulator = comp.SimulatorComponent(
            self, self.button_component, self.graph_component)

    def show(self):
        # super().show()
        self.ui_component.show()

    def load_ui(self) -> QMainWindow:

        # Load in the 'form.ui' file where the ui layout is defined
        path = os.path.join(os.path.dirname(__file__), UI_FILENAME)
        ui_file = QFile(path)

        if not ui_file.open(QIODevice.ReadOnly):
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
