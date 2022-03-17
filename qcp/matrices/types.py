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
from typing import Dict, List, Union

#: Type Alias for the allowed types for the matrix elements
SCALARS = Union[complex, float, int]
#: Typle Alias for the allowed matrix element types as a tuple
SCALARS_T = (complex, float, int)
#: Type Alias for the type of a matrix row, as a list representation
VECTOR = List[SCALARS]
#: Type Alias for the type of the matrix content, a 2D nested list of allowed
#: matrix element types
MATRIX = List[VECTOR]
#: Type Alias for the storage method used in SparseMatrix, the entries of the
#: matrix are stored in a nested dictionary, where values are looked up by
#: row/column index
SPARSE = Dict[int, Dict[int, SCALARS]]
