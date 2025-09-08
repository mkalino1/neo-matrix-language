from .interpreter.Interpreter import Interpreter
from .lexer.Lexer import Lexer
from .parser.Parser import Parser
from .lexer.Source import SourceFile, SourceString

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", help="Pass path to Neo program to interpret (optional)", type=str)
args = parser.parse_args()

# Default source string if no filename provided
source_string = """
func greet(name) {
    return "Hello, " + name
}

"World" |> greet |> print
"""

# Use SourceFile if filename provided, otherwise use SourceString
if args.filename:
    source = SourceFile(args.filename)
else:
    source = SourceString(source_string)
lexer = Lexer(source)
parser = Parser(lexer)

parsed_program = parser.parse_program()
interpreter = Interpreter(parsed_program)

interpreter.run()