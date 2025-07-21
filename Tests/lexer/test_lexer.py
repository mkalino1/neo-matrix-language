import pytest
from Lexer.Lexer import Lexer
from Lexer.Token import TokenType
from Lexer.Source import SourceFile

def test_lexer_token_values():
    expected = [
        0, 0.0, 0.0, 0.0, 0.001, 0.4,
        'String with inner "string"',
        'Random chars: %$#@,.()'
    ]
    lexer = Lexer(SourceFile("./Tests/lexer/inputs/test_values.neo"))
    tokens = list(lexer.yield_tokens())
    for token, value in zip(tokens, expected):
        assert token.value == value, f"Token value {token.value!r} != expected {value!r}"

def test_lexer_token_types():
    expected = [
        TokenType.GREATER_OR_EQUAL_TO,
        TokenType.LESS_OR_EQUAL_TO,
        TokenType.NOT_EQUAL_TO,
        TokenType.EQUAL_TO,
        TokenType.BOOL,
        TokenType.BOOL,
        TokenType.EOF
    ]
    lexer = Lexer(SourceFile("./Tests/lexer/inputs/test_types.neo"))
    tokens = list(lexer.yield_tokens())
    token_types = [token.token_type for token in tokens[:len(expected)]]
    assert token_types == expected, f"Token types {token_types} != expected {expected}"

def test_lexer_program():
    expected_types = [
        TokenType.FUNCTION, TokenType.IDENTIFIER, TokenType.OP_ROUND_BRACKET, TokenType.BOOL, TokenType.COMMA,
        TokenType.STRING, TokenType.CL_ROUND_BRACKET, TokenType.OP_CURLY_BRACKET, TokenType.VAR_DECLARATION,
        TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.SCALAR, TokenType.SEMICOLON, TokenType.RETURN,
        TokenType.IDENTIFIER, TokenType.SEMICOLON, TokenType.CL_CURLY_BRACKET, TokenType.MINUS, TokenType.SCALAR,
        TokenType.SEMICOLON, TokenType.EOF
    ]
    lexer = Lexer(SourceFile("./Tests/lexer/inputs/test_program.neo"))
    tokens = list(lexer.yield_tokens())
    token_types = [token.token_type for token in tokens]
    assert token_types == expected_types, f"Token types {token_types} != expected {expected_types}"