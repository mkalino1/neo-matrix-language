class Program():
    def __init__(self, objects):
        self.toplevel_objects = objects

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.toplevel_objects}'


class Identifier():
    def __init__(self, string):
        self.name = string

    def __repr__(self):
        return f'{self.name}'


class Function():
    def __init__(self, id, parameter_list, block):
        self.id = id
        self.parameter_list = parameter_list
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.name} {self.parameter_list} {self.block}'


class Block():
    def __init__(self, instructions):
        self.instructions = instructions

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.instructions}'


class IfStatement():
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block} {self.else_block}'


class Return():
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.expression}'


class WhileLoop():
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.condition} {self.block}'


class Assignment():
    def __init__(self, left_identifier, right_expression):
        self.left_identifier = left_identifier
        self.right_expression = right_expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.left_identifier} {self.right_expression}'


class FunctionCall():
    def __init__(self, function_name, arguments_list):
        self.function_name = function_name
        self.arguments = arguments_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.function_name} {self.arguments}'



