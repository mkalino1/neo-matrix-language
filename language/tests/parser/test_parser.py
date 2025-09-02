from ...nodes.ToplevelObjects import Function
from ...nodes.Instructions import Block, FunctionCall, IfStatement, Return
from ...nodes.Expressions import *
from ...lexer.Lexer import Lexer
from ...parser.Parser import Parser
from ...lexer.Source import SourceString
from ...nodes.OperatorType import OperatorType


def test_literals():
    neo_code = '''
    # Literal = Bool | String | Scalar | Matrix | FunctionCall | ObjectProperty | MatrixAccess | Identifier;

    var a = [1, 2 | 4, 5];
    var b = 5;
    var c = True;
    var d = "Hello";
    var e = myfun("argument");
    var f = obj.method;
    var g = matrix[3, 4];
    var h = matrix[2];
    var j = some_variable;
    '''
    parser = Parser(Lexer(SourceString(neo_code)))
    assignments = (x for x in parser.parse_program().toplevel_objects)

    assert isinstance(next(assignments).expression, Matrix)
    assert isinstance(next(assignments).expression, Scalar)
    assert isinstance(next(assignments).expression, Bool)
    assert isinstance(next(assignments).expression, String)
    assert isinstance(next(assignments).expression, FunctionCall)
    assert isinstance(next(assignments).expression, Property)
    assert isinstance(next(assignments).expression, Access)
    assert isinstance(next(assignments).expression, Access)
    assert isinstance(next(assignments).expression, Identifier)


def test_order_of_operations():
    neo_code = '''
    var a = (1 + 2) * 3;
    a = 1 + (2 * 3);
    a = 1 + 2 * 3;

    a = 1 <= 2 == 3 >= 4;

    a = 1 <= 2 == 3 >= 4 and 1 <= 2 == 3 >= 4;

    a = 10 - some_variable;

    a = not (10 == ten);
    '''
    parser = Parser(Lexer(SourceString(neo_code)))
    objects = (x for x in parser.parse_program().toplevel_objects)

    assert isinstance(next(objects).expression.lvalue, BinaryOperator)
    assert isinstance(next(objects).expression.lvalue, Scalar)
    assert isinstance(next(objects).expression.lvalue, Scalar)

    expression = next(objects).expression
    assert expression.op == OperatorType.EQUAL
    assert expression.lvalue.op == OperatorType.LESS_OR_EQUAL
    assert expression.rvalue.op == OperatorType.GREATER_OR_EQUAL

    expression = next(objects).expression
    assert expression.op == OperatorType.AND

    expression = next(objects).expression
    assert expression.op == OperatorType.MINUS

    expression = next(objects).expression
    assert expression.op == OperatorType.NOT


def test_function():
    neo_code = '''
    func example(raz, dwa){
        if(3){
            return matrix.det;
        }
        else {
            add("nothing");
        }
    }
    '''
    parser = Parser(Lexer(SourceString(neo_code)))
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