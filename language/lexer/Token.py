from enum import Enum, auto


class TokenType(Enum):
    EOF = auto()
    IDENTIFIER = auto()
    VAR_DECLARATION = auto()
    MUT = auto()

    SCALAR = auto()
    BOOL = auto()
    STRING = auto()

    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    ASSIGN = auto()

    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    DELIMITER = auto()

    OP_ROUND_BRACKET = auto()
    CL_ROUND_BRACKET = auto()
    OP_SQUARE_BRACKET = auto()
    CL_SQUARE_BRACKET = auto()
    OP_CURLY_BRACKET = auto()
    CL_CURLY_BRACKET = auto()
    OP_ANGLE_BRACKET = auto()
    CL_ANGLE_BRACKET = auto()

    LESS_OR_EQUAL_TO = auto()
    GREATER_OR_EQUAL_TO = auto()
    EQUAL_TO = auto()
    NOT_EQUAL_TO = auto()

    AND = auto()
    OR = auto()
    NOT = auto()
    FUNCTION = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()


class Symbol:
    special_characters = {
        '(': TokenType.OP_ROUND_BRACKET,
        ')': TokenType.CL_ROUND_BRACKET,
        '[': TokenType.OP_SQUARE_BRACKET,
        ']': TokenType.CL_SQUARE_BRACKET,
        '{': TokenType.OP_CURLY_BRACKET,
        '}': TokenType.CL_CURLY_BRACKET,
        '<': TokenType.OP_ANGLE_BRACKET,
        '>': TokenType.CL_ANGLE_BRACKET,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '^': TokenType.POWER,
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '=': TokenType.ASSIGN,
        '|': TokenType.DELIMITER
    }

    double_operators = {
        '<=': TokenType.LESS_OR_EQUAL_TO,
        '>=': TokenType.GREATER_OR_EQUAL_TO,
        '==': TokenType.EQUAL_TO,
        '!=': TokenType.NOT_EQUAL_TO
    }

    reserved_words = {
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'var': TokenType.VAR_DECLARATION,
        'mut': TokenType.MUT,
        'True': TokenType.BOOL,
        'False': TokenType.BOOL,
        'return': TokenType.RETURN,
        'function': TokenType.FUNCTION,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE
    }


class Token:
    def __init__(self, token_type=None, value="", line=None, column=None):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.token_type}\t\tvalue='{self.value}'\t\tposition=({self.line}, {self.column})"

    def set_position(self, position):
        self.line = position[0]
        self.column = position[1]
