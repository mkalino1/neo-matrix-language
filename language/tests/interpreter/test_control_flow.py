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

def test_if_truthy_and_falsy_values(capsys):
    program = '''
    if([0]){
        print(0)
    }
    if([0, 0 | 0, 0 | 0, 0]){
        print(1)
    }
    if([0.1]){
        print(2)
    }
    if(""){
        print(3)
    }
    if("c"){
        print(4)
    }
    if(0){
        print(5)
    }
    if(0.1){
        print(6)
    }
    if(True){
        print(7)
    }
    if(False){
        print(8)
    }
    '''
    expected = '''
    2
    4
    6
    7
    '''
    run_neo_and_assert(program, expected, capsys)

def test_while_loop_matrix_fill(capsys):
    program = '''
    var mut m = zeros(3, 4)
    var mut i = 0
    while(i < m.rowlen){
        var mut j = 0
        while( j < m.collen){
            m[i, j] = i * j
            j = j+1
        }
        i = i+1
    }
    print(m)
    '''
    expected = '''
    -----------------
    | 0   0   0   0 |
    | 0   1   2   3 |
    | 0   2   4   6 |
    -----------------
    '''
    run_neo_and_assert(program, expected, capsys)

def test_var_declaration_and_assignment(capsys):
    # Mutable variable: reassignment should work
    program = '''
    var mut x = 5
    print(x)
    x = 10
    print(x)
    '''
    expected = '''
    5
    10
    '''
    run_neo_and_assert(program, expected, capsys)

def test_var_redeclaration_error(capsys):
    program = '''
    var x = 1
    var x = 2
    '''
    run_neo_and_assert(program, "Error at line: 3, column: 5. Variable 'x' already declared in this scope", capsys)

def test_var_reassignment_error(capsys):
    program = '''
    var x = 1
    x = 2
    '''
    run_neo_and_assert(program, "Error at line: 3, column: 5. Variable 'x' is immutable and cannot be assigned to", capsys)