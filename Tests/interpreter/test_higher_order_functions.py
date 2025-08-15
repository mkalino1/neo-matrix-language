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

def test_function_as_argument(capsys):
    program = '''
    # Basic arithmetic functions
    function add(x, y) {
        return x + y;
    }

    function multiply(x, y) {
        return x * y;
    }

    function subtract(x, y) {
        return x - y;
    }

    function square(x) {
        return x * x;
    }

    function double(x) {
        return x * 2;
    }

    # Function as argument - map-like behavior
    function apply_operation(operation, x, y) {
        return operation(x, y);
    }

    print("apply_operation(add, 5, 3):", apply_operation(add, 5, 3));
    print("apply_operation(multiply, 4, 6):", apply_operation(multiply, 4, 6));
    print("apply_operation(subtract, 10, 4):", apply_operation(subtract, 10, 4));
    '''
    expected = '''
    apply_operation(add, 5, 3): 8.0
    apply_operation(multiply, 4, 6): 24.0
    apply_operation(subtract, 10, 4): 6.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_returning_function(capsys):
    """Test functions that return other functions using closures"""
    program = '''
    function create_adder(base) {
        function add(value) {
            return base + value;
        }
        return add;
    }
    
    function create_multiplier(factor) {
        function multiply(value) {
            return factor * value;
        }
        return multiply;
    }
    
    var add_five = create_adder(5);
    var multiply_by_three = create_multiplier(3);
    
    print("add_five(3):", add_five(3));
    print("add_five(7):", add_five(7));
    print("multiply_by_three(4):", multiply_by_three(4));
    print("multiply_by_three(6):", multiply_by_three(6));
    '''
    
    expected = '''
    add_five(3): 8.0
    add_five(7): 12.0
    multiply_by_three(4): 12.0
    multiply_by_three(6): 18.0
    '''
    
    run_neo_and_assert(program, expected, capsys)

def test_function_composition(capsys):
    program = '''
    function add_one(x) {
        return x + 1;
    }

    function double(x) {
        return x * 2;
    }

    function square(x) {
        return x * x;
    }

    # Function composition
    function compose(f, g, x) {
        return f(g(x));
    }

    print("Function composition:");
    print("compose(add_one, double, 5):", compose(add_one, double, 5));
    print("compose(square, add_one, 3):", compose(square, add_one, 3));
    print("compose(double, square, 4):", compose(double, square, 4));
    '''
    expected = '''
    Function composition:
    compose(add_one, double, 5): 11.0
    compose(square, add_one, 3): 16.0
    compose(double, square, 4): 32.0
    '''
    run_neo_and_assert(program, expected, capsys)