from language.nodes.Node import Node

class FunctionCall(Node):
    def __init__(self, function_name_or_body, arguments_list, line=None, column=None):
        super().__init__(line, column)
        # function_name_or_body can be either an Identifier (for named functions) or a Function (for IIFE)
        self.function_name_or_body = function_name_or_body
        self.arguments = arguments_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.function_name_or_body} {self.arguments}'

    def accept(self, visitor):
        return visitor.visit_function_call(self) 