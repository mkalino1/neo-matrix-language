from language.nodes.Node import Node

class UnaryOperator(Node):
    def __init__(self, op, rvalue, line=None, column=None):
        super().__init__(line, column)
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_unary_operator(self) 