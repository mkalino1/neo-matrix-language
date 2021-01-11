"""
Klasy obiektów najwyższych w hierarchii

    Program = { FunctionDefinition | Instruction } ;

"""

class Program():
    def __init__(self, objects):
        self.toplevel_objects = objects

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.toplevel_objects}'


class Function():
    def __init__(self, id, parameter_list, block):
        self.id = id
        self.parameter_list = parameter_list
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.name} {self.parameter_list} {self.block}'


