from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow


class AbstractComponent(QObject):

    def __init__(self, main_window: QMainWindow, *args, **kwargs):
        super(QObject).__init__(*args, **kwargs)
        self.main_window = main_window
        self.setup_signals()

    def setup_signals(self):
        pass
