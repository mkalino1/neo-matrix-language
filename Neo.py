from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceFile, SourceString

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Pass path to Neo program to interpret", type=str)
args = parser.parse_args()

source_string = """
n = zeros(9);
matrix1 = [1, 2, 3 | 4, 5, 6];
matrix2 = [7, 8 | 9, 10 | 11, 12];
matrix3 = matrix1 * matrix2;

print("Matrix1: ");
print(matrix1);

print("Matrix2: ");
print(matrix2);

print("Matrix3: ");
print(matrix3);

print("Determinant of matrix3: ", matrix3.det);
"""

source = SourceString(source_string)
# source = SourceFile(args.filename)
lexer = Lexer(source)
parser = Parser(lexer)

parsed_program = parser.parse_program()
interpreter = Interpreter(parsed_program)

interpreter.run()