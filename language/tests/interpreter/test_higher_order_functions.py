import re
from ...interpreter.Interpreter import Interpreter
from ...lexer.Lexer import Lexer
from ...parser.Parser import Parser
from ...lexer.Source import SourceString

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
    func add(x, y) {
        return x + y
    }

    func multiply(x, y) {
        return x * y
    }

    func subtract(x, y) {
        return x - y
    }

    func square(x) {
        return x * x
    }

    func double(x) {
        return x * 2
    }

    # Function as argument - map-like behavior
    func apply_operation(operation, x, y) {
        return operation(x, y)
    }

    print("apply_operation(add, 5, 3):", apply_operation(add, 5, 3))
    print("apply_operation(multiply, 4, 6):", apply_operation(multiply, 4, 6))
    print("apply_operation(subtract, 10, 4):", apply_operation(subtract, 10, 4))
    '''
    expected = '''
    apply_operation(add, 5, 3): 8
    apply_operation(multiply, 4, 6): 24
    apply_operation(subtract, 10, 4): 6
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_returning_function(capsys):
    """Test functions that return other functions using closures"""
    program = '''
    func create_adder(base) {
        func add(value) {
            return base + value
        }
        return add
    }
    
    func create_multiplier(factor) {
        func multiply(value) {
            return factor * value
        }
        return multiply
    }
    
    var add_five = create_adder(5)
    var multiply_by_three = create_multiplier(3)
    
    print("add_five(3):", add_five(3))
    print("add_five(7):", add_five(7))
    print("multiply_by_three(4):", multiply_by_three(4))
    print("multiply_by_three(6):", multiply_by_three(6))
    '''
    
    expected = '''
    add_five(3): 8
    add_five(7): 12
    multiply_by_three(4): 12
    multiply_by_three(6): 18
    '''
    
    run_neo_and_assert(program, expected, capsys)

def test_function_composition(capsys):
    program = '''
    func add_one(x) {
        return x + 1
    }

    func double(x) {
        return x * 2
    }

    func square(x) {
        return x * x
    }

    # Function composition
    func compose(f, g, x) {
        return f(g(x))
    }

    print("Function composition:")
    print("compose(add_one, double, 5):", compose(add_one, double, 5))
    print("compose(square, add_one, 3):", compose(square, add_one, 3))
    print("compose(double, square, 4):", compose(double, square, 4))
    '''
    expected = '''
    Function composition:
    compose(add_one, double, 5): 11
    compose(square, add_one, 3): 16
    compose(double, square, 4): 32
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_returning_global_function(capsys):
    program = '''
    func add(x, y) {
        return x + y
    }

    func multiply(x, y) {
        return x * y
    }

    func subtract(x, y) {
        return x - y
    }

    # Function that returns a function - operation factory
    func create_operation(operation_type) {
        if (operation_type == "add") {
            return add
        } else {
            if (operation_type == "multiply") {
                return multiply
            } else {
                if (operation_type == "subtract") {
                    return subtract
                } else {
                    return add  # Default
                }
            }
        }
    }

    var add_op = create_operation("add")
    var mult_op = create_operation("multiply")
    var sub_op = create_operation("subtract")

    print("add_op(8, 2):", add_op(8, 2))
    print("mult_op(8, 2):", mult_op(8, 2))
    print("sub_op(8, 2):", sub_op(8, 2))
    '''
    expected = '''
    add_op(8, 2): 10
    mult_op(8, 2): 16
    sub_op(8, 2): 6
    '''
    run_neo_and_assert(program, expected, capsys)