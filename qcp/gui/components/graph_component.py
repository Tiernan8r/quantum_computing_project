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
import matplotlib
import qcp.register as reg
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtWidgets
from qcp.gui.components import AbstractComponent
from qcp.gui.components.constants import GRAPH_WIDGET_NAME
from qcp.matrices import Matrix

matplotlib.use('Qt5Agg')


class GraphComponent(AbstractComponent):
    """
    UI component that handles the behaviour of the embedded matplotlib graph
    """

    def __init__(self, main_window: QtWidgets.QMainWindow, *args, **kwargs):
        """
        Initialise the GraphComponent object, referencing the main window
        element.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

        self.show()

    def setup_signals(self):
        """
        Find the graph widget to embed the matplotlib canvas in, and draw the
        canvas
        """
        super().setup_signals()

        self._setup_canvas()
        self._setup_layouts()

    def _find_widgets(self):
        """
        Determine the graph widget in the UI to use to embed the matplotlib
        canvas into.
        """
        widgets = self.main_window.ui_component.findChildren(QtWidgets.QWidget)
        for w in widgets:
            if w.objectName() == GRAPH_WIDGET_NAME:
                self.graph_widget: QtWidgets.QWidget = w

    def _setup_canvas(self):
        """
        Create a matplotlib UI canvas
        """
        self.figure = Figure()
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self.graph_widget)

    def _setup_layouts(self):
        """
        Embed this widget and the matplotlib canvas into the graph frame
        widget
        """
        graph_frame_layout = QtWidgets.QGridLayout(parent=self.graph_widget)
        graph_frame_layout.addWidget(self.toolbar)
        graph_frame_layout.addWidget(self.figure_canvas)

        self.graph_widget.setLayout(graph_frame_layout)

    def hide(self):
        """
        Hide the matplotlib graph if shown
        """
        if self.graph_widget.isVisible():
            self.graph_widget.hide()

    def show(self):
        """
        Show the matplotlib graph if hidden
        """
        if self.graph_widget.isHidden():
            self.graph_widget.show()

    def display(self, qregister: Matrix = None):
        """
        Calculate the probability distributions for the given quantum
        register to be in each qbit state, and plot the probabilities
        as a histogram within the embedded matplotlib canvas widget

        :param Matrix qregister: The column vector representing our qbit
            state.
        """
        self.show()
        self.axes.clear()

        title = "Measured Quantum States:"
        xlabel, ylabel = "states", "probabilities"

        if qregister is None:
            return

        x = [f"|{i}>" for i in range(qregister.num_rows)]
        y = reg.measure(qregister)

        self._plot(x, y, title=title,
                   xlabel=xlabel, ylabel=ylabel)

        self.figure_canvas.draw()

    def _plot(self, x: list, y: list, title: str, xlabel: str,
              ylabel: str, legend: list = None):
        """
        Plot the given x/y values on the matplotlib canvas, displaying with
        the given xlabel/ylabel/title and legend.

        :param list x: The x values to plot
        :param list y: The y values to plot
        :param str title: The title of the plot
        :param str xlabel: The label for the x axis
        :param str ylabel: The label for the y axis
        :param list legend: The (optional) legend for the plot
        :param str line_style: The line style for the plot, defaults to solid
            lines
        """
        self.axes.bar(x, y)

        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        if legend is not None:
            self.axes.legend(legend)
