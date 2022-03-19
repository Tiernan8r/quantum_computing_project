import math, cmath
from qcp.matrices import DefaultMatrix
import qcp.gates as g
from qcp.tensor_product import tensor_product as tp
import qcp.register as reg
import random


def is_unitary (input: DefaultMatrix):
    """
    Check if matrix is Unitary (can be shifted to gates.py)
    :param DefaultMatrix: input: n x n matrix
    """
    test = input.adjoint()*input
    identity = DefaultMatrix.identity(test.num_rows)
    for i in range(input.num_rows):
        for j in range(input.num_columns):
            if cmath.isclose(test[i][j],identity[i][j]):
                continue
            else:
                return False
    return True

def optimum_qubit_size(precision: int, error: float):
    """
    Returns number of qubit required for targeted number of decimal and error rate.
    """
    return math.ceil(precision + math.log2(2+1/(2*error)))

def QFT_Gate(size: int):
    """
    Performs Quantum Fourier Transform, which change the basis 
    :param int: size: number of qubits
    :return DefaultMatrix: gate
    """

    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(size-1,-1,-1):
        gate =  QFT_Rotation_Gate(size,i)*g.multi_gate(size,[i],g.Gate.H)*gate
    for i in range(int(size/2)):
        gate = g.swap(size,[i,size-1-i])*gate
    return gate    

def Inverse_QFT_Gate(size: int):
    """
    Performs Inverse Quantum Fourier Transform 
    :param int: size: number of qubits
    :return DefaultMatrix: gate
    """
    gate = g.multi_gate(size,[],g.Gate.I)
    for i in range(int(size/2)):
        gate = g.swap(size, [i,size-i-1])*gate
    for i in range(0,size):
        gate =  g.multi_gate(size,[i],g.Gate.H)*Inverse_QFT_Rotation_Gate(size,i)*gate    
    return gate

def QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate for Quantum Fourier Transform
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    :return DefaultMatrix: gate
    """
    gate = DefaultMatrix.identity(2**size)
    for i in range (1,current_qubit+1):
        phi = 2*math.pi/2**(i+1)
        control = current_qubit-i
        gate = gate * g.control_phase(size,[control],current_qubit,phi)
    return gate

def Inverse_QFT_Rotation_Gate(size: int, current_qubit: int):
    """"
    Construct the R2...R(n-i) gate for Inverse Quantum Fourier Transform
    :param size: total number of qubits, n
    :param current_qubit: which qubit to apply the rotation gate to, i 
    """
    gate = DefaultMatrix.identity(2**size)
    for i in range(0,current_qubit):
        phi = -2*math.pi/2**(current_qubit+1-i)
        control = i
        gate = gate * g.control_phase(size,[control],current_qubit,phi)
    return gate

class Phase_Estimation:
    def __init__(self, size: int, unitary: DefaultMatrix, eigenvector: DefaultMatrix):
        """
        Implement Phase Estimation, which requires a unitary matrix and one of its eigenvector 
        as the input.
        :param int: size: precision of the phase output, i.e. no. of decimal
        :param DefaultMatrix unitary: a unitary matrix whose eigenvalue's phase is the target
        :param DefaultMatrix eigenvector: an eigenvector of the unitary matrix

        Example: 
        phase = 0.125
        unitary = DefaultMatrix([[1,0],[0,exp(1j*math.pi*phase)]])
        eigenvector = DefaultMatrix([[0],[1]])
        PE = Phase_Esimation(3,unitary,eigenvector)
        PE.run()
        print(PE.measure())
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
        """
        Control-U Gate applied to auxiliary register
        """
        totalsize = self.size+self.auxsize
        gate = g.multi_gate(totalsize,[],g.Gate.I)
        rep = 0
        for i in range(0,self.size):
            for j in range(2**rep):
                gate = g.control_U(totalsize,self.size-1-i,self.unitary)*gate
            rep += 1    
        return gate

    def third_layer(self):
        """"
        Inverse QFT Gate tensor for the first register
        """
        return tp(g.multi_gate(self.auxsize,[],g.Gate.I),Inverse_QFT_Gate(self.size))

    def construct_circuit(self):
        """
        Combines the layers
        """
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
             # print all the possiblities
             # Should be removed, implement GUI histogram instead
             print(i,round(p[i],4)) 
        return observed[0]/2**self.size, round(probability,4)

