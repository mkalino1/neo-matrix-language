"""
Klasy obiektów reprezentujacych instukcje

    Instruction = IfStatement | Loop | Assignment | FunctionCall ";" | BlockInstruction | ReturnInstruction;
    
"""

from .Node import Node

class Block(Node):
    def __init__(self, instructions):
        self.instructions = instructions
        self.local_variables = {}

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.instructions}'

    def accept(self, visitor):
        return visitor.visit_block(self)


class IfStatement(Node):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block} {self.else_block}'


class Return(Node):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.expression}'

    def accept(self, visitor):
        return visitor.visit_return(self)


class WhileLoop(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block}'


class FunctionCall(Node):
    def __init__(self, function_name, arguments_list):
        self.function_name = function_name
        self.arguments = arguments_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.function_name} {self.arguments}'

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Assignment(Node):
    def __init__(self, left_identifier, right_expression):
        self.identifier = left_identifier
        self.expression = right_expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.identifier} {self.expression}'

    def accept(self, visitor):
        return visitor.visit_assignment(self)