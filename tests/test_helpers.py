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
from qcp.matrices import Matrix
import cmath

def compare_matrices(A: Matrix, B: Matrix, e=1E-9):
    assert A.num_rows == B.num_rows
    assert A.num_columns == B.num_columns

    for i in range(A.num_columns):
        for j in range(A.num_rows):

            assert cmath.isclose(A[i][j], B[i][j], rel_tol=e)