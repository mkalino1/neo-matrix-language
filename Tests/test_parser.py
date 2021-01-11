from Lexer.Token import Type
from Objects.ToplevelObjects import Function
from Objects.Instructions import Block, FunctionCall, IfStatement, Return
from Objects.Expressions import *
from Lexer.Lexer import Lexer
from Parser.Parser import Parser


def test_literals():
    parser = Parser(Lexer(filename="./Tests/ParserTestFiles/literals.neo"))
    assignments = (x for x in parser.parse_program().toplevel_objects)

    assert isinstance(next(assignments).expression, Matrix)
    assert isinstance(next(assignments).expression, Scalar)
    assert isinstance(next(assignments).expression, Bool)
    assert isinstance(next(assignments).expression, String)
    assert isinstance(next(assignments).expression, FunctionCall)
    assert isinstance(next(assignments).expression, Property)
    assert isinstance(next(assignments).expression, Access)
    assert isinstance(next(assignments).expression, Identifier)


def test_order_of_operations():
    parser = Parser(Lexer(filename="./Tests/ParserTestFiles/order.neo"))
    objects = (x for x in parser.parse_program().toplevel_objects)

    assert isinstance(next(objects).expression.lvalue, BinaryOperator)
    assert isinstance(next(objects).expression.lvalue, Scalar)
    assert isinstance(next(objects).expression.lvalue, Scalar)

    expression = next(objects).expression
    assert expression.op == Type.EQUAL_TO
    assert expression.lvalue.op == Type.LESS_OR_EQUAL_TO
    assert expression.rvalue.op == Type.GREATER_OR_EQUAL_TO

    expression = next(objects).expression
    assert expression.op == Type.AND

    expression = next(objects).expression
    assert expression.op == Type.MINUS

    expression = next(objects).expression
    assert expression.op == Type.NOT


def test_function():
    parser = Parser(Lexer(filename="./Tests/ParserTestFiles/function.neo"))
    objects = (x for x in parser.parse_program().toplevel_objects)
    fun = next(objects)
    assert isinstance(fun, Function)
    assert isinstance(fun.block, Block)
    assert isinstance(fun.name, Identifier)
    assert isinstance(fun.block.instructions[0], IfStatement)
    assert isinstance(fun.block.instructions[0].condition, Scalar)
    assert isinstance(fun.block.instructions[0].else_block.instructions[0], FunctionCall)
    assert isinstance(fun.block.instructions[0].block.instructions[0], Return)
    assert isinstance(fun.block.instructions[0].block.instructions[0].expression, Property)