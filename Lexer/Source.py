class Source():
    def __init__(self, filename):
        self.file = open(filename, 'r')

        self.current_line = 1
        self.current_column = 0
        
        self.current_char = self.move_to_next_char()

    def __del__(self):
        self.file.close()

    def move_to_next_char(self):
        self.current_char = self.file.read(1)

        self.current_column += 1

        if self.current_char == '\n':
            self.current_line += 1
            self.current_column = 0

        return self.current_char