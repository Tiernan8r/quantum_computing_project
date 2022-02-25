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
from matrix import Matrix, MATRIX, VECTOR, SCALARS


class MyMatrix(Matrix):
    def __init__(self, state: MATRIX):
        self.state = state
        self.conjugated = False

    def dim(self):
        # Return the dimension of matrix, in (row,col) tuple
        # __len__ cannot return tuple, only integer
        assert not len(self.state) == 0, "Matrix cannot be empty!"
        if not isinstance(self.state[0], list):
            return (len(self.state), 1)
        else:
            return (len(self.state), len(self.state[0]))

    def __getitem__(self, i: int) -> VECTOR:
        # TODO after discussion
        pass

    def __setitem__(self, i: int, v: SCALARS):
        # TODO after discussion
        pass

    def get_state(self) -> MATRIX:
        # Ignored, not sure what is this intended for
        return self.state

    def set_state(self, s: MATRIX):
        # Ignored, not sure what is this intended for
        self.state = s
        return

    @classmethod
    def zeros(cls, nrow, ncol=1):
        # Create zero matrix with dimension (nrow,ncol)
        # Class method used to handle the creation of new object
        return cls([[0 for _ in range(nrow)] for _ in range(ncol)])

    def __add__(self, other: Matrix, sign=1) -> Matrix:
        # Addition between two matrices with same dimension
        assert(isinstance(other, type(self)))
        assert self.dim() == other.dim(), \
            'Cannot add matrices with different dimensions'
        nrow, ncol = self.dim()
        sum = self
        for i in range(nrow):
            for j in range(ncol):
                sum[i][j] = self.state[i][j] + sign * other.state[i][j]
        return sum

    def __sub__(self, other: Matrix):
        # Take advantage of addition method
        return self.__add__(other, -1)

    def columns(self) -> MATRIX:
        pass

    def __mul__(self, other):
        # Multiplication
        # If the other input is an integer, multiply directly
        if isinstance(other, int):
            nrow, ncol = self.dim()
            new = Matrix(
                [[self.state[i][j] * other for i in range(nrow)] for j in range(ncol)])
            return new
        # Check if the dimensions of the two matrices are compatible
        assert self.dim()[1] == other.dim()[
            0], 'Cannot add matrices with different dimensions'    
        # Product matrix is of (nrow, ncol)
        nrow = self.dim()[0]
        ncol = other.dim()[1]
        n = self.dim()[1]
        # declare empty matrix
        mul = Matrix.zeros(nrow, ncol)
        for i in range(nrow):
            for j in range(ncol):
                for k in range(n):
                    mul[i][j] += self.state[i][k] * other.state[k][j]
        return mul

# Handle right multiplication, e.g. 5*M
# Since rmul is not called if two matrices multiply,
# no need to worry about commutation
    __rmul__ = __mul__

    def __str__(self) -> str:
        pass

    def conjugate(self):
        # conjugation of matrix, the state "conjugated" is reversed
        nrow, ncol = self.dim()
        for i in range(nrow):
            for j in range(ncol):
                if isinstance(self.state[i][j], complex):
                    self.state[i][j] = self.state[i][j].conjugate()
        self.conjugated = not self.conjugated
        return self.state

    def transpose(self):
        # transpose of matrix
        nrow, ncol = self.dim()
        self.state = \
            [[self.state[j][i] for i in range(nrow)] for j in range(ncol)]
        return self

    def adjoint(self):
        # dagger operation
        self.transpose()
        self.conjugate()
        return self

    def __repr__(self):
        # print list instead of object address
        return (f"{self.state}")
