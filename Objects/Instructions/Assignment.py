from Objects.Node import Node

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