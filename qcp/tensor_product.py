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
from typing import List
from matrices import Matrix, SquareMatrix


def tensor_product(A: Matrix, B: Matrix) -> Matrix:
    """
    Compute the tensor product between two matrices, and return the
    resultant Matrix

    :param A Matrix: An n*n square matrix
    :param B Matrix: Second n*n square matrix to tensor product with
    :returns: An (n^2)*(n^2) matrix of the tensor product.
    """
    assert len(A) == len(B), "A and B have mismatched column dimensions!"
    assert len(A[0]) == len(B[0]), "A and B have mismatched row dimensions!"

    n = len(A)

    tensor_product_width = n * n

    # creates an (n^2)*(n^2) list for the answer matrix
    entries = [
        [0.0 for _ in range(n * n)] for _ in range(n * n)
    ]

    # The tensor product is defined as follows:
    # A * B =
    # [A00 * B, A01 * B, ... A0n * B]
    # [A10 * B, A11 * B, ... A1n * B]
    # [...               ...        ]
    # [An0 * B, A1n * B, ... Ann * B]

    # Take a 2*2 case as an example:
    # A =   [1, 1]
    #       [1, 1]
    # B =   [2, 3]
    #       [4, 5]
    # C = A * B =
    #       [2, 3, 2, 3]
    #       [4, 5, 4, 5]
    #       [2, 3, 2, 3]
    #       [4, 5, 4, 5]

    # The values are populated by iterating over the full sized matrix (C[i][j]
    # in this example)
    # To determine the A prefactor (A00/A01/etc...) the i,j are floor divided
    # by the size of A

    # The B values need to loop over the rows and columns in subgrids, this is
    # achieved by taking the modulus of the i,j indices:

    # i ->
    #   __     __
    #  /  \   /  \
    # [2, 3,  2, 3] \   j
    # [4, 5,  4, 5] /   |
    #                   V
    # [2, 3,  2, 3] \
    # [4, 5,  4, 5] /

    for i in range(tensor_product_width):
        for j in range(tensor_product_width):

            # A[k][l]:
            k = i // n
            l = j // n  # noqa: E741

            # B[p][q]
            p = i % n
            q = j % n

            entries[i][j] = A[k][l] * B[p][q]

    return SquareMatrix(entries)
