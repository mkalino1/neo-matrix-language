from language.nodes.Node import Node
from language.errors.InterpreterExceptions import NeoRuntimeError

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

    
    """
    Returns a pretty formatted string representation of the Matrix object.
    Handles matrices containing other matrices (nested), aligning and centering each cell's content.
    """
    def __repr__(self):
        def cell_to_lines(cell):
            if isinstance(cell, Matrix):
                cell_lines = str(cell).split('\n')
                return cell_lines
            else:
                return [str(cell)]
        
        num_cols = len(self.rows[0])
        
        # For each cell, get its string lines
        cell_lines_matrix = []
        for row in self.rows:
            cell_lines_row = []
            for cell in row:
                cell_lines_row.append(cell_to_lines(cell))
            cell_lines_matrix.append(cell_lines_row)
        
        # For each column, determine the max width (across all lines of all cells in that column)
        col_widths = []
        for col in range(num_cols):
            max_width = 0
            for row in cell_lines_matrix:
                cell_lines = row[col]
                for line in cell_lines:
                    max_width = max(max_width, len(line))
            col_widths.append(max_width)
        
        # For each row, determine the max height (number of lines) for each cell in that row
        row_heights = []
        for row in cell_lines_matrix:
            max_height = max(len(cell_lines) for cell_lines in row)
            row_heights.append(max_height)
        
        # Build the string representation row by row, line by line
        repr_rows = []
        for row_idx, row in enumerate(cell_lines_matrix):
            max_height = row_heights[row_idx]
            # For each line in the row (up to max_height)
            for line_idx in range(max_height):
                cells = []
                for col_idx, cell_lines in enumerate(row):
                    width = col_widths[col_idx]
                    # If this cell has enough lines, use it, else use empty string
                    if line_idx < len(cell_lines):
                        cell_line = cell_lines[line_idx]
                    else:
                        cell_line = ""
                    # Center the value in the cell (numbers and matrices)
                    cells.append(cell_line.center(width))
                repr_rows.append('| ' + '   '.join(cells) + ' |')
        
        border = '-' * (sum(col_widths) + 3 * num_cols + 1)
        return '\n'.join([border] + repr_rows + [border])

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
            for i in range(x_rows):
                for j in range(y_cols):
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

    def __pow__(self, other):
        if not isinstance(other, (int, float)) or other < 0:
            raise NeoRuntimeError("Matrix power can only be calculated for non-negative numbers", self.line, self.column)

        n = len(self.rows)
        if n != len(self.rows[0]):
            raise NeoRuntimeError("Only square matrices can be raised to a power", self.line, self.column)
        if other == 0:
            # Identity matrix for 0 power
            return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)], self.line, self.column)

        result = Matrix([row[:] for row in self.rows], self.line, self.column)
        for _ in range(int(other) - 1):
            result = result * self
        return result

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
        if self.properties["rowlen"]() != self.properties["collen"]():
            raise NeoRuntimeError("Matrix must be square to calculate determinant", self.line, self.column)

        if not all(isinstance(elem, (int, float)) for row in self.rows for elem in row):
            raise NeoRuntimeError("Matrix determinant can only be calculated for matrices of scalars", self.line, self.column)
        
        def getMatrixMinor(m,i,j):
            return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

        def getMatrixDeternminant(m):
            if len(m) == 2:
                return m[0][0]*m[1][1]-m[0][1]*m[1][0]
            determinant = 0
            for c in range(len(m)):
                determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
            return determinant
        return(getMatrixDeternminant(self.rows)) 