
class StateVector:
    ZERO_VECTOR = [1, 0]
    ONE_VECTOR = [0, 1]

    def __init__(self, state=None):
        if state is None:
            state = [0]

        self.conjugated = False
        self.state = state

    def __add__(self, other):
        return

    def __sub__(self, other):
        return

    def tensProduct(self, other):
        return

    def conjugate(self):
        return

    def __mul__(self, other):
        if isinstance(other, int):
            return
        elif isinstance(other, StateVector):
            return