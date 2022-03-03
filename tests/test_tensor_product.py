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
from qcp.matrices import DefaultMatrix, DenseMatrix, SparseMatrix
from qcp.tensor_product import tensor_product

IDENTITY = SparseMatrix.identity(2)


def test_tensor_product_dense_with_identity():

    A = DenseMatrix([[1, 2], [3, 4]])

    C = tp.tensor_product(IDENTITY, A)

    expected = DenseMatrix(
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

    # Disgustingly complicated, and I realise the irony of using "SparseMatrix"
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


def test_tensor_product_non_square():

    mat1_1 = DefaultMatrix([[5, 1]])
    mat1_2 = DefaultMatrix([[9, 4]])
    mat1_3 = DefaultMatrix([[5, 3, 1],
                            [4, 9, 1]])

    mat2_1 = DefaultMatrix([[6, 8]])
    mat2_2 = DefaultMatrix([[7, 2]])
    mat2_3 = DefaultMatrix([[7, 1, 2],
                            [2, 5, 3]])

    ans1 = DefaultMatrix([[30, 40, 6, 8]])
    ans2 = DefaultMatrix([[63, 18, 28, 8]])
    ans3 = DefaultMatrix([[35, 5, 10, 21, 3, 6, 7, 1, 2],
                          [10, 25, 15, 6, 15, 9, 2, 5, 3],
                          [28, 4, 8, 63, 9, 18, 7, 1, 2],
                          [8, 20, 12, 18, 45, 27, 2, 5, 3]])

    assert tp.tensor_product(mat1_1, mat2_1).get_state() == ans1.get_state()
    assert tp.tensor_product(mat1_2, mat2_2).get_state() == ans2.get_state()
    assert tp.tensor_product(mat1_3, mat2_3).get_state() == ans3.get_state()


def test_tensor_product_square():
    # M1 and M2 Define matrices that were choosen at random to test the tensor product function,and (tensor_product(transpose(M1[n]),transpose(M2[n])) == transpose(Ans[n]))
    # each M1 matrix has the operation applied to the corresponding M2 matrix
    # the result of the tensor product function is then compared with the seperatly calculated answer key stored in Ans
    M1_1 = DefaultMatrix([[2, 3],
                          [5, 3]])
    M1_2 = DefaultMatrix([[6, 5],
                          [3, 1]])
    M1_3 = DefaultMatrix([[3.6, 9.8],
                          [2.1, 5.3]])
    M1_4 = DefaultMatrix([[7.6, 8.0],
                          [complex(3, 2), 2.4]])
    M1_5 = DefaultMatrix([[4, 6, 9],
                          [0, 1, 0],
                          [0, 6, 7]])

    M2_1 = DefaultMatrix([[4, 6],
                          [3, 4]])
    M2_2 = DefaultMatrix([[4, 9],
                          [3, 7]])
    M2_3 = DefaultMatrix([[7.6, 8.0],
                          [9.9, 2.4]])
    M2_4 = DefaultMatrix(
        [[complex(1, 1), 9.8],
         [2.1, complex(0, 2)]])

    M2_5 = DefaultMatrix([[5, 7, 8],
                          [2, 1, 0],
                          [9, 2, 1]])

    Ans1 = DefaultMatrix([[8, 12, 12, 18],
                          [6, 8, 9, 12],
                          [20, 30, 12, 18],
                          [15, 20, 9, 12]])
    Ans2 = DefaultMatrix(
        [[24, 54, 20, 45],
         [18, 42, 15, 35],
         [12, 27, 4, 9],
         [9, 21, 3, 7]])
    Ans3 = DefaultMatrix(
        [[27.36, 28.8, 74.48, 78.4],
         [35.64, 8.64, 97.02, 23.52],
         [15.96, 16.8, 40.28, 42.4],
         [20.79, 5.04, 52.47, 12.72]])

    Ans4 = DefaultMatrix([[complex(7.6, 7.6), complex(8, 8), 74.48, 78.4],
                          [complex(1, 5), complex(2.4, 2.4),
                           complex(29.4, 19.6), 23.52],
                          [15.96, 16.8, complex(0, 15.2), complex(0, 16)],
                          [complex(6.3, 4.2), 5.04, complex(-4, 6), complex(0, 4.8)]])

    Ans5 = DefaultMatrix([[20, 28, 32, 30, 42, 48, 45, 63, 72],
                          [8, 4, 0, 12, 6, 0, 18, 9, 0],
                          [36, 8, 4, 54, 12, 6, 81, 18, 9],
                          [0, 0, 0, 5, 7, 8, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0, 0],
                          [0, 0, 0, 9, 2, 1, 0, 0, 0],
                          [0, 0, 0, 30, 42, 48, 35, 49, 56],
                          [0, 0, 0, 12, 6, 0, 14, 7, 0],
                          [0, 0, 0, 54, 12, 6, 63, 14, 7]])

    assert tp.tensor_product(M1_1, M2_1).get_state() == Ans1.get_state()
    assert tp.tensor_product(M1_2, M2_2).get_state() == Ans2.get_state()
    assert tp.tensor_product(M1_3, M2_3).get_state() == Ans3.get_state()
    assert tp.tensor_product(M1_4, M2_4).get_state() == Ans4.get_state()
    assert tp.tensor_product(M1_5, M2_5).get_state() == Ans5.get_state()


def test_tensor_product_square_numbers():

    ret = True

    # Tests Square matrices that have a definiative and easliy computable answer
    # this allows for more tests with fewer numbers stored on larger matrices
    for size in range(0, 10):
        for index in range(0, 10):
            Ques = [[index] * size]*size
            Ans = [[index**2]*(size**2)]*(size**2)
            ret = ret and (tp.tensor_product(Ques, Ques) == Ans)

    return ret
