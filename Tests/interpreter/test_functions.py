import re
import pytest
from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceString

def run_neo_and_assert(program, expected_output, capsys):
    source = SourceString(program)
    lexer = Lexer(source)
    parser = Parser(lexer)
    interpreter = Interpreter(parser.parse_program())
    interpreter.run()
    captured = capsys.readouterr()
    assert re.sub(r'\s+', '', captured.out) == re.sub(r'\s+', '', expected_output)

def test_recursive_fibonacci(capsys):
    program = '''
    function fibonnaci(n){
       if (n <= 1){
            return n;
       }
       else{
           return fibonnaci(n-1) + fibonnaci(n-2);
       }
    }
    print(fibonnaci(10));
    '''
    expected = '''
    55.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_recursive_factorial(capsys):
    program = '''
    function factorial(n){
       if (n == 1){
            return n;
       }
       else{
           return n*factorial(n-1);
       }
    }
    print(factorial(5));
    '''
    expected = '''
    120.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_scope_and_shadowing(capsys):
    program = '''
    var mut a = 2;
    var arg = 0;
    function scope(arg){
        print(a);
        a = 4;
        print(a);
        print(arg);
    }
    scope(8);
    print(arg);
    '''
    expected = '''
    2.0
    4.0
    8.0
    0.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_scope_reassignment_error(capsys):
    program = '''
    var a = 2;
    function scope(){
        a = 4;
    }
    scope();
    '''
    run_neo_and_assert(program, "Error at line: 4, column: 9. Variable 'a' is immutable and cannot be assigned to", capsys)

def test_function_call_with_expression_args(capsys):
    program = '''
    function test(arg1, arg2){
        print(arg1);
        print(arg2);
    }
    test("kra"+"kow", "" or 4);
    '''
    expected = '''
    krakow
    4.0
    '''
    run_neo_and_assert(program, expected, capsys) 