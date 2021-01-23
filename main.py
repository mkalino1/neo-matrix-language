from Interpreter.Visitor import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser

lexer = Lexer(filename="program.neo")
parser = Parser(lexer)

parsed_program = parser.parse_program()
interpreter = Interpreter(parsed_program)

# for object in parsed_program.toplevel_objects:
#     print(object)

print(interpreter.run())