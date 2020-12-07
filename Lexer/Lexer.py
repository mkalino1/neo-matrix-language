from .Source import Source
from .Token import Token, Symbol, Type
from Error import ErrorCode, LexerError

MEX_IDENTIFIER_LENGHT = 100
MAX_STRING_LENGHT = 500

class Lexer:
    def __init__(self, filename):
        self.source = Source(filename)
        self.token = None


    def yield_tokens(self):
        eof_reached = False
        while(not eof_reached):
            self.build_next_token()
            yield self.token
            if self.token.token_type == Type.EOF:
                eof_reached = True


    def build_next_token(self):
        while self.skip_comment() or self.skip_whitespace():
            pass

        position = self.source.current_line, self.source.current_column

        if self.try_build_eof():
            pass
        elif self.try_build_identifier_or_reserved_word(position):
            pass
        elif self.try_build_string(position):
            pass
        elif self.try_build_scalar():
            pass        
        elif self.try_build_double_operator():
            pass
        elif self.try_build_special_character():
            pass
        else:
            raise LexerError(ErrorCode.CANT_IDENTIFY_TOKEN, position)

        self.token.set_position(position)


    def try_build_eof(self):
        if self.source.current_char == '':
            self.token = Token(Type.EOF, '')
            return True
        return False


    def try_build_identifier_or_reserved_word(self, position):
        word = ''
        if self.source.current_char.isalpha():
            while self.source.current_char.isalpha() or self.source.current_char.isdigit() or self.source.current_char == '_':
                word = word + self.source.current_char
                if len(word) > MEX_IDENTIFIER_LENGHT:
                    raise LexerError(ErrorCode.EXCEED_MAX_IDENTIFIER_LENGHT, position)
                self.source.move_to_next_char()
            if word in Symbol.reserved_words:
                token_type = Symbol.reserved_words[word]
                self.token = Token(token_type, word)
                return True
            else:
                self.token = Token(Type.IDENTIFIER, word)
                return True
        return False


    def try_build_scalar(self):
        if not self.source.current_char.isdigit() and not self.source.current_char == '-':
            return False

        buffer = ''
        if self.source.current_char == '-':         # obsluga minusowych liczb
            buffer = '-'
            if not self.source.move_to_next_char().isdigit():
                self.token = Token(Type.MINUS, value='-')
                return True

        if self.source.current_char == '0':         # obsluga liczb zaczynajacych sie od zera
            buffer += '0'
            self.source.move_to_next_char()
            while self.source.current_char == '0':  # ignorowanie nadmiarowych zer 
                self.source.move_to_next_char()
            self.check_dot(buffer)
            return True

        while self.source.current_char.isdigit():   # obsluga pozostalych liczb
            buffer += self.source.current_char
            self.source.move_to_next_char()
        self.check_dot(buffer)
        return True


    def check_dot(self, buffer):            # metoda pomocnicza
        if self.source.current_char == '.':
            buffer += self.source.current_char
            self.source.move_to_next_char()
            while self.source.current_char.isdigit():
                buffer += self.source.current_char
                self.source.move_to_next_char()

            self.token = Token(Type.SCALAR, float(buffer))  # to jest poprawna liczba z kropką - po kropce moze nic nie byc
            return                     

        self.token = Token(Type.SCALAR, int(buffer))        # to jest poprawna liczba bez kropki
        return                         


    def try_build_special_character(self):
        if self.source.current_char in Symbol.special_characters:
            token_type = Symbol.special_characters[self.source.current_char]
            self.token = Token(token_type, self.source.current_char, self.source.current_line, self.source.current_column)
            self.source.move_to_next_char()
            return True
        return False


    def try_build_double_operator(self):
        first_char = self.source.current_char
        if first_char == ">" or first_char == "<" or first_char == "=" or first_char == "!":
            second_char = self.source.move_to_next_char()
            if first_char + second_char in Symbol.double_operators:
                token_type = Symbol.double_operators[first_char + second_char]
                self.token = Token(token_type, first_char + second_char)
                self.source.move_to_next_char()
                return True
            elif first_char in Symbol.special_characters:
                token_type = Symbol.special_characters[first_char]
                self.token = Token(token_type, first_char)
                return True
        return False


    def try_build_string(self, position):
        if self.source.current_char != '"':
            return False

        self.source.move_to_next_char()
        chars = []
        while self.source.current_char != '"':
            if self.source.current_char == '':
                raise LexerError(ErrorCode.STRING_BUILD_FAIL, position)

            if len(chars) > MAX_STRING_LENGHT:
                raise LexerError(ErrorCode.EXCEED_MAX_STRING_LENGHT, position)

            if self.source.current_char == '\\':
                self.source.move_to_next_char()
                if self.source.current_char == '\\':
                    chars.append('\\')
                elif self.source.current_char == '"':
                    chars.append('"')
            else:
                chars.append(self.source.current_char)
            self.source.move_to_next_char()

        self.source.move_to_next_char()

        self.token = Token(Type.STRING, ''.join(chars))
        return True


    def skip_comment(self):
        if self.source.current_char == '#':
            while self.source.current_char != '\n' and self.source.current_char != '':
                self.source.move_to_next_char()
            self.source.move_to_next_char()
            return True
        return False


    def skip_whitespace(self):
        if self.source.current_char == ' ' or self.source.current_char == '\n':
            while self.source.current_char == ' ' or self.source.current_char == '\n':
                self.source.move_to_next_char()
            return True
        return False