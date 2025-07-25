from Objects.Node import Node

class Declaration(Node):
    def __init__(self, identifier, expression, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.identifier} = {self.expression}'

    def accept(self, visitor):
        return visitor.visit_declaration(self) 