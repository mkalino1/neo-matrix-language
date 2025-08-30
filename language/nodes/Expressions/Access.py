from language.nodes.Node import Node

class Access(Node):
    def __init__(self, identifier, first, second, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.first = first
        self.second = second

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.first} {self.second}'

    def accept(self, visitor):
        return visitor.visit_access(self) 