from enum import Enum, auto


class OperatorType(Enum):
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    EQUAL = auto()
    NOT_EQUAL = auto()

    LESS_OR_EQUAL = auto()
    GREATER_OR_EQUAL = auto()
    GREATER = auto()
    LESS = auto()

    AND = auto()
    OR = auto()
    NOT = auto()


to_operator = {
    '<=': OperatorType.LESS_OR_EQUAL,
    '>=': OperatorType.GREATER_OR_EQUAL,
    '<': OperatorType.LESS,
    '>': OperatorType.GREATER,

    '==': OperatorType.EQUAL,
    '!=': OperatorType.NOT_EQUAL,

    '*': OperatorType.MULTIPLY,
    '/': OperatorType.DIVIDE,
    '+': OperatorType.PLUS,
    '-': OperatorType.MINUS,

    'and': OperatorType.AND,
    'or': OperatorType.OR,
    'not': OperatorType.NOT,
}
