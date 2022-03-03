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
from qcp.tensor_product import tensor_product
from qcp.matrices import DefaultMatrix

IDENTITY = DefaultMatrix.identity(2)


def transpose(m):
    ret = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    return ret


def test_tensor_product_with_identity():

    A = DefaultMatrix([[1, 2], [3, 4]])

    C = tensor_product(IDENTITY, A)

    expected = DefaultMatrix(
        [
            [1, 2, 0, 0],
            [3, 4, 0, 0],
            [0, 0, 1, 2],
            [0, 0, 3, 4]
        ]
    )

    assert C.get_state() == expected.get_state()


def tensor_test_smallnonsquare():

    # nonsquare matrices to be incorparted into the below function
    ret = True

    M1 = [[[5, 1]],
          [[9, 4]],
          [[5, 3, 1], [4, 9, 1]]]

    M2 = [[[6, 8]],
          [[7, 2]],
          [[7, 1, 2], [2, 5, 3]]]

    Ans = [[[30, 40, 6, 8]],
           [[35, 5, 10, 21, 3, 6, 7, 1, 2], [10, 25, 15, 6, 15, 9, 2, 5, 3], [
               28, 4, 8, 63, 9, 18, 7, 1, 2], [8, 20, 12, 18, 45, 27, 2, 5, 3]],
           [[63, 18, 28, 8]]]

    for n in range(0, len(Ans)):
        ret = ret and (tensor_product(M1[n], M2[n]) == Ans[n]) and (
            tensor_product(transpose(M1[n]), transpose(M2[n])) == transpose(Ans[n]))

    return ret


def tensor_test_square():

    # ret => variable to return
    ret = True

    # M1 and M2 Define matrices that were choosen at random to test the tensor product function,and (tensor_product(transpose(M1[n]),transpose(M2[n])) == transpose(Ans[n]))
    # each M1 matrix has the operation applied to the corresponding M2 matrix
    # the result of the tensor product function is then compared with the seperatly calculated answer key stored in Ans
    M1 = [
         [[2, 3],
          [5, 3]],

         [[6, 5],
          [3, 1]],

         [[3.6, 9.8],
          [2.1, 5.3]],

         [[7.6, 8.0],
          [complex(3, 2), 2.4]]

         [[4, 6, 9],
          [0, 1, 0],
          [0, 6, 7]]]

    M2 = [
         [[4, 6],
          [3, 4]],

         [[4, 9],
          [3, 7]],

         [[7.6, 8.0],
          [9.9, 2.4]],

         [[complex(1, 1), 9.8],
          [2.1, complex(0, 2)]],

        [[5, 7, 8],
             [2, 1, 0],
             [9, 2, 1]]]

    Ans = [
        [[8, 12, 12, 18],
            [6, 8, 9, 12],
            [20, 30, 12, 18],
            [15, 20, 9, 12]],

        [[24, 54, 20, 45],
            [18, 42, 15, 35],
            [12, 27, 4, 9],
            [9, 21, 3, 7]],

        [[27.36, 28.8, 74.48, 78.4],
            [35.64, 8.64, 97.02, 23.52],
            [15.96, 16.8, 40.28, 42.4],
            [20.79, 5.04, 52.47, 12.72]],

        [[complex(7.6, 7.6), complex(8, 8), 74.48, 78.4],
            [complex(1, 5), complex(2.4, 2.4), complex(29.4, 19.6), 23.52],
            [15.96, 16.8, complex(0, 15.2), complex(0, 16)],
            [complex(6.3, 4.2), 5.04, complex(-4, 6), complex(0, 4.8)]],

        [[20, 28, 32, 30, 42, 48, 45, 63, 72],
            [8, 4, 0, 12, 6, 0, 18, 9, 0],
            [36, 8, 4, 54, 12, 6, 81, 18, 9],
            [0, 0, 0, 5, 7, 8, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0, 0],
            [0, 0, 0, 9, 2, 1, 0, 0, 0],
            [0, 0, 0, 30, 42, 48, 35, 49, 56],
            [0, 0, 0, 12, 6, 0, 14, 7, 0],
            [0, 0, 0, 54, 12, 6, 63, 14, 7]]]

    # tests all matrices with thier answers
    # taking the transpose of the matrices doubles the number of tests
    for n in range(0, len(Ans)):
        ret = ret and (tensor_product(M1[n], M2[n]) == Ans[n]) and (
            tensor_product(transpose(M1[n]), transpose(M2[n])) == transpose(Ans[n]))

    return ret


def tensor_test_square_numbers():

    ret = True

    # Tests Square matrices that have a definiative and easliy computable answer
    # this allows for more tests with fewer numbers stored on larger matrices
    for size in range(0, 10):
        for index in range(0, 10):
            Ques = [[index] * size]*size
            Ans = [[index**2]*(size**2)]*(size**2)
            ret = ret and (tensor_product(Ques, Ques) == Ans)

    return ret
