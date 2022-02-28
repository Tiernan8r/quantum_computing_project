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
import qcp.tensor_product as tp
from qcp.matrices import SquareMatrix, SparseMatrix


def test_tensor_product_square_with_identity():

    A = SquareMatrix([[1, 2], [3, 4]])
    ID = SquareMatrix.identity(2)

    C = tp.tensor_product(ID, A)

    expected = SquareMatrix(
        [
            [1, 2, 0, 0],
            [3, 4, 0, 0],
            [0, 0, 1, 2],
            [0, 0, 3, 4]
        ]
    )

    assert C.get_state() == expected.get_state()


def test_tensor_product_sparse_with_identity():

    A = SparseMatrix({0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}})
    ID = SparseMatrix.identity(2)

    C = tp.tensor_product(ID, A)

    expected = SparseMatrix({
        0: {0: 1, 1: 2},
        1: {0: 3, 1: 4},
        2: {2: 1, 3: 2},
        3: {2: 3, 3: 4}
    })

    assert C.get_state() == expected.get_state()
