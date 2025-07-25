from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceFile, SourceString

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Pass path to Neo program to interpret", type=str)
args = parser.parse_args()

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

source = SourceString(source_string)
# source = SourceFile(args.filename)
lexer = Lexer(source)
parser = Parser(lexer)

parsed_program = parser.parse_program()
interpreter = Interpreter(parsed_program)

interpreter.run()