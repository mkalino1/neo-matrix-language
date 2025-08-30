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

def test_function_assignment(capsys):
    program = '''
    function add(x, y) {
        return x + y;
    }

    function multiply(x, y) {
        return x * y;
    }

    function subtract(x, y) {
        return x - y;
    }

    # Function assignment
    var my_add = add;
    var my_multiply = multiply;
    var my_subtract = subtract;

    # Double chained function assignment
    var my_my_add = my_add;

    print("add(5, 3):", add(5, 3));
    print("my_add(5, 3):", my_add(5, 3));
    print("multiply(4, 6):", multiply(4, 6));
    print("my_multiply(4, 6):", my_multiply(4, 6));
    print("my_my_add(5, 3):", my_my_add(5, 3));
    '''
    expected = '''
    add(5, 3): 8.0
    my_add(5, 3): 8.0
    multiply(4, 6): 24.0
    my_multiply(4, 6): 24.0
    my_my_add(5, 3): 8.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_reassignment(capsys):
    program = '''
    function add(x, y) {
        return x + y;
    }

    function multiply(x, y) {
        return x * y;
    }

    function subtract(x, y) {
        return x - y;
    }

    # Function reassignment
    var mut operation = add;
    print("operation(10, 5):", operation(10, 5));

    operation = multiply;
    print("After reassignment - operation(10, 5):", operation(10, 5));

    operation = subtract;
    print("After reassignment - operation(10, 5):", operation(10, 5));
    '''
    expected = '''
    operation(10, 5): 15.0
    After reassignment - operation(10, 5): 50.0
    After reassignment - operation(10, 5): 5.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_as_return_value(capsys):
    program = '''
    function add(x, y) {
        return x + y;
    }

    function multiply(x, y) {
        return x * y;
    }

    function subtract(x, y) {
        return x - y;
    }

    # Function that returns a function
    function get_operation(op_type) {
        if (op_type == "add") {
            return add;
        } else {
            if (op_type == "multiply") {
                return multiply;
            } else {
                if (op_type == "subtract") {
                    return subtract;
                }
            }
        }
    }

    var mut add_func = get_operation("add");
    var mut mult_func = get_operation("multiply");
    var mut sub_func = get_operation("subtract");

    print("add_func(8, 2):", add_func(8, 2));
    print("mult_func(8, 2):", mult_func(8, 2));
    print("sub_func(8, 2):", sub_func(8, 2));
    '''
    expected = '''
    add_func(8, 2): 10.0
    mult_func(8, 2): 16.0
    sub_func(8, 2): 6.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_with_no_parameters(capsys):
    program = '''
    function constant() {
        return 100;
    }

    var const_func = constant;
    print("Constant function:", const_func());
    '''
    expected = '''
    Constant function: 100.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_with_multiple_parameters(capsys):
    program = '''
    function complex_op(a, b, c) {
        return a * b + c;
    }

    var complex_func = complex_op;
    print("Complex operation:", complex_func(2, 3, 4));
    '''
    expected = '''
    Complex operation: 10.0
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_comparison(capsys):
    program = '''
    function test_func() {
        return 42;
    }

    var func_ref1 = test_func;
    var func_ref2 = test_func;
    var func_ref3 = func_ref1;

    print("func_ref1 == func_ref2:", func_ref1 == func_ref2);
    print("func_ref1 == func_ref3:", func_ref1 == func_ref3);
    print("func_ref1():", func_ref1());
    print("func_ref2():", func_ref2());
    print("func_ref3():", func_ref3());
    '''
    expected = '''
    func_ref1 == func_ref2: True
    func_ref1 == func_ref3: True
    func_ref1(): 42.0
    func_ref2(): 42.0
    func_ref3(): 42.0
    '''
    run_neo_and_assert(program, expected, capsys)
