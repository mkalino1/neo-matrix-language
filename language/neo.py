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
func create_adder(base) {
    func add(value) {
        return base + value;
    }
    return add;
}
var adder = create_adder(10);
print(adder(5));
print(adder(7));
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