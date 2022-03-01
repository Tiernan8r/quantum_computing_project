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
from matrices import DefaultMatrix, Matrix, SparseMatrix
import cmath


def tensor_product(A: Matrix, B: Matrix) -> Matrix:
    """
    Compute the tensor product between two matrices, and return the
    resultant Matrix
    :param A Matrix: An m*n matrix
    :param B Matrix: Second p*q matrix to tensor product with
    :returns: An (m*p)*(n*q) matrix of the tensor product.
    """

    if isinstance(A, SparseMatrix) and isinstance(B, SparseMatrix):
        return _tensor_product_sparse(A, B)

    m = A.num_rows
    n = A.num_columns
    p = B.num_rows
    q = B.num_columns

    row_width = m * p
    column_width = n * q

    # creates an (m*p)*(n*q) list for the answer matrix
    entries = [
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


def _tensor_product_sparse(A: SparseMatrix, B: SparseMatrix) -> Matrix:
    """
    Compute the tensor product between two SparseMatrices, and return the
    resultant Matrix
    :param A SparseMatrix: An m*n matrix
    :param B SparseMatrix: Second p*q matrix to tensor product with
    :returns: An (m*p)*(n*q) matrix of the tensor product.
    """

    m = A.num_rows
    n = A.num_columns
    p = B.num_rows
    q = B.num_columns

    num_columns = n * q
    num_rows = m * p

    # creates a dictionary to store the (m*p)*(n*q) entries
    entries = {
        i: {} for i in range(num_rows)
    }

    for k, row_a in A._entries.items():
        for l, v_a in row_a.items():  # noqa: E741

            for r, row_b in B._entries.items():
                for s, v_b in row_b.items():

                    i = k * p + r
                    j = l * q + s

                    entries[i][j] = v_a * v_b

    return SparseMatrix(entries, w=num_columns, h=num_rows)
