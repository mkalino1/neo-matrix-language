from Interpreter.Visitor import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceFile, SourceString

string = """
function hej(){
    return "test";
}
print(hej(), 5);
"""

source = SourceFile("program.neo")
source = SourceString(string)
lexer = Lexer(source)
parser = Parser(lexer)

parsed_program = parser.parse_program()
interpreter = Interpreter(parsed_program)

interpreter.run()