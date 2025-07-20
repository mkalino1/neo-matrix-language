from Objects.Node import Node

class Function(Node):
    def __init__(self, name, parameter_list, block, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.parameter_list = parameter_list
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} {self.parameter_list} {self.block}'

    def accept(self, visitor):
        return visitor.visit_function(self) 