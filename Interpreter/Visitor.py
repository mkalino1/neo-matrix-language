from Objects.Instructions import Assignment, Block, FunctionCall, IfStatement, Return, WhileLoop
from Objects.ToplevelObjects import Function
from Objects.Expressions import Access, BinaryOperator, Identifier, Matrix, Property, UnaryOperator
from Objects.OperatorType import OperatorType
from Errors.InterpreterExceptions import NeoRuntimeError
from .Built_ins import builtin_functions


class Interpreter():
    def __init__(self, parsed_program):
        self.parsed_objects = parsed_program.toplevel_objects
        self.visitor = Visitor()

    def run(self):
        for top_level_object in self.parsed_objects:
            try:
                top_level_object.accept(self.visitor)
            except NeoRuntimeError as e:
                print(e)
                return
  

class Visitor:
    def __init__(self):
        self.variables = [{}]
        self.functions = {}


    def visit_function(self, function:Function):
        if function.name.value in builtin_functions:
            raise NeoRuntimeError(f"Function name '{function.name.value}' is reserved", function.name.line, function.name.column)

        self.functions[function.name.value] = function


    def visit_function_call(self, function_call:FunctionCall):
        line = function_call.function_name.line
        column = function_call.function_name.column

        if function_call.function_name.value in builtin_functions:
            builtin_function = builtin_functions[function_call.function_name.value]
            return builtin_function(line, column, *[arg.accept(self) for arg in function_call.arguments])

        if not function_call.function_name.value in self.functions:
            raise NeoRuntimeError(f"Function '{ function_call.function_name.value}' doesn't exist", line, column) 

        function:Function = self.functions[function_call.function_name.value]

        if len(function.parameter_list) != len(function_call.arguments):
            raise NeoRuntimeError("Incorrect number of arguments", line, column)

        for param, arg in zip(function.parameter_list, function_call.arguments):
            function.block.passed_variables[param.value] = arg.accept(self)

        return function.block.accept(self)


    def visit_block(self, block:Block):
        self.variables.append({})

        # jeśli blok ten jest ciałem funkcji to trzeba dołączyć przekazane jako argumenty zmienne
        self.variables[-1].update(block.passed_variables)

        return_value = None
        for instruction in block.instructions:
            if return_value := instruction.accept(self):
                break

        self.variables.pop()
        return return_value


    def visit_if_statement(self, if_statement:IfStatement):
        condition = if_statement.condition.accept(self)

        if condition:
            return if_statement.block.accept(self)
        elif if_statement.else_block:
            return if_statement.else_block.accept(self)


    def visit_while_loop(self, while_loop:WhileLoop):
        condition = while_loop.condition.accept(self)

        while condition:
            while_loop.block.accept(self)
            condition = while_loop.condition.accept(self)


    def visit_return(self, return_instruction:Return):
        if return_instruction.expression is None:
            return None
        return return_instruction.expression.accept(self)


    def visit_assignment(self, assignment:Assignment):
        expression_value = assignment.expression.accept(self)

        if not assignment.first_index:
            for scope in self.variables[::-1]:
                if assignment.identifier.value in scope:
                    scope[assignment.identifier.value] = expression_value
                    return
            self.variables[-1][assignment.identifier.value] = expression_value

        else:
            if not (assignment.first_index.value.is_integer() and assignment.second_index.value.is_integer()):
                raise NeoRuntimeError("Indieces of matrix must be whole numbers", assignment.line, assignment.column)
            for scope in self.variables[::-1]:
                if assignment.identifier.value in scope:
                    matrix:Matrix = scope[assignment.identifier.value]
                    if not isinstance(matrix, Matrix):
                        raise NeoRuntimeError("You can't use access in non-matrix", assignment.line, assignment.column)
                    matrix.rows[int(assignment.first_index.value)][int(assignment.second_index.value)] = expression_value
                    return
            raise NeoRuntimeError("You can't use access in non-existing matrix", assignment.line, assignment.column)     


    def visit_identifier(self, identifier:Identifier):
        for scope in self.variables[::-1]:
            if identifier.value in scope:
                # print(f'Variable found: {scope[identifier.value]}')
                return scope[identifier.value]
        
        raise NeoRuntimeError(f"Variable '{identifier.value}' doesn't exist", identifier.line, identifier.column) 


    def visit_matrix(self, matrix:Matrix):
        values = []
        for row in matrix.rows:
            values_row = []
            for cell in row:
                value = cell.accept(self)
                if not isinstance(value, float):
                    raise NeoRuntimeError("Matrix can contain only scalars", matrix.line, matrix.column)
                values_row.append(value)
            values.append(values_row)

        matrix.rows = values
        return matrix


    def visit_access(self, access:Access):
        matrix = access.identifier.accept(self)

        if not (access.first.value.is_integer() and access.second.value.is_integer()):
            raise NeoRuntimeError("Indieces must be whole numbers", access.line, access.column)

        if not isinstance(matrix, Matrix):
            raise NeoRuntimeError("Matrix is needed for access operation", access.line, access.column)

        return matrix.rows[int(access.first.value)][int(access.second.value)]
                

    def visit_property(self, property:Property):
        object = property.object_name.accept(self)

        if not isinstance(object, Matrix):
            raise NeoRuntimeError("Only supported object for now is Matrix", property.line, property.column)

        try: 
            property_getter = object.properties[property.property_name.value]
        except KeyError:
            raise NeoRuntimeError(f"Unknown property '{property.property_name.value}'", property.line, property.column)

        return property_getter()


    def visit_unary_operator(self, unary:UnaryOperator):
        right = unary.rvalue.accept(self)

        # Obsługa macierzy obsłużona poprzez __neg__
        if unary.op == OperatorType.MINUS:
            return -right

        if unary.op == OperatorType.NOT:
            return not bool(right)

        raise NeoRuntimeError("Unknown unary operator", unary.line, unary.column)


    def visit_binary_operator(self, binary:BinaryOperator):
        left = binary.lvalue.accept(self)
        right = binary.rvalue.accept(self)

        if binary.op == OperatorType.PLUS:
            return left + right
        if binary.op == OperatorType.MINUS:
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError(f"Strings cannot take part in substract operation", binary.lvalue.line, binary.lvalue.column)
            return left - right
        if binary.op == OperatorType.MULTIPLY:
            if isinstance(left, str) and isinstance(right, str):
                raise NeoRuntimeError(f"Cannot multiply two strings", binary.lvalue.line, binary.lvalue.column)
            return left * right
        if binary.op == OperatorType.DIVIDE:
            if isinstance(left, Matrix) or isinstance(right, Matrix):
                raise NeoRuntimeError(f"Matrixes cannot take part in divide operation", binary.lvalue.line, binary.lvalue.column)
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError(f"Strings cannot take part in substract operation", binary.lvalue.line, binary.lvalue.column)
            try:
                return left / right
            except ZeroDivisionError:
                raise NeoRuntimeError(f"Cannot divide by zero", binary.lvalue.line, binary.lvalue.column)

        # Obsługa różnych typów obsłużona poprzez __eq__
        if binary.op == OperatorType.EQUAL:
            return left == right
        if binary.op == OperatorType.NOT_EQUAL:
            return left != right

        if binary.op == OperatorType.AND:
            return left and right
        if binary.op == OperatorType.OR:
            return left or right

        # Porównania
        if binary.op == OperatorType.GREATER:
            try: 
                return left > right
            except TypeError:
                raise NeoRuntimeError(f"Types '{type(left).__name__}' and '{type(right).__name__}' cannot be compared with '>' operator", binary.lvalue.line, binary.lvalue.column)
        if binary.op == OperatorType.GREATER_OR_EQUAL:
            try: 
                return left >= right
            except TypeError:
                raise NeoRuntimeError(f"Types '{type(left).__name__}' and '{type(right).__name__}' cannot be compared with '>=' operator", binary.lvalue.line, binary.lvalue.column)
        if binary.op == OperatorType.LESS:
            try: 
                return left < right
            except TypeError:
                raise NeoRuntimeError(f"Types '{type(left).__name__}' and '{type(right).__name__}' cannot be compared with '<' operator", binary.lvalue.line, binary.lvalue.column)
        if binary.op == OperatorType.LESS_OR_EQUAL:
            try: 
                return left <= right
            except TypeError:
                raise NeoRuntimeError(f"Types '{type(left).__name__}' and '{type(right).__name__}' cannot be compared with '<=' operator", binary.lvalue.line, binary.lvalue.column)

        raise NeoRuntimeError("Unknown binary operator", binary.line, binary.column)


        # Scalar or bool or string
    def visit_literal(self, literal):
        return literal.value