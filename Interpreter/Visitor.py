from Objects.Instructions import Block, Return
from Objects.ToplevelObjects import Function
from Objects.Expressions import BinaryOperator, Scalar, UnaryOperator
from Objects.OperatorType import OperatorType
    
class Interpreter():
    def __init__(self, parsed_program):
        self.parsed_objects = parsed_program.toplevel_objects
        self.visitor = Visitor()

    def run(self):
        for function in self.parsed_objects:
            return function.accept(self.visitor)
                

class Visitor:
    def visit_scalar(self, scalar:Scalar):
        return scalar.value

    def evaluate(self, expression):
        return expression.accept(self)

    def visit_function(self, function:Function):
        return function.block.accept(self)

    def visit_block(self, block:Block):
        for instruction in block.instructions:
            return instruction.accept(self)

    def visit_return(self, return_instruction:Return):
        return return_instruction.expression.accept(self)

    def visit_unary_operator(self, unary:UnaryOperator):
        right = self.evaluate(unary.rvalue)

        # TODO: rozbudowac obsluge roznych typow. Matrix przede wszystkim
        if unary.op == OperatorType.MINUS:
            return right

        if unary.op == OperatorType.NOT:
            return not bool(right)

        raise Exception("Unknown unary operator")


    def visit_binary_operator(self, binary:BinaryOperator):
        left = self.evaluate(binary.lvalue)
        right = self.evaluate(binary.rvalue)

        # TODO: konkatenacja stringow
        if binary.op == OperatorType.PLUS:
            return left + right

        # switch (expr.operator.type) {
        # case MINUS:
        #     return (double)left - (double)right;
        # case SLASH:
        #     return (double)left / (double)right;
        # case STAR:
        #     return (double)left * (double)right;
        # }

        raise Exception("Unknown binary operator")