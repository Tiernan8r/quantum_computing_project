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
from qcp.ui.components import AbstractComponent
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
                self.graph_widget = GraphWidget(
                    w, width=300, height=100, dpi=100)

    def refresh(self):
        # TODO: need to get qregister here
        self.graph_widget.display()

    def hide(self):
        self.graph_widget.hide()

    def show(self):
        self.graph_widget.show()
