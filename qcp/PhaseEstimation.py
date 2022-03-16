from distutils.command.build_scripts import first_line_re
from inspect import currentframe
from os import curdir
from signal import default_int_handler
import sys
sys.path.insert(0,'C:\\Users\\Ng Yi Sheng\\Desktop\\QCP\\quantum_computing_project')
import math
from qcp.matrices import DefaultMatrix, sparse_matrix
import qcp.gates as g
import cmath
from qcp.tensor_product import _tensor_product_sparse as tps
import qcp.register as reg
import random

def QFT_Gate(size: int):
    """
    Performs Quantum Fourier Transform 
    :param state: input vector
    :return vector
    """

    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(size):
        gate =  QFT_Rotation_Gate(size,i)*g.multi_gate(size,[i],g.Gate.H)*gate
    for i in range(int(size/2)):
        gate = g.swap(size,[i,2**size-i-1])*gate
        print(gate)
    return gate    

def Inverse_QFT_Gate(size: int):
    """
    Performs Quantum Fourier Transform 
    :param state: input vector
    :return vector
    """

    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(int(size/2)):
        gate = g.swap(size, [i,2**size-i-1])*gate
    for i in range(size-1,-1,-1):
        gate =  g.multi_gate(size,[i],g.Gate.H)*Inverse_QFT_Rotation_Gate(size,i)*gate    
    return gate

def is_unitary (input: DefaultMatrix):
    test = input.adjoint()*input
    identity = sparse_matrix.SparseMatrix.identity(test.num_rows)
    for i in range(input.num_rows):
        for j in range(input.num_columns):
            if cmath.isclose(test[i][j],identity[i][j]):
                continue
            else:
                return False
    return True

def QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    """
    gate = sparse_matrix.SparseMatrix.identity(2**size)
    for i in range (1,size-current_qubit):
        phi = 2*math.pi/2**(i+1)
        target = current_qubit+i
        gate = gate * g.control_phase(size,[target],current_qubit,phi)
    return gate

def Inverse_QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    """
    gate = sparse_matrix.SparseMatrix.identity(2**size)
    iteration = 0
    for i in range (size-current_qubit,1,-1):
        phi = -2*math.pi/2**(i)
        target = size-1-iteration
        iteration += 1
        gate = gate * g.control_phase(size,[target],current_qubit,phi)
    return gate

class PhaseEstimation:
    def __init__(self, size: int, unitary: DefaultMatrix, eigenvector: DefaultMatrix):
        """
        Implement Phase Estimation
        :param size: precision of the phase output, i.e. no. of decimal
        """
        assert is_unitary(unitary), "Matrix must be unitary!"

        self.size = size
        self.unitary = unitary
        self.auxiliary = eigenvector
        self.auxsize = int(math.log2(eigenvector.num_rows))
        self.state = self.initial_state()

        self.circuit = self.construct_circuit()

    def initial_state(self):
        """
        Creates a state vector corresponding to |0..0>
        :return: returns state vector
        """
        entries = [[0] for _ in range(2 ** self.size)]
        entries[0][0] = 1
        return tps(DefaultMatrix(entries),self.auxiliary)

    def first_layer(self):
        """
        Tensor Hadamard (first register) with Identity (auxiliary)
        """
        return tps(g.multi_gate(self.size,[i for i in range(self.size)],g.Gate.H),g.multi_gate(self.auxsize,[],g.Gate.I))

    def second_layer(self):
        totalsize = self.size+self.auxsize
        gate = g.multi_gate(totalsize,[],g.Gate.I)
        rep = 0
        for i in range(self.size-1,-1,-1):
            for j in range(2**rep):
                gate = g.control_U(totalsize,i,self.unitary)*gate
            rep += 1    
        return gate

    def third_layer(self):
        return tps(Inverse_QFT_Gate(self.size),g.multi_gate(self.auxsize,[],g.Gate.I))

    def construct_circuit(self):
        cu = DefaultMatrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1j]])
        swp = DefaultMatrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
        mat=tps(g.multi_gate(1,[0],g.Gate.H),g.multi_gate(1,[],g.Gate.I))*cu.conjugate()*tps(g.multi_gate(1,[],g.Gate.I),g.multi_gate(1,[0],g.Gate.H))*swp
        return tps(mat,g.multi_gate(1,[],g.Gate.I))*self.second_layer()*self.first_layer()

    def run(self):
        """
        Multiplies our Phase Esimation's circuit with the initial state
        :return: Final state
        """
        self.state = self.circuit * self.state
        return self.state
    
    # def measure(self):
    #     """
    #     'measures' self.state by selecting a state weighted by its
    #     (amplitude ** 2)
    #     :return: the state observed and the probability of measuring
    #             said state
    #     """

    #     for i in range(2**self.size):
    #         entries = [[0] for _ in range(2**self.size)]
    #         phi = str(bin(i))
    #         for j in range(len(phi)-1,1,-1):
    #             if phi[j] == '1':
    #                 entries[len(phi)-j-1] = [1]
    #         trial= tps(DefaultMatrix(entries),self.auxiliary)
    #         dot = trial.transpose()*(self.state)
    #         dot = complex(str(dot[0][0]))
    #         if math.isclose(dot.real,1) and math.isclose(dot.imag,0):
    #             return i/2**self.size       
    def measure(self):
        """
        'measures' self.state by selecting a state weighted by its
        (amplitude ** 2)
        :return: the state observed and the probability of measuring
                said state
        """
        p = reg.measure(self.state)
        # list of weighted probabilities with the index representing the state

        # # observed = random.choices([i for i in range(len(p))], p, k=1)
        # probability = p[observed[0]]
        # return observed[0], probability 

unitary = DefaultMatrix([[1,0],[0,cmath.exp(1j*cmath.pi*2/3)]])
eigenvec = DefaultMatrix([[0],[1]])
PE = PhaseEstimation(2,unitary,eigenvec)
PE.run()
print(PE.measure())

# vec = DefaultMatrix([[0.5],[0.5j],[-0.5],[-0.5j]])
# v = DefaultMatrix([[0],[1],[0],[0]])
# swp = DefaultMatrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
# cu = DefaultMatrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1j]])
# QFT =swp*tps(g.multi_gate(1,[],g.Gate.I),g.multi_gate(1,[0],g.Gate.H))*cu*tps(g.multi_gate(1,[0],g.Gate.H),g.multi_gate(1,[],g.Gate.I))
# mat=tps(g.multi_gate(1,[0],g.Gate.H),g.multi_gate(1,[],g.Gate.I))*cu.conjugate()*tps(g.multi_gate(1,[],g.Gate.I),g.multi_gate(1,[0],g.Gate.H))*swp
# result = Inverse_QFT_Gate(2)*vec
# # QFT = tps(g.multi_gate(1,[],g.Gate.I),g.multi_gate(1,[0],g.Gate.H))
# # FT = g.multi_gate(2,[0],g.Gate.H)
# print(mat*QFT)
# # print('\n')
# # print(FT)
# # print (mat*vec)
# # print('\n')
# # print(result)

print(g.control_phase(2,[0],1,math.pi/2))