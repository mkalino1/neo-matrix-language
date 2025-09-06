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

def test_recursive_fibonacci(capsys):
    program = '''
    func fibonnaci(n){
       if (n <= 1){
            return n
       }
       else{
           return fibonnaci(n-1) + fibonnaci(n-2)
       }
    }
    print(fibonnaci(10))
    '''
    expected = '''
    55
    '''
    run_neo_and_assert(program, expected, capsys)

def test_recursive_factorial(capsys):
    program = '''
    func factorial(n){
       if (n == 1){
            return n
       }
       else{
           return n*factorial(n-1)
       }
    }
    print(factorial(5))
    '''
    expected = '''
    120
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_scope_and_shadowing(capsys):
    program = '''
    var mut a = 2
    var arg = 0
    func scope(arg){
        print(a)
        a = 4
        print(a)
        print(arg)
    }
    scope(8)
    print(arg)
    '''
    expected = '''
    2
    4
    8
    0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_scope_reassignment_error(capsys):
    program = '''
    var a = 2
    func scope(){
        a = 4
    }
    scope()
    '''
    run_neo_and_assert(program, "Error at line: 4, column: 9. Variable 'a' is immutable and cannot be assigned to", capsys)

def test_function_call_with_expression_args(capsys):
    program = '''
    func test(arg1, arg2){
        print(arg1)
        print(arg2)
    }
    test("kra"+"kow", "" or 4)
    '''
    expected = '''
    krakow
    4
    '''
    run_neo_and_assert(program, expected, capsys)
    
def test_anonymous_function_basic_assignment(capsys):
    """Test basic anonymous function assignment and execution"""
    program = '''
    var add = func(x, y) {
        return x + y
    }
    print(add(5, 3))
    '''
    expected = '''
    8
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_no_parameters(capsys):
    """Test anonymous function with no parameters"""
    program = '''
    var get_answer = func() {
        return 42
    }
    print(get_answer())
    '''
    expected = '''
    42
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_closure(capsys):
    """Test anonymous function closure behavior"""
    program = '''
    func create_counter() {
        var mut count = 0
        return func() {
            count = count + 1
            return count
        }
    }
    
    var counter1 = create_counter()
    var counter2 = create_counter()
    
    print(counter1())
    print(counter1())
    print(counter1())
    print(counter2())
    print(counter2())
    '''
    expected = '''
    1
    2
    3
    1
    2
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_nested(capsys):
    """Test nested anonymous functions"""
    program = '''
    var add_one = func(x) {
        return func(y) {
            return x + y
        }
    }
    
    var add_to_five = add_one(5)
    var result = add_to_five(3)
    print(result)
    '''
    expected = '''
    8
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_with_side_effects(capsys):
    """Test anonymous function with side effects"""
    program = '''
    var mut global_var = 0
    
    var modify_global = func(value) {
        global_var = value
        return global_var
    }
    
    print(modify_global(42))
    print(global_var)
    '''
    expected = '''
    42
    42
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_immediate_execution(capsys):
    """Test immediately invoked anonymous function (IIFE)"""
    program = '''
    var result = func(x, y) {
        return x * y
    }(6, 7)
    print(result)
    '''
    expected = '''
    42
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_recursive(capsys):
    """Test recursive anonymous function"""
    program = '''
    var factorial = func(n) {
        if (n <= 1) {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }
    
    print(factorial(5))
    '''
    expected = '''
    120
    '''
    run_neo_and_assert(program, expected, capsys)

def test_anonymous_function_inline_argument(capsys):
    """Test anonymous function for simple processing"""
    program = '''
    func process_numbers(a, b, c, processor) {
        return processor(a) + processor(b) + processor(c)
    }
    
    var sum = process_numbers(1, 2, 3, func(x) { return x })
    var squares = process_numbers(1, 2, 3, func(x) { return x * x })
    
    print(sum)
    print(squares)
    '''
    expected = '''
    6
    14
    '''
    run_neo_and_assert(program, expected, capsys) 