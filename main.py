from Lexer.Lexer import Lexer


lexer_function = Lexer(filename="test_program.txt")

for token in lexer_function.yield_tokens():
    print(token)