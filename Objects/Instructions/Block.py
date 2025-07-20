from Objects.Node import Node

class Block(Node):
    def __init__(self, instructions, is_function_body = False, line=None, column=None):
        super().__init__(line, column)
        self.instructions = instructions
        self.passed_variables = {}
        self.is_function_body = is_function_body

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.instructions}'

    def accept(self, visitor):
        return visitor.visit_block(self) 