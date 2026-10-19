from .interpreter.Interpreter import Interpreter
from .lexer.Lexer import Lexer
from .parser.Parser import Parser
from .lexer.Source import SourceFile, SourceString
from .errors.InterpreterExceptions import NeoRuntimeError
from .errors.LexerExceptions import LexerError
from .errors.ParserExceptions import EmptyMatrix, InvalidMatrix, InvalidSyntax

import argparse
import sys


def main(argv=None):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "filename",
        nargs="?",
        help="Pass path to Neo program to interpret (optional)",
        type=str
    )
    args = argument_parser.parse_args(argv)

    # Default source string if no filename provided
    source_string = """
    func greet() {
        return "Hello, I am Neo! Provide script path and I will run it."
    }

    greet |> print
    """

    source = None
    try:
        source = SourceFile(args.filename) if args.filename else SourceString(source_string)
        lexer = Lexer(source)
        parser = Parser(lexer)

        parsed_program = parser.parse_program()
        interpreter = Interpreter(parsed_program)

        if not interpreter.run(error_stream=sys.stderr):
            return 1
        return 0
    except (NeoRuntimeError, LexerError, EmptyMatrix, InvalidMatrix, InvalidSyntax, OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        if isinstance(source, SourceFile):
            source.close()


if __name__ == "__main__":
    raise SystemExit(main())