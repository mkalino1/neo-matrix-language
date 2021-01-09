from Lexer.Lexer import Lexer


lexer = Lexer(filename="test_program.txt")

for token in lexer.yield_tokens():
    print(token)