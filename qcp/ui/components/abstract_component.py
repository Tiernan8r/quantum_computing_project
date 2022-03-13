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
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow


class AbstractComponent(QObject):

    def __init__(self, main_window: QMainWindow, *args, **kwargs):
        super(QObject).__init__(*args, **kwargs)
        self.main_window = main_window
        self.setup_signals()

    def setup_signals(self):
        pass
