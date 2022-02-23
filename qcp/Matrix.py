class Matrix:

    def __init__(self, state=None):
        self.state = state

        if state is None:
            self.state = [[1], [0]]

        self.conjugated = False

    def set_state(self, s):
        self.state = s
        return

    def get_state(self):
        s = self.state
        return s

    def __add__(self, other):
        assert(isinstance(other, type(self)))

        return

    def __sub__(self, other):
        assert (isinstance(other, type(self)))

        return

    def conjugate(self):
        return

    def __mul__(self, other):

        if isinstance(other, int):

            return
        elif isinstance(other, Matrix):

            return
