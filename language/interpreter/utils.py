import math

from language.errors.InterpreterExceptions import NeoRuntimeError
from language.nodes.Expressions import Matrix


def check_representation_size(value, line, col, limit, active=None):
    if not isinstance(value, Matrix):
        text = str(value)
        lines = text.split("\n")
        return len(text), max(map(len, lines)), len(lines)

    if active is None:
        active = set()
    matrix_id = id(value)
    if matrix_id in active:
        raise NeoRuntimeError("Cannot print a matrix containing a circular reference", line, col)

    active.add(matrix_id)
    columns = len(value.rows[0])
    column_widths = [0] * columns
    row_heights = []
    for row in value.rows:
        row_height = 0
        for index, cell in enumerate(row):
            cell_size, cell_width, cell_height = check_representation_size(
                cell,
                line,
                col,
                limit,
                active
            )
            if cell_size > limit:
                raise NeoRuntimeError(f"Output exceeds the {limit}-character limit", line, col)
            column_widths[index] = max(column_widths[index], cell_width)
            row_height = max(row_height, cell_height)
        row_heights.append(row_height)
    active.remove(matrix_id)

    line_width = sum(column_widths) + 3 * columns + 1
    line_count = sum(row_heights) + 2
    size = line_width * line_count + line_count - 1
    if size > limit:
        raise NeoRuntimeError(f"Output exceeds the {limit}-character limit", line, col)
    return size, line_width, line_count


def check_string_concatenation_size(left, right, node, max_string_length):
    if max_string_length is None:
        return

    left_size = check_representation_size(
        left,
        node.line,
        node.column,
        max_string_length
    )[0]
    right_size = check_representation_size(
        right,
        node.line,
        node.column,
        max_string_length
    )[0]
    if left_size + right_size > max_string_length:
        raise NeoRuntimeError(
            f"String exceeds the {max_string_length}-character limit",
            node.line,
            node.column
        )


def check_matrix_dimensions(line, col, first, second):
    values = (first,) if second is None else (first, second)
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or value <= 0
        or (isinstance(value, float) and (
            not math.isfinite(value) or not value.is_integer()
        ))
        for value in values
    ):
        raise NeoRuntimeError("Matrix dimensions must be positive whole numbers", line, col)

    rows = int(first)
    columns = rows if second is None else int(second)
    return rows, columns
