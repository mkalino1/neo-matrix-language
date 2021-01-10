class Scalar():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'


class Bool():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'


class String():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'


class Property():
    def __init__(self, object_name, property_name):
        self.object_name = object_name
        self.property_name = property_name

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.object_name}.{self.property_name}'


class Matrix():
    def __init__(self, rows):
        self.rows = rows

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.rows}'


class Access():
    def __init__(self, identifier, first, second):
        self.identifier = identifier
        self.first = first
        self.second = second

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.first} {self.second}'


class BinaryOperator():
    def __init__(self, lvalue, op, rvalue):
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op.value}'