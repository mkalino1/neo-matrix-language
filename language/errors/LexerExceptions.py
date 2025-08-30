class ErrorCode:
    EXCEED_MAX_IDENTIFIER_LENGHT = 'Exceeded max length of an identifier'
    EXCEED_MAX_STRING_LENGHT = 'Exceeded max length of a string'
    STRING_BUILD_FAIL = 'Failed to build a string. No matching right quotation mark'
    CANT_IDENTIFY_TOKEN = 'Cant identify token. There is no match'

class LexerError(Exception):
    def __init__(self, error_code, position, char):
        self.message = f'{error_code}. Error at line: {position[0]}, column: {position[1]}. Char: {char}'
        super().__init__(self.message)
