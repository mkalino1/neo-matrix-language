from language.nodes.Node import Node

class BinaryOperator(Node):
    def __init__(self, lvalue, op, rvalue, line=None, column=None):
        super().__init__(line, column)
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.lvalue} {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_binary_operator(self) 