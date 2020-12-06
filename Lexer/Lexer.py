from .Source import Source
from .Token import Token, Symbol, Type


class Lexer:
    def __init__(self, filename):
        self.source = Source(filename)
        self.token = None


    def build_tokens(self):
        eof_reached = False
        while(not eof_reached):
            self.build_next_token()
            print(self.token)
            if self.token != None and self.token.token_type == Type.EOF:
                eof_reached = True


    def build_next_token(self):
        while self.skip_comment() or self.skip_whitespace():
            pass

        if self.try_build_eof():
            return
        elif self.try_build_identifier():
            return
        elif self.try_build_scalar():
            return
        elif self.try_build_special_character():
            return
        else:
            self.token = Token(Type.UNIDENTIFIED, self.source.get_char())
            self.source.get_next_char()
            return

        # elif self.try_double_operator():
        #     return

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


    def try_build_eof(self):
        if self.source.current_char == '':
            self.token = Token(Type.EOF, '', self.source.current_line, self.source.current_column)
            return True
        return False


    def try_build_identifier(self):
        word = ''
        position = self.source.current_line, self.source.current_column
        if self.source.current_char.isalpha():
            while self.source.current_char.isalpha() or self.source.current_char.isdigit() or self.source.current_char == '_':
                word = word + self.source.current_char
                self.source.move_to_next_char()
            if word in Symbol.special_words:
                token_type = Symbol.special_words[word]
                self.token = Token(token_type, word, position[0], position[1])
                return True
            else:
                self.token = Token(Type.IDENTIFIER, word, position[0], position[1])
                return True
        return False


    def try_build_scalar(self):
        # TODO: Dodac obsluge minusow
        if not self.source.current_char.isdigit():
            return False

        buffer = ''
        position = self.source.current_line, self.source.current_column

        if self.source.current_char == '0':         # obsluga liczb zaczynajacych sie od zera
            buffer += '0'
            self.source.move_to_next_char()
            return self.__check_dot(buffer, position)

        while self.source.current_char.isdigit():   # obsluga pozostalych liczb
            buffer += self.source.current_char
            self.source.move_to_next_char()
        return self.__check_dot(buffer, position)

    def __check_dot(self, buffer, position):
        if self.source.current_char == '.':
            buffer += self.source.current_char
            self.source.move_to_next_char()
            if self.source.current_char.isdigit():
                while self.source.current_char.isdigit():
                    buffer += self.source.current_char
                    self.source.move_to_next_char()

            self.token = Token(Type.SCALAR, float(buffer), position[0], position[1])
            return True                     # to jest poprawna liczba z kropką - po kropce moze nic nie byc

        self.token = Token(Type.SCALAR, int(buffer), position[0], position[1])
        return True                         # to jest poprawna liczba bez kropki

    def try_build_special_character(self):
        if self.source.current_char in Symbol.special_characters:
            token_type = Symbol.special_characters[self.source.current_char]
            self.token = Token(token_type, self.source.current_char, self.source.current_line, self.source.current_column)
            self.source.move_to_next_char()
            return True
        return False


