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


def test_tensor_sparse():

    # Test 3*2 matrix, tensor 2*3
    A = SparseMatrix([[1, 2, 3], [4, 5, 6]])
    B = SparseMatrix([[1, 2], [3, 4], [5, 6]])

    C = tp.tensor_product(A, B)

    expected = SparseMatrix([
        [1, 2, 2, 4, 3, 6],
        [3, 4, 6, 8, 9, 12],
        [5, 6, 10, 12, 15, 18],
        [4, 8, 5, 10, 6, 12],
        [12, 16, 15, 20, 18, 24],
        [20, 24, 25, 30, 30, 36]
    ])

    assert C.get_state() == expected.get_state()

    D = SparseMatrix([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20]
    ])

    E = SparseMatrix([
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7]
    ])

    F = tp.tensor_product(D, E)

    # Disgusting comoplicated, and I realise the irony of using "SparseMatrix"
    # with such a dense matrix...
    expected2 = SparseMatrix([
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [1, 2, 3, 4, 5, 6, 7, 2, 4, 6, 8, 10, 12, 14, 3, 6, 9, 12, 15,
            18, 21, 4, 8, 12, 16, 20, 24, 28, 5, 10, 15, 20, 25, 30, 35],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [6, 12, 18, 24, 30, 36, 42, 7, 14, 21, 28, 35, 42, 49, 8, 16, 24, 32,
            40, 48, 56, 9, 18, 27, 36, 45, 54, 63, 10, 20, 30, 40, 50, 60, 70],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [11, 22, 33, 44, 55, 66, 77, 12, 24, 36, 48, 60, 72, 84, 13, 26, 39,
            52, 65, 78, 91, 14, 28, 42, 56, 70, 84, 98, 15, 30, 45, 60, 75,
            90, 105],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
        [16, 32, 48, 64, 80, 96, 112, 17, 34, 51, 68, 85, 102, 119, 18, 36,
            54, 72, 90, 108, 126, 19, 38, 57, 76, 95, 114, 133, 20, 40, 60,
            80, 100, 120, 140],
    ])

    assert F.get_state() == expected2.get_state()
