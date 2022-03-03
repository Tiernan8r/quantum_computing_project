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
from src.matrices import Matrix, DefaultMatrix
from src.matrices._types import MATRIX
import cmath


def tensor_product(A: Matrix, B: Matrix) -> Matrix:
    """
    Compute the tensor product between two matrices, and return the
    resultant Matrix
    :param A Matrix: An m*n matrix
    :param B Matrix: Second p*q matrix to tensor product with
    :returns: An (m*p)*(n*q) matrix of the tensor product.
    """
    m = len(A)
    n = 0
    if m > 0:
        n = len(A[0])
    p = len(B)
    q = 0
    if p > 0:
        q = len(B[0])

    row_width = m * p
    column_width = n * q

    # creates an (m*p)*(n*q) list for the answer matrix
    entries: MATRIX = [
        [0.0 for _ in range(row_width)] for _ in range(column_width)
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

    for i in range(row_width):
        for j in range(column_width):

            # A[k][l]:
            k = (i // m) % m
            l = (j // n) % n  # noqa: E741

            # B[r][s]
            r = i % p
            s = j % q

            val = A[k][l] * B[r][s]
            # Round values close to zero within 1e-9
            if cmath.isclose(val, 0):
                val = 0

            entries[i][j] = val

    return DefaultMatrix(entries)
