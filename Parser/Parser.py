from os import terminal_size
from Objects.Objects import *
from Lexer.Token import Type
from Lexer.Lexer import Lexer
from Exceptions import *

class Parser:
    def __init__(self, lexer:Lexer):
        self.lexer = lexer
        self.lexer.build_next_token()


    def expect(self, expected_token_type):
        if self.lexer.token.token_type != expected_token_type:
            raise InvalidSyntax(
                (self.lexer.token.line, self.lexer.token.column),
                expected_token_type,
                self.lexer.token.token_type,
                self.lexer.token.value
            )
        prev_token = self.lexer.token
        self.lexer.build_next_token()
        return prev_token


    def check_type(self, token_type):
        return self.lexer.token.token_type == token_type


    def parse_program(self):
        """Specyfikacja składni:
        Program = { FunctionDefinition | Instruction } ;
        """
        toplevel_objects = []

        while parsed_object := self.try_parse_function():     # or (parsed_object := self.parse_instruction)
            toplevel_objects.append(parsed_object)
            self.start_of_object_pos = (self.lexer.token.line, self.lexer.token.column)

        self.expect(Type.EOF)
        return Program(toplevel_objects)


    def try_parse_function(self):
        """Specyfikacja składni:
        FunctionDefinition = ‘function’ Identifier ‘(‘ [Parameters] ‘)’ BlockInstruction ;
        """
        if self.lexer.token.token_type != Type.FUNCTION:
            return None
        self.lexer.build_next_token()

        function_identifier = Identifier(self.expect(Type.IDENTIFIER).value)

        self.expect(Type.OP_ROUND_BRACKET)
        parameter_list = self.parse_parameters()
        self.expect(Type.CL_ROUND_BRACKET)

        function_block = self.parse_block()

        return Function(function_identifier, parameter_list, function_block)


    def parse_parameters(self):
        """Specyfikacja składni:
        Parameters = Identifier { ‘,’ Identifier } ;
        """
        if self.lexer.token.token_type == Type.CL_ROUND_BRACKET:
            return []

        parameter_list = [Identifier(self.expect(Type.IDENTIFIER).value)]

        while self.lexer.token.token_type == Type.COMMA:
            self.lexer.build_next_token()
            parameter_list.append(Identifier(self.expect(Type.IDENTIFIER).value))

        return parameter_list


    def try_parse_block(self):
        if self.lexer.token.token_type != Type.OP_CURLY_BRACKET:
            return None
        return self.parse_block()


    def parse_block(self):
        """Specyfikacja składni:
        BlockInstruction = ‘{‘ {Instruction} ‘}’
        """
        self.expect(Type.OP_CURLY_BRACKET)
        instructions = []
        while not self.check_type(Type.CL_CURLY_BRACKET):
            instructions.append(self.parse_instruction())
        self.expect(Type.CL_CURLY_BRACKET)
        return Block(instructions)


    def parse_instruction(self):
        """Specyfikacja składni:
        Instruction = IfStatement | Loop | Assignment | MethodCall | FunctionCall | BlockInstruction | ReturnInstruction;
        """
        block_try = self.try_parse_block()
        if block_try != None: return block_try

        if_try = self.try_parse_if()
        if if_try != None: return if_try

        while_try = self.try_parse_while()
        if while_try != None: return while_try

        return_try = self.try_parse_return()
        if return_try != None: return return_try

        # TODO: Assignment | MethodCall | FunctionCall

        # return None
        raise Exception("Nieznana instrukcja")


    def try_parse_if(self):
        """Specyfikacja składni:
        IfStatement = ‘if’ ‘(‘ Expression ‘)’ BlockInstruction [‘else’ BlockInstruction] ;
        """
        if self.lexer.token.token_type != Type.IF:
            return None
        self.lexer.build_next_token()

        self.expect(Type.OP_ROUND_BRACKET)
        condition_expression = self.parse_expression()
        self.expect(Type.CL_ROUND_BRACKET)

        main_block = self.parse_block()
        else_block = None
        if self.lexer.token.token_type == Type.ELSE:
            self.lexer.build_next_token()
            else_block = self.parse_block()

        return IfStatement(condition_expression, main_block, else_block)


    def try_parse_while(self):
        """Specyfikacja składni:
        Loop = ‘while’ ‘(‘ Expression ‘)’ BlockInstruction ;
        """
        if self.lexer.token.token_type != Type.WHILE:
            return None
        self.lexer.build_next_token()

        self.expect(Type.OP_ROUND_BRACKET)
        condition_expression = self.parse_expression()
        self.expect(Type.CL_ROUND_BRACKET)

        block = self.parse_block()
        return WhileLoop(condition_expression, block)


    def try_parse_return(self):
        """Specyfikacja składni:
        ReturnInstruction = ‘return’ [ Expression ] ‘;’ ;
        """
        if self.lexer.token.token_type != Type.RETURN:
            return None
        self.lexer.build_next_token()
        expression = None

        if not self.check_type(Type.SEMICOLON):
            expression = self.parse_expression()

        self.expect(Type.SEMICOLON)
        return Return(expression)


    def parse_expression(self):
        return Scalar(self.expect(Type.SCALAR).value)

        # TODO: Dokonczyc expression. Trzeba bedzie to jakos podzielic
        
        # if self.check_type(Type.SCALAR): return Scalar(self.expect(Type.SCALAR).value)

