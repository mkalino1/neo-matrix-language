class NeoRuntimeError(Exception):
    def __init__(self, problem, line = None, column = None):
        message = f'Error at line: {line}, column: {column}. {problem}'
        super().__init__(message)