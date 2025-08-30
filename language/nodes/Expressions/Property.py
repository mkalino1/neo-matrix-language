from language.nodes.Node import Node

class Property(Node):
    def __init__(self, object_name, property_name, line=None, column=None):
        super().__init__(line, column)
        self.object_name = object_name
        self.property_name = property_name

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.object_name}.{self.property_name}'

    def accept(self, visitor):
        return visitor.visit_property(self) 