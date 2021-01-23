from Objects.Instructions import Assignment, Block, FunctionCall, Return
from Objects.ToplevelObjects import Function
from Objects.Expressions import BinaryOperator, Identifier, Scalar, UnaryOperator
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
        self.global_variables = {}
        self.functions = {}

    # Scalar or bool or string
    def visit_literal(self, literal):
        return literal.value


    def evaluate(self, expression):
        return expression.accept(self)


    def visit_function(self, function:Function):
        self.functions[function.name.value] = function


    def visit_function_call(self, function_call:FunctionCall):
        function:Function = self.functions[function_call.function_name.value]

        if len(function.parameter_list) != len(function_call.arguments):
            raise RuntimeError("Incorrect number of arguments")

        for param, arg in zip(function.parameter_list, function_call.arguments):
            function.block.local_variables[param.value] = arg.value

        return function.block.accept(self)


    def visit_block(self, block:Block):
        print(f'Weszlismy w blok, instrukcje: {block.instructions}, zmienne lokalne: {block.local_variables}')

        for instruction in block.instructions:
            if isinstance(instruction, Return):
                print("Pierwsze wystapienie return instruction osiagniete")
                return instruction.accept(self)
            instruction.accept(self)


    def visit_return(self, return_instruction:Return):
        return return_instruction.expression.accept(self)


    def visit_assignment(self, assignment:Assignment):
        # co jesli juz jest
        self.global_variables[assignment.identifier.value] = assignment.expression.accept(self)
        return assignment.expression.accept(self)

    def visit_identifier(self, identifier:Identifier):
        print(f'hello from visit id: {self.global_variables[identifier.value]}')
        return self.global_variables[identifier.value]


    def visit_unary_operator(self, unary:UnaryOperator):
        right = self.evaluate(unary.rvalue)

        # TODO: rozbudowac obsluge roznych typow. Matrix przede wszystkim
        if unary.op == OperatorType.MINUS:
            return right

        if unary.op == OperatorType.NOT:
            return not bool(right)

        raise RuntimeError("Unknown unary operator")


    def visit_binary_operator(self, binary:BinaryOperator):
        left = self.evaluate(binary.lvalue)
        right = self.evaluate(binary.rvalue)

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