from language.nodes.Node import Node

class WhileLoop(Node):
    def __init__(self, condition, block, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block}'

    def accept(self, visitor):
        return visitor.visit_while_loop(self) 