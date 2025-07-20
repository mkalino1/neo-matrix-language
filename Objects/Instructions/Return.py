from Objects.Node import Node

class Return(Node):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.expression}'

    def accept(self, visitor):
        return visitor.visit_return(self) 