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

def test_basic_scoping(capsys):
    """Test basic variable and function scoping rules"""
    program = '''
    # Global scope
    var global_var = 10;

    func global_func() {
        return global_var;
    }

    # Test basic scoping
    func test_basic_scoping() {
        var local_var = 20;

        print("Global var:", global_var);
        print("Local var:", local_var);
        print("Global func result:", global_func());
    }

    test_basic_scoping();
    '''
    expected = '''
    Global var: 10
    Local var: 20
    Global func result: 10
    '''
    run_neo_and_assert(program, expected, capsys)

def test_nested_scoping(capsys):
    """Test nested function scoping"""
    program = '''
    var global_var = 10;

    func test_nested_scoping() {
        var outer_var = 30;

        func inner_function() {
            var inner_var = 40;
            print("Inner function - outer_var:", outer_var);
            print("Inner function - inner_var:", inner_var);
            print("Inner function - global_var:", global_var);
        }

        inner_function();
        print("Outer function - outer_var:", outer_var);
    }

    test_nested_scoping();
    '''
    expected = '''
    Inner function - outer_var: 30
    Inner function - inner_var: 40
    Inner function - global_var: 10
    Outer function - outer_var: 30
    '''
    run_neo_and_assert(program, expected, capsys)

def test_shadowing(capsys):
    """Test variable shadowing in different scopes"""
    program = '''
    var shadow_var = 50;
    
    func test_shadowing() {
        var shadow_var = 60;
        print("Inside function:", shadow_var);
    }

    print("Before function call:", shadow_var);
    test_shadowing();
    print("After function call:", shadow_var);
    '''
    expected = '''
    Before function call: 50
    Inside function: 60
    After function call: 50
    '''
    run_neo_and_assert(program, expected, capsys)

def test_block_scoping(capsys):
    """Test block-level scoping"""
    program = '''
    var block_var = 100;
    
    {
        var block_var = 200;
        print("Inside block:", block_var);
    }
    
    print("Outside block:", block_var);
    '''
    expected = '''
    Inside block: 200
    Outside block: 100
    '''
    run_neo_and_assert(program, expected, capsys)

def test_scope_isolation(capsys):
    """Test that variables are isolated between different functions"""
    program = '''
    func func1() {
        var isolated_var = 70;
        print("func1:", isolated_var);
    }

    func func2() {
        var isolated_var = 80;
        print("func2:", isolated_var);
    }

    func1();
    func2();
    '''
    expected = '''
    func1: 70
    func2: 80
    '''
    run_neo_and_assert(program, expected, capsys)

def test_global_access_from_nested_scopes(capsys):
    """Test access to global variables from deeply nested scopes"""
    program = '''
    var global_var = 42;
    
    func global_func() {
        return global_var * 2;
    }

    func test_global_access() {
        func deeply_nested() {
            func even_deeper() {
                print("Deeply nested:", global_var);
                print("Deeply nested:", global_func());
            }
            even_deeper();
        }
        deeply_nested();
    }

    test_global_access();
    '''
    expected = '''
    Deeply nested: 42
    Deeply nested: 84
    '''
    run_neo_and_assert(program, expected, capsys)

def test_mutable_variable_scoping(capsys):
    """Test that mutable variables respect scoping rules"""
    program = '''
    var mut global_mut = 1;
    
    func test_mutable_scoping() {
        var mut local_mut = 10;
        print("Before modification - global_mut:", global_mut);
        print("Before modification - local_mut:", local_mut);
        
        global_mut = 2;
        local_mut = 20;
        
        print("After modification - global_mut:", global_mut);
        print("After modification - local_mut:", local_mut);
    }

    test_mutable_scoping();
    print("After function - global_mut:", global_mut);
    '''
    expected = '''
    Before modification - global_mut: 1
    Before modification - local_mut: 10
    After modification - global_mut: 2
    After modification - local_mut: 20
    After function - global_mut: 2
    '''
    run_neo_and_assert(program, expected, capsys)

def test_function_declaration_scoping(capsys):
    """Test that function declarations respect scoping rules"""
    program = '''
    func outer_func() {
        func inner_func() {
            return "inner";
        }
        return inner_func();
    }

    func test_func_scoping() {
        func inner_func() {
            return "shadowed";
        }
        print("Local inner_func result:", inner_func());
        print("Outer inner_func result:", outer_func());
    }

    test_func_scoping();
    '''
    expected = '''
    Local inner_func result: shadowed
    Outer inner_func result: inner
    '''
    run_neo_and_assert(program, expected, capsys)
