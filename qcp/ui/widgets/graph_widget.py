from qcp.matrices import Matrix
from qcp.ui.widgets.embedded_graph import EmbeddedGraph
import logging
import matplotlib
from PySide6 import QtWidgets

matplotlib.use('Qt5Agg')


class GraphWidget(EmbeddedGraph):

    def __init__(self, graph_widget: QtWidgets.QWidget, width, height, dpi):
        super().__init__(graph_widget, width, height, dpi)
        self.display()

    def display(self, qregister: Matrix = None):
        self.axes.clear()

        title = "Measured Quantum States:"
        xlabel, ylabel = "states", "probabilities"

        # TODO: remove placeholders
        x = range(10)
        y = [2**i for i in x]
        x = [f"|{bin(i)[2:]}>" for i in x]

        if qregister is not None:
            x = range(qregister.num_columns)
            # TODO: someway to measure qregister
            y = qregister.measure()
        
        self._plot_line(x, y, title=title,
                        xlabel=xlabel, ylabel=ylabel)

        self.figure_canvas.draw()
