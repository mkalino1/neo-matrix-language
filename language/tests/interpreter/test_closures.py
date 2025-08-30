import re
from ...interpreter.Interpreter import Interpreter
from ...parser.Parser import Parser
from ...lexer.Lexer import Lexer
from ...lexer.Source import SourceString


def run_neo_and_assert(program, expected_output, capsys):
    """Helper function to run Neo code and assert output"""
    source = SourceString(program)
    lexer = Lexer(source)
    parser = Parser(lexer)
    parsed_program = parser.parse_program()
    
    interpreter = Interpreter(parsed_program)
    interpreter.run()
    
    captured = capsys.readouterr()
    assert re.sub(r'\s+', '', captured.out) == re.sub(r'\s+', '', expected_output)


def test_basic_closure(capsys):
    """Test basic closure functionality - inner function can access outer function variables"""
    program = '''
    function outer_function(x) {
        var mut counter = 0;
        
        function inner_function() {
            counter = counter + 1;
            return x + counter;
        }
        
        return inner_function;
    }
    
    var get_next = outer_function(10);
    print("First call:", get_next());
    print("Second call:", get_next());
    print("Third call:", get_next());
    '''
    
    expected = '''
    First call: 11.0
    Second call: 12.0
    Third call: 13.0
    '''
    
    run_neo_and_assert(program, expected, capsys)
