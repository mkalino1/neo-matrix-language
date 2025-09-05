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

def test_matrix_determinant(capsys):
    program = '''
    var m2 = [1, 2 | 3, 4]
    var m3 = [6, 1, 1 | 4, -2, 5 | 2, 8, 7]
    print(m2.det)
    print(m3.det)
    '''
    expected = '''
    -2
    -306
    '''
    run_neo_and_assert(program, expected, capsys)


def test_matrix_arithmetic_and_equality(capsys):
    program = '''
    var m = [1, 2 | 3, 4]
    var n = [11, 22 | 33, 44]
    print(10+m*2)
    print(-10-m*2)
    '''
    expected = '''
    -----------
    | 12   14 |
    | 16   18 |
    -----------
    -------------
    | -12   -14 |
    | -16   -18 |
    -------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_copy_and_assignment(capsys):
    program = '''
    var mut m = zeros(2)
    var n = m.copy
    m[0, 0] = 5
    print(n)
    print(m)
    '''
    expected = '''
    ---------
    | 0   0 |
    | 0   0 |
    ---------
    ---------
    | 5   0 |
    | 0   0 |
    ---------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_transpose(capsys):
    program = '''
    var m = zeros(2, 3)
    var n = m.transposed
    print(n)
    print(m)
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
    var m = [2, 0 | 0, 2]
    print(m ^ 0) # Identity
    print(m ^ 1) # Itself
    print(m ^ 2) # Squared
    '''
    expected = '''
    -------------
    | 1.0   0.0 |
    | 0.0   1.0 |
    -------------
    ---------
    | 2   0 |
    | 0   2 |
    ---------
    ---------
    | 4   0 |
    | 0   4 |
    ---------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_power_fibonacci(capsys):
    program = '''
    var m = [1, 1 | 1, 0]
    print(m ^ 5) # Fibonacci matrix to the 5th power
    '''
    expected = '''
    ---------
    | 8   5 |
    | 5   3 |
    ---------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_within_matrix(capsys):
    program = '''
    var m1 = [1, 2 | 3, 4]
    var m2 = [5, 6 | 7, 8]
    var big = [m1, m2 | m2, m1]
    print(big)
    '''
    expected = '''
    -------------------------
    | ---------   --------- |
    | | 1   2 |   | 5   6 | |
    | | 3   4 |   | 7   8 | |
    | ---------   --------- |
    | ---------   --------- |
    | | 5   6 |   | 1   2 | |
    | | 7   8 |   | 3   4 | |
    | ---------   --------- |
    -------------------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_power_non_square_raises_error(capsys):
    program = '''
    var m = [1, 2, 3 | 4, 5, 6]
    print(m ^ 2)
    '''
    run_neo_and_assert(program, "Error at line: 2, column: 13. Only square matrices can be raised to a power", capsys)

def test_matrix_determinant_non_square_raises_error(capsys):
    program = '''
    var m = [1, 2, 3 | 4, 5, 6]
    print(m.det)
    '''
    run_neo_and_assert(program, "Error at line: 2, column: 13. Matrix must be square to calculate determinant", capsys)

def test_matrix_immutable_assignment(capsys):
    program = '''
    var m = zeros(2)
    m = zeros(3)
    '''
    run_neo_and_assert(program, "Error at line: 3, column: 5. Variable 'm' is immutable and cannot be assigned to", capsys)

def test_matrix_mutable_assignment(capsys):
    program = '''
    var mut m = zeros(2)
    m = zeros(3)
    print(m)
    '''
    expected = '''
    -------------
    | 0   0   0 |
    | 0   0   0 |
    | 0   0   0 |
    -------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_matrix_immutable_element_assignment(capsys):
    program = '''
    var m = zeros(2)
    m[0, 0] = 5
    '''
    run_neo_and_assert(program, "Error at line: 3, column: 5. Matrix variable 'm' is immutable and cannot be modified", capsys)

def test_matrix_mutable_element_assignment(capsys):
    program = '''
    var mut m = zeros(2)
    m[0, 0] = 5
    print(m)
    '''
    expected = '''
    ---------
    | 5   0 |
    | 0   0 |
    ---------
    '''
    run_neo_and_assert(program, expected, capsys)

