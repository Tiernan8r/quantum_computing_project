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
from matrix import Matrix
from square_matrix import SquareMatrix


def tensor_product(A: Matrix, B: Matrix):
    # A = m * n matrix
    # B = n * p
    m = len(A)
    n = len(A[0])
    p = len(B[0])

    row_width = n * m
    column_width = n * p

    # creates an (m*n)*(n*p) list for the answer matrix

    # entries = [[None] * row_width] * column_width
    entries = make_zeros(row_width, column_width)
    # print("ENTRIES:")
    # print(entries)

    # A * B =
    # [A00 * B, A01 * B, ... A0n * B]
    # [A10 * B, A11 * B, ... A1n * B]
    # [ ...              ...        ]
    # [An0 * B, A1n * B, ... Ann * B]

    for i in range(row_width):
        for j in range(column_width):

            # A[k][l]:
            k = i // n
            l = j // n

            # B[p][q]
            p = i % n
            q = j % n

            # print(f"@({i},{j}): A=({k},{l}) / B=({p},{q})")

            entries[i][j] = A[k][l] * B[p][q]
            # print(entries)

    return SquareMatrix(entries)


def make_zeros(n, m):
    l = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(0)
        l.append(row)
    return l
