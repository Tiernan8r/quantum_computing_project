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
import qcp.register as reg
from qcp.ui.widgets.embedded_graph import EmbeddedGraph
from typing import List, Any


class GraphWidget(EmbeddedGraph):
    """
    Custom widget to embed a matplotlib plot canvas into our UI.
    """

    def __init__(self, graph_widget: QtWidgets.QWidget):
        super().__init__(graph_widget)
        self.display()

    def display(self, qregister: Matrix = None):
        """
        Calculate the probability distributions for the given quantum
        register to be in each qbit state, and plot the probabilities
        as a histogram within the embedded matplotlib canvas widget

        :param Matrix qregister: The column vector representing our qbit
            state.
        """
        self.axes.clear()

        title = "Measured Quantum States:"
        xlabel, ylabel = "states", "probabilities"

        # TODO: remove placeholders
        x: List[Any] = list(range(10))
        y = [2**i for i in x]

        if qregister is not None:
            x = list(range(qregister.num_rows))
            y = reg.measure(qregister)

        x = [f"|{bin(i)[2:]}>" for i in x]

        self._plot_line(x, y, title=title,
                        xlabel=xlabel, ylabel=ylabel)

        self.figure_canvas.draw()
