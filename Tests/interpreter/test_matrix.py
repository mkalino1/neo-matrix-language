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

def test_matrix_determinant(capsys):
    program = '''
    m2 = [1, 2 | 3, 4];
    m3 = [6, 1, 1 | 4, -2, 5 | 2, 8, 7];
    print(m2.det);
    print(m3.det);
    '''
    expected = '''
    -2.0
    -306.0
    '''
    run_neo_and_assert(program, expected, capsys)


def test_matrix_arithmetic_and_equality(capsys):
    program = '''
    m = [1, 2 | 3, 4];
    n = [11, 22 | 33, 44];
    print(10+m*2);
    print(-10-m*2);
    print(n + m == n - (-m));
    '''
    expected = '''
    ---------------
    | 12.0   14.0 |
    | 16.0   18.0 |
    ---------------
    -----------------
    | -12.0   -14.0 |
    | -16.0   -18.0 |
    -----------------
    True
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_copy_and_assignment(capsys):
    program = '''
    m = zeros(2);
    n = m.copy;
    m[0, 0] = 5;
    print(n);
    print(m);
    '''
    expected = '''
    ---------
    | 0   0 |
    | 0   0 |
    ---------
    -----------
    | 5.0   0 |
    |   0   0 |
    -----------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_transpose(capsys):
    program = '''
    m = zeros(2, 3);
    n = m.transposed;
    print(n);
    print(m);
    '''
    expected = '''
    ---------
    | 0   0 |
    | 0   0 |
    | 0   0 |
    ---------
    -------------
    | 0   0   0 |
    | 0   0   0 |
    -------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_power_identity_and_square(capsys):
    program = '''
    m = [2, 0 | 0, 2];
    print(m ^ 0); # Identity
    print(m ^ 1); # Itself
    print(m ^ 2); # Squared
    '''
    expected = '''
    -------------
    | 1.0   0.0 |
    | 0.0   1.0 |
    -------------
    -------------
    | 2.0   0.0 |
    | 0.0   2.0 |
    -------------
    -------------
    | 4.0   0.0 |
    | 0.0   4.0 |
    -------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_power_fibonacci(capsys):
    program = '''
    m = [1, 1 | 1, 0];
    print(m ^ 5); # Fibonacci matrix to the 5th power
    '''
    expected = '''
    -------------
    | 8.0   5.0 |
    | 5.0   3.0 |
    -------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_within_matrix(capsys):
    program = '''
    m1 = [1, 2 | 3, 4];
    m2 = [5, 6 | 7, 8];
    big = [m1, m2 | m2, m1];
    print(big);
    '''
    expected = '''
    ---------------------------------
    | -------------   ------------- |
    | | 1.0   2.0 |   | 5.0   6.0 | |
    | | 3.0   4.0 |   | 7.0   8.0 | |
    | -------------   ------------- |
    | -------------   ------------- |
    | | 5.0   6.0 |   | 1.0   2.0 | |
    | | 7.0   8.0 |   | 3.0   4.0 | |
    | -------------   ------------- |
    ---------------------------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_power_non_square_raises_error(capsys):
    program = '''
    m = [1, 2, 3 | 4, 5, 6];
    print(m ^ 2);
    '''
    run_neo_and_assert(program, "Error at line: 2, column: 9. Only square matrices can be raised to a power", capsys)

def test_matrix_determinant_non_square_raises_error(capsys):
    program = '''
    m = [1, 2, 3 | 4, 5, 6];
    print(m.det);
    '''
    run_neo_and_assert(program, "Error at line: 2, column: 9. Matrix must be square to calculate determinant", capsys)

