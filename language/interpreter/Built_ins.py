from language.nodes.Expressions import Matrix
from language.errors.InterpreterExceptions import NeoRuntimeError


def neo_print(line, col, *obj):
    print(*obj)


def neo_zeros(line, col, first, second=None):
    if first <= 0 or (second and second <= 0):
        raise NeoRuntimeError("Positive scalars expected", line, col)
    return Matrix([[0 for _ in range(int(second) if second else int(first))] for _ in range(int(first))], line, col)

def neo_ones(line, col, first, second=None):
    if first <= 0 or (second and second <= 0):
        raise NeoRuntimeError("Positive scalars expected", line, col)
    return Matrix([[1 for _ in range(int(second) if second else int(first))] for _ in range(int(first))], line, col)


builtin_functions = {
    "print": neo_print,
    "zeros": neo_zeros,
    "ones": neo_ones
}
