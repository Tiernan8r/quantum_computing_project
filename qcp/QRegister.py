from StateVector import StateVector

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
        stateVec = state
        #TODO: convert states into state vector
        assert (len(stateVec) == (2 ** len(self.initState)))
        return stateVec

    def setStateVec(self, stateVec):
        assert (len(stateVec) == (2 ** len(self.initState)))
        self.stateVec = stateVec
        return

    def getStateVec(self):
        s = self.stateVec
        return s

    # Manipulative Functions
    def addState(self, arg):
        return 4

    def subtractState(self):
        return 4
