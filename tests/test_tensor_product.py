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
from qcp.matrices import DefaultMatrix
import tests.test_helpers as h


def test_tensor_product_with_identity():

    A = DefaultMatrix([[1, 2], [3, 4]])
    id = DefaultMatrix.identity(2)

    C = tp.tensor_product(id, A)

    expected = DefaultMatrix(
        [
            [1, 2, 0, 0],
            [3, 4, 0, 0],
            [0, 0, 1, 2],
            [0, 0, 3, 4]
        ]
    )

    h.compare_matrices(C, expected)


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

    tens1 = tp.tensor_product(mat1_1, mat2_1)
    tens2 = tp.tensor_product(mat1_2, mat2_2)
    tens3 = tp.tensor_product(mat1_3, mat2_3)

    h.compare_matrices(tens1, ans1)
    h.compare_matrices(tens2, ans2)
    h.compare_matrices(tens3, ans3)


def test_tensor_product_square():
    # M1 and M2 Define matrices that were choosen at random to test the tensor
    # product function each M1 matrix has the operation applied to the
    # corresponding M2 matrix the result of the tensor product function is then
    # compared with the seperatly calculated answer key stored in Ans
    m1_1 = DefaultMatrix([[2, 3],
                          [5, 3]])
    m1_2 = DefaultMatrix([[6, 5],
                          [3, 1]])
    m1_3 = DefaultMatrix([[3.6, 9.8],
                          [2.1, 5.3]])
    m1_4 = DefaultMatrix([[7.6, 8.0],
                          [3+2j, 2.4]])
    m1_5 = DefaultMatrix([[4, 6, 9],
                          [0, 1, 0],
                          [0, 6, 7]])

    m2_1 = DefaultMatrix([[4, 6],
                          [3, 4]])
    m2_2 = DefaultMatrix([[4, 9],
                          [3, 7]])
    m2_3 = DefaultMatrix([[7.6, 8.0],
                          [9.9, 2.4]])
    m2_4 = DefaultMatrix([[1+1j, 9.8],
                          [2.1, 2j]])
    m2_5 = DefaultMatrix([[5, 7, 8],
                          [2, 1, 0],
                          [9, 2, 1]])

    ans1 = DefaultMatrix([[8, 12, 12, 18],
                          [6, 8, 9, 12],
                          [20, 30, 12, 18],
                          [15, 20, 9, 12]])
    ans2 = DefaultMatrix([[24, 54, 20, 45],
                          [18, 42, 15, 35],
                          [12, 27, 4, 9],
                          [9, 21, 3, 7]])
    ans3 = DefaultMatrix([[27.36, 28.8, 74.48, 78.4],
                          [35.64, 8.64, 97.02, 23.52],
                          [15.96, 16.8, 40.28, 42.4],
                          [20.79, 5.04, 52.47, 12.72]])
    ans4 = DefaultMatrix([[7.6+7.6j, 74.48, 8+8j, 78.4],
                          [15.96, 15.2j, 16.8, 16j],
                          [1+5j, 29.4+19.6j, 2.4+2.4j, 23.52],
                          [6.3+4.2j, -4+6j, 5.04, 4.8j]])
    ans5 = DefaultMatrix([[20, 28, 32, 30, 42, 48, 45, 63, 72],
                          [8, 4, 0, 12, 6, 0, 18, 9, 0],
                          [36, 8, 4, 54, 12, 6, 81, 18, 9],
                          [0, 0, 0, 5, 7, 8, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0, 0],
                          [0, 0, 0, 9, 2, 1, 0, 0, 0],
                          [0, 0, 0, 30, 42, 48, 35, 49, 56],
                          [0, 0, 0, 12, 6, 0, 14, 7, 0],
                          [0, 0, 0, 54, 12, 6, 63, 14, 7]])

    tens1 = tp.tensor_product(m1_1, m2_1)
    tens2 = tp.tensor_product(m1_2, m2_2)
    tens3 = tp.tensor_product(m1_3, m2_3)
    tens4 = tp.tensor_product(m1_4, m2_4)
    tens5 = tp.tensor_product(m1_5, m2_5)

    h.compare_matrices(tens1, ans1)
    h.compare_matrices(tens2, ans2)
    h.compare_matrices(tens3, ans3)
    h.compare_matrices(tens4, ans4)
    h.compare_matrices(tens5, ans5)
