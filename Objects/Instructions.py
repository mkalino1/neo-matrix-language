"""
Klasy obiektów reprezentujacych instukcje

    Instruction = IfStatement | Loop | Assignment | FunctionCall ";" | BlockInstruction | ReturnInstruction;
    
"""

from .Node import Node

class Block(Node):
    def __init__(self, instructions, line=None, column=None):
        super().__init__(line, column)
        self.instructions = instructions
        self.passed_variables = {}

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.instructions}'

    def accept(self, visitor):
        return visitor.visit_block(self)


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


class Return(Node):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.expression}'

    def accept(self, visitor):
        return visitor.visit_return(self)


class WhileLoop(Node):
    def __init__(self, condition, block, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block}'

    def accept(self, visitor):
        return visitor.visit_while_loop(self)


class FunctionCall(Node):
    def __init__(self, function_name, arguments_list, line=None, column=None):
        super().__init__(line, column)
        self.function_name = function_name
        self.arguments = arguments_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.function_name} {self.arguments}'

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Assignment(Node):
    def __init__(self, left_identifier, first_index, second_index, right_expression, line=None, column=None):
        super().__init__(line, column)
        self.identifier = left_identifier
        self.first_index = first_index
        self.second_index = second_index
        self.expression = right_expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.identifier} {self.expression}'

    def accept(self, visitor):
        return visitor.visit_assignment(self)