from ...interpreter.Interpreter import Interpreter
from ...lexer.Lexer import Lexer
from ...lexer.Source import SourceString
from ...parser.Parser import Parser


def run_limited(program, **limits):
    parsed_program = Parser(Lexer(SourceString(program))).parse_program()
    interpreter = Interpreter(parsed_program, **limits)
    succeeded = interpreter.run()
    return succeeded, interpreter.error


def test_execution_step_limit_stops_infinite_loop(capsys):
    succeeded, error = run_limited(
        "while(True) { var value = 1 }",
        max_steps=20
    )

    assert not succeeded
    assert "Execution step limit exceeded" in str(error)
    assert "Execution step limit exceeded" in capsys.readouterr().out


def test_string_growth_is_limited_before_allocation(capsys):
    succeeded, error = run_limited(
        'var mut value = "123456"\nvalue = value + value',
        max_string_length=10
    )

    assert not succeeded
    assert "String exceeds the 10-character limit" in str(error)
    capsys.readouterr()
