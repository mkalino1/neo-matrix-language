"""
Klasy obiektów reprezentujacych expression

    Expression     = Equality ( ( "and" | "or" ) Equality )*;
    Equality       = Comparison ( "==" Comparison )* ;
    Comparison     = Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
    Term           = Factor ( ( "-" | "+" ) Factor )* ;
    Factor         = Unary ( ( "/" | "*" ) Unary )* ;
    Unary          = ( "not" | "-" ) Unary | Primary ;
    Primary        = Literal | "(" Expression ")" ; 
    Literal        = Bool | String | Scalar | Matrix | FunctionCall | ObjectProperty | MatrixAccess | Identifier; 

"""

from .Node import Node

class BinaryOperator(Node):
    def __init__(self, lvalue, op, rvalue):
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.lvalue} {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_binary_operator(self)


class UnaryOperator(Node):
    def __init__(self, op, rvalue):
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_unary_operator(self)


class Scalar(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Bool(Node):
    def __init__(self, value):
        self.value = value == "true"

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Property(Node):
    def __init__(self, object_name, property_name):
        self.object_name = object_name
        self.property_name = property_name

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.object_name}.{self.property_name}'


class Matrix(Node):
    def __init__(self, rows):
        self.rows = rows

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.rows}'


class Access(Node):
    def __init__(self, identifier, first, second):
        self.identifier = identifier
        self.first = first
        self.second = second

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.first} {self.second}'


class Identifier(Node):
    def __init__(self, string):
        self.value = string

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor):
        return visitor.visit_identifier(self)
