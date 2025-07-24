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

def test_if_truthy_and_falsy_values(capsys):
    program = '''
    if([0]){
        print(0);
    }
    if([0, 0 | 0, 0 | 0, 0]){
        print(1);
    }
    if([0.1]){
        print(2);
    }
    if(""){
        print(3);
    }
    if("c"){
        print(4);
    }
    if(0){
        print(5);
    }
    if(0.1){
        print(6);
    }
    if(True){
        print(7);
    }
    if(False){
        print(8);
    }
    '''
    expected = '''
    2.0
    4.0
    6.0
    7.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_while_loop_matrix_fill(capsys):
    program = '''
    m = zeros(3, 4);
    i = 0;
    while(i < m.rowlen){
        j = 0;
        while( j < m.collen){
            m[i, j] = i * j;
            j = j+1;
        }
        i = i+1;
    }
    print(m);
    '''
    expected = '''
    -------------------------
    | 0.0   0.0   0.0   0.0 |
    | 0.0   1.0   2.0   3.0 |
    | 0.0   2.0   4.0   6.0 |
    -------------------------
    '''
    run_neo_and_assert(program, expected, capsys) 