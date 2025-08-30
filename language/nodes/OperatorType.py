from enum import Enum, auto


class OperatorType(Enum):
    LESS_OR_EQUAL = auto()
    GREATER_OR_EQUAL = auto()
    GREATER = auto()
    LESS = auto()

    EQUAL = auto()
    NOT_EQUAL = auto()

    MULTIPLY = auto()
    DIVIDE = auto()
    PLUS = auto()
    MINUS = auto()
    POWER = auto()

    AND = auto()
    OR = auto()
    NOT = auto()


to_operator_type = {
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
    '^': OperatorType.POWER,

    'and': OperatorType.AND,
    'or': OperatorType.OR,
    'not': OperatorType.NOT,
}
