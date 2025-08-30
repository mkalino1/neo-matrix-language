from language.nodes.Node import Node

class FunctionCall(Node):
    def __init__(self, function_name, arguments_list, line=None, column=None):
        super().__init__(line, column)
        self.function_name = function_name
        self.arguments = arguments_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.function_name} {self.arguments}'

    def accept(self, visitor):
        return visitor.visit_function_call(self) 