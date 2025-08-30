from language.nodes.Node import Node

class Declaration(Node):
    def __init__(self, identifier, expression, mutable=False, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.expression = expression
        self.mutable = mutable

    def __repr__(self):
        mut_str = 'mutable' if self.mutable else 'immutable'
        return f'{self.__class__.__name__}: {mut_str} {self.identifier} = {self.expression}'

    def accept(self, visitor):
        return visitor.visit_declaration(self) 