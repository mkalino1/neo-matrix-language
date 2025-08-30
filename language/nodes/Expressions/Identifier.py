from language.nodes.Node import Node

class Identifier(Node):
    def __init__(self, string, line=None, column=None):
        super().__init__(line, column)
        self.value = string

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor):
        return visitor.visit_identifier(self) 