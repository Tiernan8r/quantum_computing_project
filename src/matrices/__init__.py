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
from src.matrices.matrix import Matrix  # noqa: F401
from src.matrices.sparse_matrix import SparseMatrix  # noqa: F401
from src.matrices.dense_matrix import DenseMatrix  # noqa: F401

from src.matrices.types import SCALARS, SCALARS_TYPES, \
    VECTOR, MATRIX, SPARSE  # noqa: F401

DefaultMatrix = SparseMatrix
