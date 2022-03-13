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
from PySide6 import QtWidgets
from qcp.matrices import Matrix
from qcp.ui.widgets.embedded_graph import EmbeddedGraph


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
