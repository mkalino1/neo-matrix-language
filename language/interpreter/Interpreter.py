from language.nodes.Instructions import Assignment, Block, FunctionCall, IfStatement, Return, WhileLoop, Declaration
from language.nodes.ToplevelObjects import Function
from language.nodes.Expressions import Access, BinaryOperator, Identifier, Matrix, Property, UnaryOperator
from language.nodes.OperatorType import OperatorType
from language.errors.InterpreterExceptions import NeoRuntimeError
from language.interpreter.Built_ins import builtin_functions

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
        self.scopes = [{}]


    def visit_function_declaration(self, function:Function):
        if function.name.value in builtin_functions:
            raise NeoRuntimeError(f"Function name '{function.name.value}' is reserved for build-in function", function.name.line, function.name.column)

        # Store function in the current scope as a value
        self.scopes[-1][function.name.value] = (function, False)


    def visit_function_call(self, function_call:FunctionCall):
        line = function_call.function_name.line
        column = function_call.function_name.column
        function_name = function_call.function_name.value

        if function_name in builtin_functions:
            builtin_function = builtin_functions[function_name]
            return builtin_function(line, column, *[arg.accept(self) for arg in function_call.arguments])

        # Look for function in scopes
        function = None
        for scope in self.scopes[::-1]:
            if function_name in scope:
                value, _ = scope[function_name]
                if isinstance(value, Function):
                    function = value
                    break
        
        if function is None:
            raise NeoRuntimeError(f"Function '{function_name}' doesn't exist", line, column)

        if len(function.parameter_list) != len(function_call.arguments):
            raise NeoRuntimeError("Incorrect number of arguments", line, column)

        for param, arg in zip(function.parameter_list, function_call.arguments):
            # Always store as (value, mutable=False) for parameters
            function.block.passed_variables[param.value] = (arg.accept(self), False)

        return function.block.accept(self)

    def visit_block(self, block:Block):
        if block.closure:
            self.scopes.append(block.closure)

        # creating a new scope for the block
        self.scopes.append({})

        if block.passed_variables:
            self.scopes[-1].update(block.passed_variables)

        return_value = None
        for instruction in block.instructions:
            return_value = instruction.accept(self)
            if isinstance(instruction, Return):
                break

        if isinstance(return_value, Function):
            return_value.block.closure = self.scopes[-1]
        
        self.scopes.pop()
        # Clean up the closure scopes
        if block.closure:
            self.scopes.pop()

        return return_value


    def visit_if_statement(self, if_statement:IfStatement):
        condition = if_statement.condition.accept(self)

        if condition:
            return if_statement.block.accept(self)
        elif if_statement.else_block:
            return if_statement.else_block.accept(self)


    def visit_while_loop(self, while_loop:WhileLoop):
        condition = while_loop.condition.accept(self)

        return_value = None
        while condition:
            return_value = while_loop.block.accept(self)
            if (return_value is None):
                condition = while_loop.condition.accept(self)
            else:
                return return_value


    def visit_return(self, return_instruction:Return):
        if return_instruction.expression is None:
            return None
        return return_instruction.expression.accept(self)


    def visit_assignment(self, assignment:Assignment):
        expression_value = assignment.expression.accept(self)

        if not assignment.first_index:
            # Only allow assignment if variable already exists in any scope
            for scope in self.scopes[::-1]:
                if assignment.identifier.value in scope:
                    old_value, mutable = scope[assignment.identifier.value]
                    if not mutable:
                        raise NeoRuntimeError(
                            f"Variable '{assignment.identifier.value}' is immutable and cannot be assigned to",
                            assignment.line,
                            assignment.column
                        )
                    scope[assignment.identifier.value] = (expression_value, mutable)
                    break
            else:
                raise NeoRuntimeError(
                    f"Variable '{assignment.identifier.value}' must be declared before assignment",
                    assignment.line,
                    assignment.column
                )
        else:
            first_index_value = assignment.first_index.accept(self)
            second_index_value = assignment.second_index.accept(self)

            if not (first_index_value.is_integer() and second_index_value.is_integer()):
                raise NeoRuntimeError("Indices must be whole numbers", assignment.line, assignment.column)
            for scope in self.scopes[::-1]:
                if assignment.identifier.value in scope:
                    matrix, mutable = scope[assignment.identifier.value]
                    if not isinstance(matrix, Matrix):
                        raise NeoRuntimeError("Only matrix can use access operation", assignment.line, assignment.column)
                    if not mutable:
                        raise NeoRuntimeError(
                            f"Matrix variable '{assignment.identifier.value}' is immutable and cannot be modified",
                            assignment.line,
                            assignment.column
                        )
                    matrix.rows[int(first_index_value)][int(second_index_value)] = expression_value
                    return
            raise NeoRuntimeError(f"Matrix {assignment.identifier.value} doesn't exist", assignment.line, assignment.column)     


    def visit_declaration(self, declaration:Declaration):
        identifier = declaration.identifier.value
        if identifier in self.scopes[-1]:
            raise NeoRuntimeError(f"Variable '{identifier}' already declared in this scope", declaration.line, declaration.column)
        value = declaration.expression.accept(self)
        self.scopes[-1][identifier] = (value, declaration.mutable)


    def visit_identifier(self, identifier:Identifier):
        for scope in self.scopes[::-1]:
            if identifier.value in scope:
                value, _ = scope[identifier.value]
                return value
        
        raise NeoRuntimeError(f"Variable '{identifier.value}' doesn't exist", identifier.line, identifier.column) 


    def visit_matrix(self, matrix:Matrix):
        values = []
        for row in matrix.rows:
            values_row = []
            for cell in row:
                value = cell.accept(self)
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
            raise NeoRuntimeError("Only matrix can have properties", property.line, property.column)

        try: 
            property_getter = object.properties[property.property_name.value]
        except KeyError:
            raise NeoRuntimeError(f"Unknown property '{property.property_name.value}'", property.line, property.column)

        return property_getter()


    def visit_unary_operator(self, unary:UnaryOperator):
        right = unary.rvalue.accept(self)

        # Matrix handling is done through __neg__
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
        elif binary.op == OperatorType.MINUS:
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError("Strings cannot take part in substract operation", binary.lvalue.line, binary.lvalue.column)
            return left - right
        elif binary.op == OperatorType.MULTIPLY:
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError("Strings cannot take part in multiply operation", binary.lvalue.line, binary.lvalue.column)
            return left * right
        elif binary.op == OperatorType.DIVIDE:
            if isinstance(left, Matrix) or isinstance(right, Matrix):
                raise NeoRuntimeError("Matrixes cannot take part in divide operation", binary.lvalue.line, binary.lvalue.column)
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError("Strings cannot take part in substract operation", binary.lvalue.line, binary.lvalue.column)
            try:
                return left / right
            except ZeroDivisionError:
                raise NeoRuntimeError("Cannot divide by zero", binary.lvalue.line, binary.lvalue.column)
        elif binary.op == OperatorType.DIVIDE_INTEGER:
            if isinstance(left, Matrix) or isinstance(right, Matrix):
                raise NeoRuntimeError("Matrixes cannot take part in integer divide operation", binary.lvalue.line, binary.lvalue.column)
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError("Strings cannot take part in integer divide operation", binary.lvalue.line, binary.lvalue.column)
            try:
                return left // right
            except ZeroDivisionError:
                raise NeoRuntimeError("Cannot divide by zero", binary.lvalue.line, binary.lvalue.column)
        elif binary.op == OperatorType.POWER:
            if isinstance(left, str) or isinstance(right, str):
                raise NeoRuntimeError("Strings cannot take part in power operation", binary.lvalue.line, binary.lvalue.column)
            return left ** right

        # Different types handling is done through __eq__
        if binary.op == OperatorType.EQUAL:
            return left == right
        if binary.op == OperatorType.NOT_EQUAL:
            return left != right

        if binary.op == OperatorType.AND:
            return left and right
        if binary.op == OperatorType.OR:
            return left or right

        # Comparisons
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