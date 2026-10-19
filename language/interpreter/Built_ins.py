from language.nodes.Expressions import Matrix
from language.errors.InterpreterExceptions import NeoRuntimeError
from language.interpreter.utils import check_matrix_dimensions, check_representation_size


def neo_print(line, col, *obj, max_output_length=None):
    if max_output_length is not None:
        output_size = sum(
            check_representation_size(value, line, col, max_output_length)[0]
            for value in obj
        ) + max(0, len(obj) - 1) + 1
        if output_size > max_output_length:
            raise NeoRuntimeError(
                f"Output exceeds the {max_output_length}-character limit",
                line,
                col
            )
    print(*obj)


def neo_zeros(line, col, first, second=None):
    rows, columns = check_matrix_dimensions(line, col, first, second)
    return Matrix([[0 for _ in range(columns)] for _ in range(rows)], line, col)


def neo_ones(line, col, first, second=None):
    rows, columns = check_matrix_dimensions(line, col, first, second)
    return Matrix([[1 for _ in range(columns)] for _ in range(rows)], line, col)


builtin_functions = {
    "print": neo_print,
    "zeros": neo_zeros,
    "ones": neo_ones
}
