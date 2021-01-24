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
    def __init__(self, lvalue, op, rvalue, line=None, column=None):
        super().__init__(line, column)
        self.lvalue = lvalue
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.lvalue} {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_binary_operator(self)


class UnaryOperator(Node):
    def __init__(self, op, rvalue, line=None, column=None):
        super().__init__(line, column)
        self.op = op
        self.rvalue = rvalue

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.op} < {self.rvalue} >'

    def accept(self, visitor):
        return visitor.visit_unary_operator(self)


class Scalar(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Bool(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value == "true"

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class String(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Property(Node):
    def __init__(self, object_name, property_name, line=None, column=None):
        super().__init__(line, column)
        self.object_name = object_name
        self.property_name = property_name

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.object_name}.{self.property_name}'

    def accept(self, visitor):
        return visitor.visit_property(self)


class Matrix(Node):
    def __init__(self, rows, line=None, column=None):
        super().__init__(line, column)
        self.rows = rows
        self.properties = {}
        self.properties['det'] = self.determinant

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.rows}'

    def accept(self, visitor):
        return visitor.visit_matrix(self)

    def determinant(self):
        # Section 1: Establish n parameter and copy A
        A = self.rows
        n = len(A)
        AM = [x[:] for x in A]
    
        # Section 2: Row ops on A to get in upper triangle form
        for fd in range(n): # A) fd stands for focus diagonal
            for i in range(fd+1,n): # B) only use rows below fd row
                if AM[fd][fd] == 0: # C) if diagonal is zero ...
                    AM[fd][fd] == 1.0e-18 # change to ~zero
                # D) cr stands for "current row"
                crScaler = AM[i][fd] / AM[fd][fd] 
                # E) cr - crScaler * fdRow, one element at a time
                for j in range(n): 
                    AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
        
        # Section 3: Once AM is in upper triangle form ...
        product = 1.0
        for i in range(n):
            # ... product of diagonals is determinant
            product *= AM[i][i] 
    
        return product


class Access(Node):
    def __init__(self, identifier, first, second, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.first = first
        self.second = second

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.first} {self.second}'

    def accept(self, visitor):
        return visitor.visit_access(self)


class Identifier(Node):
    def __init__(self, string, line=None, column=None):
        super().__init__(line, column)
        self.value = string

    def __repr__(self):
        return f'{self.value}'

    def accept(self, visitor):
        return visitor.visit_identifier(self)
