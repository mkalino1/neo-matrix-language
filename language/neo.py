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
var n = zeros(9);
var firstMatrix = [1, 2, 3 | 4, 5, 6];
var secondMatrix = [1, 2 | 3, 4 | 5, 6];
var multiplied = firstMatrix * secondMatrix;

var resultMatrix = [
  "First matrix", "Second matrix", "Multiplied", "Transposed" |
  firstMatrix, secondMatrix, multiplied, multiplied.transposed
];

print(resultMatrix);

# Fibonacci matrix to the 10th power
print([1, 1 | 1, 0] ^ 10);
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