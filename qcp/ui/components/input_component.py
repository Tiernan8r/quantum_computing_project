from cgitb import text
from qcp.ui.components import AbstractComponent
from PySide6 import QtWidgets
import logging
from qcp.ui.constants import INPUT_SEARCH_WIDGET_NAME, INPUT_TARGET_WIDGET_NAME, INPUT_BROWSE_FILE


class InputComponent(AbstractComponent):

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        self._find_widgets()

        self.input_browse.clicked.connect(self.browse_files)

    def _find_widgets(self):
        lineEdits = self.main_window.ui_component.findChildren(
            QtWidgets.QLineEdit)
        for lineEdit in lineEdits:
            if lineEdit.objectName() == INPUT_TARGET_WIDGET_NAME:
                self.input_target = lineEdit

        textEdit = self.main_window.ui_component.findChild(QtWidgets.QTextEdit)
        if textEdit is not None and textEdit.objectName() == INPUT_SEARCH_WIDGET_NAME:
            self.input_search = textEdit

        buttons = self.main_window.ui_component.findChildren(
            QtWidgets.QPushButton)
        for b in buttons:
            if b.objectName() == INPUT_BROWSE_FILE:
                self.input_browse = b

    def browse_files(self):
        dialog = QtWidgets.QFileDialog(self.main_window)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter("Text (*.txt *.json *.cvc *.yml)")
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        file_names = []
        if dialog.exec_():
            file_names = dialog.selectedFiles()
        
        if len(file_names) != 1:
            return

        file_name = file_names[0]

        with open(file_name, "r") as f:
            content = f.read()
            self.input_search.setPlainText(content)
