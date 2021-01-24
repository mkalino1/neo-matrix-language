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
from Errors.InterpreterExceptions import NeoRuntimeError

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

        
class Matrix(Node):
    def __init__(self, rows, line=None, column=None):
        super().__init__(line, column)
        self.rows = rows
        self.properties = {}
        self.properties['det'] = self.determinant
        self.properties['rowlen'] = self.rowlen
        self.properties['collen'] = self.collen


    def __repr__(self):
        return f'{self.__class__.__name__}: {self.rows}'


    def accept(self, visitor):
        return visitor.visit_matrix(self)


    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
            return False       
        for row1, row2 in zip(self.rows, other.rows):
            for elem1, elem2 in zip(row1, row2):
                if elem1 != elem2:
                    return False
        return True 


    def __mul__(self, other):
        # TODO:obsluzyc przypadek niematrix

        x_rows = len(self.rows)
        x_cols = len(self.rows[0])
        y_rows = len(other.rows)
        y_cols = len(other.rows[0])

        if x_cols != y_rows:
            raise NeoRuntimeError("Wrong shapes of matrixes. Cannot multiply", self.line, self.column)

        result = [[0 for _ in range(y_cols)] for _ in range(x_rows)]

        # iterate through rows of X
        for i in range(x_rows):
            # iterate through columns of Y
            for j in range(y_cols):
                # iterate through rows of Y
                for k in range(y_rows):
                    result[i][j] += self.rows[i][k] * other.rows[k][j]

        return Matrix(result, self.line, self.column)


    def __add__(self, other):
        new_rows = []
        if isinstance(other, Matrix):
            if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
                raise NeoRuntimeError("Matrixes must have the same shape", self.line, self.column)

            for row1, row2 in zip(self.rows, other.rows):
                new_row = []
                for elem1, elem2 in zip(row1, row2):
                    new_row.append(elem1 + elem2)
                new_rows.append(new_row)

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(elem + other)
                new_rows.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot add 'Matrix' and '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(new_rows, self.line, self.column)


    def __sub__(self, other):
        new_rows = []
        if isinstance(other, Matrix):
            if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
                raise NeoRuntimeError("Matrixes must have the same shape", self.line, self.column)

            for row1, row2 in zip(self.rows, other.rows):
                new_row = []
                for elem1, elem2 in zip(row1, row2):
                    new_row.append(elem1 - elem2)
                new_rows.append(new_row)

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(elem - other)
                new_rows.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot substract 'Matrix' with '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(new_rows, self.line, self.column)


    def rowlen(self):
        return len(self.rows)


    def collen(self):
        return len(self.rows[0])


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


