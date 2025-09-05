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

def test_basic_iife(capsys):
    """Test basic IIFE functionality"""
    program = """
    print(func() {
        return 42
    }())
    """
    expected = "42"
    run_neo_and_assert(program, expected, capsys)

def test_iife_with_parameters(capsys):
    """Test IIFE with parameters"""
    program = """
    print(func(x, y) {
        return x + y
    }(10, 20))
    """
    expected = "30"
    run_neo_and_assert(program, expected, capsys)

def test_iife_with_no_parameters(capsys):
    """Test IIFE with no parameters"""
    program = """
    print(func() {
        return "Hello World"
    }())
    """
    expected = "Hello World"
    run_neo_and_assert(program, expected, capsys)

def test_iife_with_side_effects(capsys):
    """Test IIFE that modifies variables"""
    program = """
    var mut x = 0
    var temp = func() {
        x = 100
    }()
    print(x)
    """
    expected = "100"
    run_neo_and_assert(program, expected, capsys)

def test_iife_returns_function(capsys):
    """Test IIFE that returns a function"""
    program = """
    var double_func = func() {
        return func(x) {
            return x * 2
        }
    }()
    print(double_func(5))
    """
    expected = "10"
    run_neo_and_assert(program, expected, capsys)
