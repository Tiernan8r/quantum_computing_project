from Matrix import Matrix
import consts
from tensor_product import tensor_product


class QRegister:
    def __init__(self, state):
        """
        Params
        ------
        State: List
            Binary representation of the state of the QRegister
        """

        self.initState = state
        self.stateVec = self.makeStateVec(state)

    def makeStateVec(self, state):
        stateVec = Matrix()

        if state[0] == 0:
            stateVec.set_state(consts.ZERO_VECTOR.getState())
        elif state[0] == 1:
            stateVec.set_state(consts.ONE_VECTOR.getState())

        for i in range(1, len(state)):
            if state[i] == 0:
                tensor_product(stateVec, consts.ZERO_VECTOR)

            elif state[i] == 1:

                tensor_product(stateVec, consts.ONE_VECTOR)

        assert (len(stateVec.state) == (2 ** len(self.initState)))
        return stateVec

    def setStateVec(self, stateVec):
        assert (len(stateVec) == (2 ** len(self.initState)))
        self.stateVec = stateVec
        return

    def getStateVec(self):
        s = self.stateVec
        return s
