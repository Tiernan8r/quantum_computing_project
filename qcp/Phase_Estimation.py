from ast import In
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
from qcp.tensor_product import tensor_product as tp
import qcp.register as reg
import random


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

def QFT_Gate(size: int):
    """
    Performs Quantum Fourier Transform 
    :param state: input vector
    :return vector
    """

    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(size-1,-1,-1):
        gate =  QFT_Rotation_Gate(size,i)*g.multi_gate(size,[i],g.Gate.H)*gate
    for i in range(int(size/2)):
        gate = g.swap(size,[i,size-1-i])*gate
    return gate    

def Inverse_QFT_Gate(size: int):
    """
    Performs Quantum Fourier Transform 
    :param state: input vector
    :return vector
    """
    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(int(size/2)):
        gate = g.swap(size, [i,size-i-1])*gate
    for i in range(0,size):
        gate =  g.multi_gate(size,[i],g.Gate.H)*Inverse_QFT_Rotation_Gate(size,i)*gate    
    return gate

def QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    """
    gate = sparse_matrix.SparseMatrix.identity(2**size)
    for i in range (1,current_qubit+1):
        phi = 2*math.pi/2**(i+1)
        control = current_qubit-i
        gate = gate * g.control_phase(size,[control],current_qubit,phi)
    return gate

def Inverse_QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    """
    gate = sparse_matrix.SparseMatrix.identity(2**size)
    for i in range(0,current_qubit):
        phi = -2*math.pi/2**(current_qubit+1-i)
        print(phi)
        control = i
        gate = gate * g.control_phase(size,[control],current_qubit,phi)
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
        return tp(self.auxiliary,DefaultMatrix(entries))

    def first_layer(self):
        """
        Tensor Hadamard (first register) with Identity (auxiliary)
        """
        return tp(g.multi_gate(self.auxsize,[],g.Gate.I),g.multi_gate(self.size,[i for i in range(self.size)],g.Gate.H))

    def second_layer(self):
        totalsize = self.size+self.auxsize
        gate = g.multi_gate(totalsize,[],g.Gate.I)
        rep = 0
        for i in range(0,self.size):
            for j in range(2**rep):
                gate = g.control_U(totalsize,self.size-1-i,self.unitary)*gate
            rep += 1    
        return gate

    def third_layer(self):
        return tp(g.multi_gate(self.auxsize,[],g.Gate.I),Inverse_QFT_Gate(self.size))

    def construct_circuit(self):
        return self.third_layer()*self.second_layer()*self.first_layer()

    def run(self):
        """
        Multiplies our Phase Esimation's circuit with the initial state
        :return: Final state
        """
        self.state = self.circuit * self.state
        return self.state
    
    def measure(self):
        """
        'measures' self.state by selecting a state weighted by its
        (amplitude ** 2)
        :return: the state observed and the probability of measuring
                said state
        """
        result = DefaultMatrix([[0] for _ in range(2**self.size)])
        for i in range(2**self.size):
            entries = [[0] for _ in range(2**self.size)]
            entries[i] = [1]
            trial= tp(self.auxiliary,DefaultMatrix(entries))
            result[i] = (trial.transpose()*self.state)[0]
        p = reg.measure(result)
        observed = random.choices([i for i in range(len(p))], p, k=1)
        probability = p[observed[0]]
        for i in range(2**self.size):
             print(i,p[i])
        return observed[0]/2**self.size, probability 
        
vec=DefaultMatrix([[0] for _ in range(4)])
vec[0] = [1]
print(QFT_Gate(2)*vec)
phase = 0.25
unitary = DefaultMatrix([[1,0],[0,cmath.exp(2j*cmath.pi*phase)]])
eigenvec = DefaultMatrix([[0],[1]])
PE = PhaseEstimation(2,unitary,eigenvec)
PE.run()
print(PE.measure())

# vec=DefaultMatrix([[0] for _ in range(8)])
# vec[6] = [1]
# print( Inverse_QFT_Gate(3)*vec)

# print(g.control_phase(3,[0],1,math.pi))
# print('\n')
# print(g.control_phase(3,[2],1,math.pi))