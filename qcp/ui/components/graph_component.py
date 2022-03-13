from qcp.ui.components.abstract_component import AbstractComponent
from PySide6 import QtWidgets
from qcp.ui.widgets import GraphWidget
from qcp.ui.constants import GRAPH_WIDGET_NAME


class GraphComponent(AbstractComponent):

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        super().__init__(main_window, *args, **kwargs)

        self.graph_widget.hide()

    def setup_signals(self):
        self._find_graph_widget()

        self.refresh()

    def _find_graph_widget(self):
        widgets = self.main_window.ui_component.findChildren(QtWidgets.QWidget)
        for w in widgets:
            if w.objectName() == GRAPH_WIDGET_NAME:
                self.graph_widget = GraphWidget(w, width=300, height=100, dpi=100)

    def refresh(self):
        # TODO: need to get qregister here
        self.graph_widget.display()

    def hide(self):
        self.graph_widget.hide()

    def show(self):
        self.graph_widget.show()
