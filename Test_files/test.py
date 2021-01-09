from Lexer.Lexer import Lexer
from Lexer.Token import Type


# TESTOWANIE PRAWIDLOWYCH WARTOSCI TOKENOW
lexer_values = Lexer(filename="test_values.txt")

correct_scalars_zeros = [0, 0.0, 0.0, 0.0, 0.001, 0.4]
correct_strings = ['Kiedy powiem sobie "dosc"', 'Rozne znaki: %$#@,.()']
correct_scalars = iter(correct_scalars_zeros + correct_strings + [''])

for token in lexer_values.yield_tokens():
    print(token.value)
    assert token.value == next(correct_scalars)


# TESTOWANIE PRAWIDLOWYCH TYPOW TOKENOW
lexer_token_types = Lexer(filename="test_types.txt")

correct_doubles = [Type.GREATER_OR_EQUAL_TO, Type.LESS_OR_EQUAL_TO, Type.NOT_EQUAL_TO, Type.EQUAL_TO]
correct_booleans = [Type.BOOL, Type.BOOL]
correct_scalars = iter(correct_doubles+ correct_booleans + [Type.EOF])

for token in lexer_token_types.yield_tokens():
    print(token.token_type)
    assert token.token_type == next(correct_scalars)


print('Ok! Wszystkie testy zaliczone')