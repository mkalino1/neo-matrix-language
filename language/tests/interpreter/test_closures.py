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
    func outer_function(x) {
        var mut counter = 0;
        
        func inner_function() {
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
    First call: 11
    Second call: 12
    Third call: 13
    '''
    
    run_neo_and_assert(program, expected, capsys)

def test_closure_multiple_instances(capsys):
    """Test factory function creating multiple independent closure instances"""
    program = '''
    func create_counter(initial_value) {
        var mut count = initial_value;
        
        func counter() {
            count = count + 1;
            return count;
        }
        
        return counter;
    }
    
    var counter1 = create_counter(0);
    var counter2 = create_counter(100);
    
    print("Counter1 first:", counter1());
    print("Counter2 first:", counter2());
    print("Counter1 second:", counter1());
    print("Counter2 second:", counter2());
    print("Counter1 third:", counter1());
    print("Counter2 third:", counter2());
    '''
    
    expected = '''
    Counter1 first: 1
    Counter2 first: 101
    Counter1 second: 2
    Counter2 second: 102
    Counter1 third: 3
    Counter2 third: 103
    '''
    
    run_neo_and_assert(program, expected, capsys)   
