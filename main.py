from Lexer.Lexer import Lexer
from Parser.Parser import Parser


lexer = Lexer(filename="test.txt")
parser = Parser(lexer)

parsed_program = parser.parse_program()
for object in parsed_program.toplevel_objects:
    print(object)