class InvalidSyntax(Exception):
    def __init__(self, position=(0, 0), expected_type=None, given_type=None, given_value=None):
        self.position = position
        self.expected_type = expected_type
        self.given_type = given_type
        self.given_value = given_value
        self.message = f'Error at line: {position[0]}, column: {position[1]}. Expected {expected_type}, got {given_type} with value "{given_value}"'
        super().__init__(self.message)


class InvalidMatrix(Exception):
    def __init__(self, position=(0, 0)):
        self.position = position
        self.message = f'Error at line: {position[0]}, column: {position[1]}. Matrix rows must be the same length'
        super().__init__(self.message)


class EmptyMatrix(Exception):
    def __init__(self, position=(0, 0)):
        self.position = position
        self.message = f'Error at line: {position[0]}, column: {position[1]}. Matrix cannot be empty'
        super().__init__(self.message)


class InvalidFilename(Exception):
    def __init__(self, filename):
        self.filename = filename
        self.message = f'{filename} does not exist'
        super().__init__(self.message)
