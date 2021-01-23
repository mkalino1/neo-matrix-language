from Objects.Instructions import Assignment, Block, FunctionCall, IfStatement, Return, WhileLoop
from Objects.ToplevelObjects import Function
from Objects.Expressions import Access, BinaryOperator, Identifier, Matrix, Property, Scalar, UnaryOperator
from Objects.OperatorType import OperatorType
    
class Interpreter():
    def __init__(self, parsed_program):
        self.parsed_objects = parsed_program.toplevel_objects
        self.visitor = Visitor()

    def run(self):
        # try:
            # value = evaluate(expression)
            # print(value)
        for top_level_object in self.parsed_objects:
            print(f'TOP LEVEL: {top_level_object.accept(self.visitor)}')
        # except RuntimeError: 
        #     print("Error has occured")
        return "Job is done"

                

class Visitor:
    def __init__(self):
        self.variables = [{}]
        self.functions = {}

    # Scalar or bool or string
    def visit_literal(self, literal):
        return literal.value


    def visit_function(self, function:Function):
        self.functions[function.name.value] = function


    def visit_function_call(self, function_call:FunctionCall):
        function:Function = self.functions[function_call.function_name.value]

        if len(function.parameter_list) != len(function_call.arguments):
            raise RuntimeError("Incorrect number of arguments")

        for param, arg in zip(function.parameter_list, function_call.arguments):
            function.block.passed_variables[param.value] = arg.accept(self)

        return function.block.accept(self)


    def visit_block(self, block:Block):
        print(f'Weszlismy w blok, instrukcje: {block.instructions}, zmienne passed: {block.passed_variables}')

        self.variables.append({})

        # jeśli blok ten jest ciałem funkcji to trzeba dołączyć przekazane jako argumenty zmienne
        self.variables[-1].update(block.passed_variables)

        return_value = None
        for instruction in block.instructions:
            if isinstance(instruction, Return):
                print("Pierwsze wystapienie return instruction osiagniete")
                return_value = instruction.accept(self)
                break 
            instruction.accept(self)

        self.variables.pop()
        return return_value


    def visit_if_statement(self, if_statement:IfStatement):
        condition = if_statement.condition.accept(self)

        if condition:
            if_statement.block.accept(self)
        elif if_statement.else_block:
            if_statement.else_block.accept(self)


    def visit_while_loop(self, while_loop:WhileLoop):
        condition = while_loop.condition.accept(self)

        while condition:
            while_loop.block.accept(self)
            condition = while_loop.condition.accept(self)


    def visit_return(self, return_instruction:Return):
        return return_instruction.expression.accept(self)


    def visit_assignment(self, assignment:Assignment):
        expression_value = assignment.expression.accept(self)

        for scope in self.variables[::-1]:
            if assignment.identifier.value in scope:
                scope[assignment.identifier.value] = expression_value
        self.variables[-1][assignment.identifier.value] = expression_value


    def visit_identifier(self, identifier:Identifier):
        for scope in self.variables[::-1]:
            if identifier.value in scope:
                print(f'Variable found: {scope[identifier.value]}')
                return scope[identifier.value]
        
        raise RuntimeError("Variable doesn't exist") 


    def visit_matrix(self, matrix:Matrix):
        return matrix


    def visit_access(self, access:Access):
        matrix = access.identifier.accept(self)

        if not isinstance(matrix, Matrix):
            raise RuntimeError("Matrix is needed for access operation")

        return matrix.rows[access.first.value][access.second.value]
                

    def visit_property(self, property:Property):
        object = property.object_name.accept(self)

        if not isinstance(object, Matrix):
            raise RuntimeError("Only supported object is Matrix")

        return object.properties[property.property_name.value]


    def visit_unary_operator(self, unary:UnaryOperator):
        right = unary.rvalue.accept(self)

        # TODO: rozbudowac obsluge roznych typow. Matrix przede wszystkim
        if unary.op == OperatorType.MINUS:
            return -right

        if unary.op == OperatorType.NOT:
            return not bool(right)

        raise RuntimeError("Unknown unary operator")


    def visit_binary_operator(self, binary:BinaryOperator):
        left = binary.lvalue.accept(self)
        right = binary.rvalue.accept(self)

        # TODO: konkatenacja stringow
        if binary.op == OperatorType.PLUS:
            return left + right
        if binary.op == OperatorType.MINUS:
            return left - right
        if binary.op == OperatorType.MULTIPLY:
            return left * right
        if binary.op == OperatorType.DIVIDE:
            return left / right

        if binary.op == OperatorType.GREATER:
            return left > right
        if binary.op == OperatorType.GREATER_OR_EQUAL:
            return left >= right
        if binary.op == OperatorType.LESS:
            return left < right
        if binary.op == OperatorType.LESS_OR_EQUAL:
            return left <= right

        # TODO: jakas funkcja isEqual?
        if binary.op == OperatorType.EQUAL:
            return left == right
        if binary.op == OperatorType.NOT_EQUAL:
            return left != right

        raise RuntimeError("Unknown binary operator")