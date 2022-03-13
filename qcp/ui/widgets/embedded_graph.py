from PySide6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
import matplotlib

matplotlib.use('Qt5Agg')


class EmbeddedGraph(QtWidgets.QWidget):

    def __init__(self, graph_widget: QtWidgets.QWidget, width, height, dpi=100):
        super().__init__(parent=graph_widget)
        self.graph_widget = graph_widget

        self.figure, self.toolbar, self.axes = None, None, None

        self._setup_canvas(width, height, dpi)
        self._setup_layouts()

    def hide(self) -> None:
        super().hide()
        self.graph_widget.hide()
        self.figure_canvas.hide()
        self.toolbar.hide()

    def show(self) -> None:
        super().show()
        self.graph_widget.show()
        self.figure_canvas.show()
        self.toolbar.show()

    def _setup_canvas(self, width, height, dpi):
        # self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.figure = Figure()
        self.figure.tight_layout()
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self)

    def _setup_layouts(self):

        graph_frame_layout = QtWidgets.QGridLayout(parent=self.graph_widget)
        graph_frame_layout.addWidget(self.toolbar)
        graph_frame_layout.addWidget(self.figure_canvas)

        self.setLayout(graph_frame_layout)

        parent_layout = QtWidgets.QHBoxLayout(parent=self.graph_widget)
        parent_layout.addWidget(self)

        self.graph_widget.setLayout(parent_layout)

        self.figure_canvas.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.figure_canvas.updateGeometry()

    def _plot_line(self, x, y, title, xlabel, ylabel, legend=None, line_style="-"):
        self.axes.plot(x, y, line_style)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        if legend is not None:
            self.axes.legend(legend)
