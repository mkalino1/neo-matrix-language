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

def test_simple_pipe_operation(capsys):
    """Test basic pipe operation with user-defined function"""
    program = '''
    func double(x) {
        return x * 2
    }
    
    var result = 5 |> double
    print(result)
    '''
    expected = '''
    10
    '''
    run_neo_and_assert(program, expected, capsys)

def test_chained_pipe_operations(capsys):
    """Test multiple pipe operations chained together"""
    program = '''
    func addOne(x) {
        return x + 1
    }
    
    func multiplyByTwo(x) {
        return x * 2
    }
    
    func addExclamation(text) {
        return text + "!"
    }
    
    var result = 3 |> addOne |> multiplyByTwo
    print(result)
    
    var text = "Hello" |> addExclamation |> addExclamation
    print(text)
    '''
    expected = '''
    8
    Hello!!
    '''
    run_neo_and_assert(program, expected, capsys)


def test_pipe_with_builtin_functions(capsys):
    """Test pipe operations with builtin functions"""
    program = '''
    func process(x) {
        return x * 2
    }
    
    "Hello" |> print
    5 |> process |> print
    '''
    expected = '''
    Hello
    10
    '''
    run_neo_and_assert(program, expected, capsys)


def test_pipe_precedence(capsys):
    """Test that pipe operator has correct precedence"""
    program = '''
    var combined = 5 < 10 |> print
    '''
    expected = '''
    True
    '''
    run_neo_and_assert(program, expected, capsys)


def test_pipe_with_matrix_operations(capsys):
    """Test pipe operations with matrix operations"""
    program = '''
    func createMatrix(size) {
        return zeros(size, size)
    }
    
    func processMatrix(matrix) {
        return matrix[0][0]
    }
    
    var result = 3 |> createMatrix |> processMatrix
    print(result)
    '''
    expected = '''
    0
    '''
    run_neo_and_assert(program, expected, capsys)


def test_pipe_with_conditional_functions(capsys):
    """Test pipe operations with functions that return different types"""
    program = '''
    func isPositive(x) {
        return x > 0
    }
    
    func formatResult(x) {
        if (x) {
            return "Positive"
        } else {
            return "Not positive"
        }
    }
    
    var result1 = 5 |> isPositive |> formatResult
    var result2 = -3 |> isPositive |> formatResult
    print(result1)
    print(result2)
    '''
    expected = '''
    Positive
    Not positive
    '''
    run_neo_and_assert(program, expected, capsys)

def test_pipe_with_nested_expressions(capsys):
    """Test pipe operations with complex nested expressions"""
    program = '''
    func square(x) {
        return x * x
    }
    
    # Test: 2 + 3 |> square
    2 + 3 |> square |> print
    '''
    expected = '''
    25
    '''
    run_neo_and_assert(program, expected, capsys)


def test_pipe_with_closure_functions(capsys):
    """Test pipe operations with functions that use closures"""
    program = '''
    func createMultiplier(factor) {
        func multiply(x) {
            return x * factor
        }
        return multiply
    }
    
    var double = createMultiplier(2)
    var triple = createMultiplier(3)
    
    var result1 = 5 |> double
    var result2 = 4 |> triple
    print(result1)
    print(result2)
    '''
    expected = '''
    10
    12
    '''
    run_neo_and_assert(program, expected, capsys)

def test_pipe_with_recursive_functions(capsys):
    """Test pipe operations with recursive functions"""
    program = '''
    func factorial(n) {
        if (n <= 1) {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }

    4 |> factorial |> print
    '''
    expected = '''
    24
    '''
    run_neo_and_assert(program, expected, capsys)

def test_pipe_with_function_objects(capsys):
    """Test pipe operations with Function objects stored in variables"""
    program = '''
    3 |> func(x) {return x + 1} |> print
    '''
    expected = '''
    4
    '''
    run_neo_and_assert(program, expected, capsys)
