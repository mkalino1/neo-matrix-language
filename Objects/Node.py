class Node():
    def __init__(self, line=None, column=None):
        self.line = line
        self.column = column

    def accept(self, visitor):
        raise NotImplementedError(f'{self.__class__.__name__} not implemented')
