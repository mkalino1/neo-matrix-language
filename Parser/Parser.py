from Objects.ToplevelObjects import *
from Objects.Instructions import *
from Objects.Expressions import *
from Lexer.Token import Type
from Lexer.Lexer import Lexer
from Errors.ParserExceptions import *

class Parser:
    def __init__(self, lexer:Lexer):
        self.lexer = lexer
        self.lexer.build_next_token()


    def consume(self):
        prev_token = self.lexer.token
        self.lexer.build_next_token()
        return prev_token


    def expect(self, expected_token_type):
        if not self.check_type(expected_token_type):
            raise InvalidSyntax(
                (self.lexer.token.line, self.lexer.token.column),
                expected_token_type,
                self.lexer.token.token_type,
                self.lexer.token.value
            )
        prev_token = self.lexer.token
        self.consume()
        return prev_token


    def check_type(self, token_type):
        return self.lexer.token.token_type == token_type


    def parse_program(self):
        """
        Program = { FunctionDefinition | Instruction } ;
        """
        toplevel_objects = []
        while (object := self.try_parse_function()) or (object := self.try_parse_instruction()):
            toplevel_objects.append(object)

        self.expect(Type.EOF)
        return Program(toplevel_objects)


    def try_parse_function(self):
        """
        FunctionDefinition = ‘function’ Identifier ‘(‘ [Parameters] ‘)’ BlockInstruction ;
        """
        if not self.check_type(Type.FUNCTION):
            return None
        self.consume()

        function_identifier = Identifier(self.expect(Type.IDENTIFIER).value)

        self.expect(Type.OP_ROUND_BRACKET)
        parameter_list = self.parse_parameters()
        self.expect(Type.CL_ROUND_BRACKET)

        function_block = self.parse_block()
        return Function(function_identifier, parameter_list, function_block)


    def parse_parameters(self):
        """
        Parameters = { Identifier { ‘,’ Identifier } } ;
        """
        if self.check_type(Type.CL_ROUND_BRACKET):
            return []
        parameter_list = [Identifier(self.expect(Type.IDENTIFIER).value)]
        while self.check_type(Type.COMMA):
            self.consume()
            parameter_list.append(Identifier(self.expect(Type.IDENTIFIER).value))

        return parameter_list


    def parse_arguments(self):
        """
        Arguments = { Expression { ‘,’ Expression } };
        """
        if self.check_type(Type.CL_ROUND_BRACKET):
            return []
        arguments_list = [self.parse_expression()]
        while self.check_type(Type.COMMA):
            self.consume()
            arguments_list.append(self.parse_expression())

        return arguments_list


    def try_parse_block(self):
        if not self.check_type(Type.OP_CURLY_BRACKET):
            return None
        return self.parse_block()


    def parse_block(self):
        """
        BlockInstruction = ‘{‘ {Instruction} ‘}’
        """
        self.expect(Type.OP_CURLY_BRACKET)
        instructions = []
        while not self.check_type(Type.CL_CURLY_BRACKET):
            instructions.append(self.parse_instruction())
        self.expect(Type.CL_CURLY_BRACKET)
        return Block(instructions)


    def try_parse_instruction(self):
        types_to_check = [Type.IF, Type.WHILE, Type.OP_CURLY_BRACKET, Type.RETURN, Type.IDENTIFIER]
        if any([self.check_type(t) for t in types_to_check]):
            return self.parse_instruction()
        return None


    def parse_instruction(self):
        """
        Instruction = IfStatement | Loop | Assignment | FunctionCall ";" | BlockInstruction | ReturnInstruction;
        """
        if (block_trial := self.try_parse_block()): return block_trial
        if (if_trial := self.try_parse_if()): return if_trial
        if (while_trial := self.try_parse_while()): return while_trial
        if (return_trial := self.try_parse_return()): return return_trial

        # w takim razie instrukcja powinna zaczynać się identyfikatorem
        first_identifier = Identifier(self.expect(Type.IDENTIFIER).value)

        # jesli wywołanie funkcji wystepuje jako samotna instrukcja to musi konczyc sie średnikiem
        if (funcall_trial := self.try_parse_functioncall_with_consumed_identifier(first_identifier)): 
            self.expect(Type.SEMICOLON)
            return funcall_trial
        if (assign_trial := self.try_parse_assignment_with_consumed_identifier(first_identifier)): return assign_trial

        raise InvalidSyntax(
            (self.lexer.token.line, self.lexer.token.column),
            "equal sign or left round bracket",
            self.lexer.token.token_type,
            self.lexer.token.value
        )


    def try_parse_if(self):
        """
        IfStatement = ‘if’ ‘(‘ Expression ‘)’ BlockInstruction [‘else’ BlockInstruction] ;
        """
        if not self.check_type(Type.IF):
            return None
        self.consume()

        self.expect(Type.OP_ROUND_BRACKET)
        condition_expression = self.parse_expression()
        self.expect(Type.CL_ROUND_BRACKET)

        main_block = self.parse_block()
        else_block = None
        if self.check_type(Type.ELSE):
            self.consume()
            else_block = self.parse_block()

        return IfStatement(condition_expression, main_block, else_block)


    def try_parse_while(self):
        """
        Loop = ‘while’ ‘(‘ Expression ‘)’ BlockInstruction ;
        """
        if not self.check_type(Type.WHILE):
            return None
        self.consume()

        self.expect(Type.OP_ROUND_BRACKET)
        condition_expression = self.parse_expression()
        self.expect(Type.CL_ROUND_BRACKET)

        block = self.parse_block()
        return WhileLoop(condition_expression, block)


    def try_parse_return(self):
        """
        ReturnInstruction = ‘return’ [ Expression ] ‘;’ ;
        """
        if not self.check_type(Type.RETURN):
            return None
        self.consume()
        expression = None

        if not self.check_type(Type.SEMICOLON):
            expression = self.parse_expression()

        self.expect(Type.SEMICOLON)
        return Return(expression)


    def try_parse_functioncall_with_consumed_identifier(self, first_identifier):
        """
        FunctionCall = Identifier ‘(‘ [Arguments] ‘)’ ‘;’ ;
        """
        if not self.check_type(Type.OP_ROUND_BRACKET):
            return None
        self.consume()
        arguments = self.parse_arguments()
        self.expect(Type.CL_ROUND_BRACKET)
        return FunctionCall(first_identifier, arguments)


    def try_parse_assignment_with_consumed_identifier(self, first_identifier):
        """
        Assignment = Identifier ‘=’ Expression ‘;’ ;
        """
        if not self.check_type(Type.ASSIGN):
            return None
        self.consume()
        expression = self.parse_expression()
        self.expect(Type.SEMICOLON)
        return Assignment(first_identifier, expression)


    def parse_expression(self):
        """
        Expression     = Equality ( ( "and" | "or" ) Equality )*;
        Equality       = Comparison ( "==" Comparison )* ;
        Comparison     = Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
        Term           = Factor ( ( "-" | "+" ) Factor )* ;
        Factor         = Unary ( ( "/" | "*" ) Unary )* ;
        Unary          = ( "not" | "-" ) Unary | Primary ;
        Primary        = Literal | "(" Expression ")" ; 
        Literal        = Bool | String | Scalar | Matrix | FunctionCall | ObjectProperty | MatrixAccess | Identifier; 
        """
        l_expression = self.parse_equality()

        while self.check_type(Type.AND) or self.check_type(Type.OR):
            op = self.consume().token_type
            r_expression = self.parse_equality()
            l_expression = BinaryOperator(l_expression, op, r_expression)
        return l_expression


    def parse_equality(self):
        """
        Equality       = Comparison ( "==" Comparison )* ;
        """
        l_expression = self.parse_comparison()

        while self.check_type(Type.EQUAL_TO):
            op = self.consume().token_type
            r_expression = self.parse_comparison()
            l_expression = BinaryOperator(l_expression, op, r_expression)
        return l_expression


    def parse_comparison(self):
        """
        Comparison     = Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
        """
        l_expression = self.parse_term()

        while self.check_type(Type.LESS_OR_EQUAL_TO) or self.check_type(Type.GREATER_OR_EQUAL_TO) or self.check_type(Type.CL_ANGLE_BRACKET) or self.check_type(Type.OP_ANGLE_BRACKET):
            op = self.consume().token_type
            r_expression = self.parse_term()
            l_expression = BinaryOperator(l_expression, op, r_expression)
        return l_expression


    def parse_term(self):
        """
        Term           = Factor ( ( "-" | "+" ) Factor )* ;
        """
        l_expression = self.parse_factor()

        while self.check_type(Type.PLUS) or self.check_type(Type.MINUS):
            op = self.consume().token_type
            r_expression = self.parse_factor()
            l_expression = BinaryOperator(l_expression, op, r_expression)
        return l_expression


    def parse_factor(self):
        """
        Factor         = Unary ( ( "/" | "*" ) Unary )* ;
        """
        l_expression = self.parse_unary()

        while self.check_type(Type.DIVIDE) or self.check_type(Type.MULTIPLY):
            op = self.consume().token_type
            r_expression = self.parse_unary()
            l_expression = BinaryOperator(l_expression, op, r_expression)
        return l_expression
        

    def parse_unary(self):
        """
        Unary          = ( "not" | "-" ) Unary | Primary ;
        """
        if self.check_type(Type.NOT) or self.check_type(Type.MINUS):
            op = self.consume().token_type
            right = self.parse_unary()
            return UnaryOperator(op, right)
        return self.parse_primary()


    def parse_primary(self):
        """
        Primary        = Literal | "(" Expression ")" ; 
        """
        if (grouping_trial := self.try_parse_grouping()): return grouping_trial
        if (literal_trial := self.try_parse_literal()): return literal_trial

        raise InvalidSyntax(
            (self.lexer.token.line, self.lexer.token.column),
            "literal or grouping",
            self.lexer.token.token_type,
            self.lexer.token.value
        )


    def try_parse_literal(self):
        """
        Literal = Bool | String | Scalar | Matrix | FunctionCall | ObjectProperty | MatrixAccess | Identifier;
        """
        if self.check_type(Type.BOOL): return Bool(self.consume().value)
        if self.check_type(Type.STRING): return String(self.consume().value)
        if self.check_type(Type.SCALAR): return Scalar(self.consume().value)
        if (matrix_trial := self.try_parse_matrix()): return matrix_trial
        if self.check_type(Type.IDENTIFIER):
            identifier = self.consume().value
            if (property_trial := self.try_parse_functioncall_with_consumed_identifier(identifier)): return property_trial
            if (property_trial := self.try_parse_property_with_consumed_identifier(identifier)): return property_trial
            if (access_trial := self.try_parse_access_with_consumed_identifier(identifier)): return access_trial
            return Identifier(identifier)
        return None


    def try_parse_grouping(self):
        """
        Grouping = ‘(’ Expression ‘)’
        """
        if not self.check_type(Type.OP_ROUND_BRACKET):
            return None
        self.consume()
        expression = self.parse_expression()
        self.expect(Type.CL_ROUND_BRACKET)
        return expression


    def try_parse_matrix(self):
        """
        Matrix = ‘[‘ {MatrixRow} ‘]’ ;
        """
        if not self.check_type(Type.OP_SQUARE_BRACKET):
            return None
        first_token_of_matrix = self.consume()

        rows = []
        while not self.check_type(Type.CL_SQUARE_BRACKET):
            rows.append(self.parse_matrix_row())
        self.expect(Type.CL_SQUARE_BRACKET)

        # jesli wszystkie wiersze nie maja równych długości
        if len([None for row in rows if len(row)==len(rows[0])]) != len(rows):
            raise InvalidMatrix((first_token_of_matrix.line, first_token_of_matrix.column))
        return Matrix(rows)


    def parse_matrix_row(self):
        """
        MatrixRow = ‘<’ Scalar {‘,’ Scalar } ‘>’ ;
        """
        self.expect(Type.OP_ANGLE_BRACKET)
        scalars = [Scalar(self.expect(Type.SCALAR).value)]

        while not self.check_type(Type.CL_ANGLE_BRACKET):
            self.expect(Type.COMMA)
            scalars.append(Scalar(self.expect(Type.SCALAR).value))
        self.expect(Type.CL_ANGLE_BRACKET)
        return scalars


    def try_parse_property_with_consumed_identifier(self, first_identifier):
        """
        Property = Identifier ‘.’ Identifier ‘;’ ;
        """
        if not self.check_type(Type.DOT):
            return None
        self.consume()
        second_identifier = Identifier(self.expect(Type.IDENTIFIER).value)
        return Property(first_identifier, second_identifier)


    def try_parse_access_with_consumed_identifier(self, identifier):
        """
        MatrixAccess = Identifier ‘[‘ Scalar ‘]’ ‘[‘ Scalar ‘]’
        """
        if not self.check_type(Type.OP_SQUARE_BRACKET):
            return None
        self.consume()
        first_expression = self.parse_expression()
        self.expect(Type.CL_SQUARE_BRACKET)

        self.expect(Type.OP_SQUARE_BRACKET)
        second_expression = self.parse_expression()
        self.expect(Type.CL_SQUARE_BRACKET)
        return Access(identifier, first_expression, second_expression)
