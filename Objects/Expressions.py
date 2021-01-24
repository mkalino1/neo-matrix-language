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
        self.value = value == "True"

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
        self.properties['transposed'] = self.transposed
        self.properties['copy'] = self.copy


    def __repr__(self):
        return '\n'.join([repr(row) for row in self.rows])


    def accept(self, visitor):
        return visitor.visit_matrix(self)


    def __bool__(self):
        return not all(all(num == 0 for num in row) for row in self.rows)


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


    def __neg__(self):
        result = []
        for row in self.rows:
            new_row = []
            for elem in row:
                new_row.append(-elem)
            result.append(new_row)
        return Matrix(result, self.line, self.column)


    def __mul__(self, other):
        result = []

        if isinstance(other, Matrix):
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

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(elem * other)
                result.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot multiply 'Matrix' and '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(result, self.line, self.column)

    
    def __rmul__(self, other):
        return self.__mul__(other)


    def __add__(self, other):
        result = []
        if isinstance(other, Matrix):
            if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
                raise NeoRuntimeError("Matrixes must have the same shape", self.line, self.column)

            for row1, row2 in zip(self.rows, other.rows):
                new_row = []
                for elem1, elem2 in zip(row1, row2):
                    new_row.append(elem1 + elem2)
                result.append(new_row)

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(elem + other)
                result.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot add 'Matrix' and '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(result, self.line, self.column)


    def __radd__(self, other):
        return self.__add__(other)


    def __sub__(self, other):
        result = []
        if isinstance(other, Matrix):
            if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
                raise NeoRuntimeError("Matrixes must have the same shape", self.line, self.column)

            for row1, row2 in zip(self.rows, other.rows):
                new_row = []
                for elem1, elem2 in zip(row1, row2):
                    new_row.append(elem1 - elem2)
                result.append(new_row)

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(elem - other)
                result.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot substract 'Matrix' with '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(result, self.line, self.column)


    def __rsub__(self, other):
        result = []
        if isinstance(other, Matrix):
            if self.properties["rowlen"]() != other.properties["rowlen"]() or self.properties["collen"]() != other.properties["collen"]():
                raise NeoRuntimeError("Matrixes must have the same shape", self.line, self.column)

            for row1, row2 in zip(self.rows, other.rows):
                new_row = []
                for elem1, elem2 in zip(row1, row2):
                    new_row.append(elem2 - elem1)
                result.append(new_row)

        elif isinstance(other, float):
            for row in self.rows:
                new_row = []
                for elem in row:
                    new_row.append(other - elem)
                result.append(new_row)
        else:
            raise NeoRuntimeError(f"You cannot substract 'Matrix' with '{other.__class__.__name__}'", self.line, self.column)

        return Matrix(result, self.line, self.column)


    def rowlen(self):
        return len(self.rows)


    def collen(self):
        return len(self.rows[0])

    def copy(self):
        return Matrix([row[:] for row in self.rows], self.line, self.column)


    def transposed(self):
        result = [[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]
        return Matrix(result, self.line, self.column)


    def determinant(self):
        def getMatrixMinor(m,i,j):
            return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

        def getMatrixDeternminant(m):
            #base case for 2x2 matrix
            if len(m) == 2:
                return m[0][0]*m[1][1]-m[0][1]*m[1][0]

            determinant = 0
            for c in range(len(m)):
                determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
            return determinant

        return(getMatrixDeternminant(self.rows))


