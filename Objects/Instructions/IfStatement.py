from Objects.Node import Node

class IfStatement(Node):
    def __init__(self, condition, block, else_block, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block} {self.else_block}'

    def accept(self, visitor):
        return visitor.visit_if_statement(self) 