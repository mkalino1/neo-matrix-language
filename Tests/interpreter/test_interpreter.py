import re
import pytest
from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceString

programs_and_outputs = [
    (
        """
		function fibonnaci(n){
		   if (n <= 1){
		        return n;
		   }
		   else{
		       return fibonnaci(n-1) + fibonnaci(n-2);
		   }
		}
		print(fibonnaci(10));
        """,
        """
		55.0
        """
    ),
    (
        """
		a = 2;
		arg = 0;

		function scope(arg){
		    print(a);
		    a = 4;
		    print(a);
		    print(arg);
		}

		scope(8);
		print(arg);
        """,
        """
		2.0
		4.0
		8.0
		0.0
        """
    ),
    (
        """
		m = zeros(3, 4);
		i = 0;
		while(i < m.rowlen){
		    j = 0;
		    while( j < m.collen){
		        m[i, j] = i * j;
		        j = j+1;
		    }
		    i = i+1;
		}
		print(m);
        """,
        """
		-------------------------
		| 0.0   0.0   0.0   0.0 |
		| 0.0   1.0   2.0   3.0 |
		| 0.0   2.0   4.0   6.0 |
		-------------------------
        """
    ),
    (
        """
		function fun(arg){
		    m = [3, 2 | 3, 4];
		    i = 1;
		    while(i < m.det and 1 >= 0){
		        if(i != arg){
		            print("Not arg");
		        }
		        else{
		            print("Arg found");
		        }
		        i = i + 1;
		    }
		}
		fun(3);
        """,
        """
		Not arg
		Not arg
		Arg found
		Not arg
		Not arg
        """
    ),
    (
        """
		if([0]){
		    print(0);
		}
		if([0, 0 | 0, 0 | 0, 0]){
		    print(1);
		}
		if([0.1]){
		    print(2);
		}
		if(""){
		    print(3);
		}
		if("c"){
		    print(4);
		}
		if(0){
		    print(5);
		}
		if(0.1){
		    print(6);
		}
		if(True){
		    print(7);
		}
		if(False){
		    print(8);
		}
        """,
        """
		2.0
		4.0
		6.0
		7.0
        """
    ),
    (
        """
		m = [1, 2 | 3, 4];
		n = [11, 22 | 33, 44];

		print(10+m*2);
		print(-10-m*2);
		print(n + m == n - (-m));
        """,
        """
		---------------
		| 12.0   14.0 |
		| 16.0   18.0 |
		---------------
		-----------------
		| -12.0   -14.0 |
		| -16.0   -18.0 |
		-----------------
		True
        """
    ),
    (
        """
		m = zeros(2);
		n = m.copy;
		m[0, 0] = 5;

		print(n);
		print(m);
        """,
        """
		---------
		| 0   0 |
		| 0   0 |
		---------
		-----------
		| 5.0   0 |
		|   0   0 |
		-----------
        """
    ),
    (
        """
		m = zeros(2, 3);
		n = m.transposed;

		print(n);
		print(m);
        """,
        """
		---------
		| 0   0 |
		| 0   0 |
		| 0   0 |
		---------
		-------------
		| 0   0   0 |
		| 0   0   0 |
		-------------
        """
    ),
    (
        """
		function test(arg1, arg2){
		    print(arg1);
		    print(arg2);
		}
		test("kra"+"kow", "" or 4);
        """,
        """
		krakow
		4.0
        """
    ),
    (
        """
		function factorial(n){
		   if (n == 1){
		        return n;
		   }
		   else{
		       return n*factorial(n-1);
		   }
		}
		print(factorial(5));
        """,
        """
		120.0
        """
    ),
    (
        """
        m = [2, 0 | 0, 2];
        print(m ^ 0); # Identity
        print(m ^ 1); # Itself
        print(m ^ 2); # Squared
        """,
        """
        -------------
        | 1.0   0.0 |
        | 0.0   1.0 |
        -------------
        -------------
        | 2.0   0.0 |
        | 0.0   2.0 |
        -------------
        -------------
        | 4.0   0.0 |
        | 0.0   4.0 |
        -------------
        """
    ),
    (
        """
        m = [1, 1 | 1, 0];
        print(m ^ 5); # Fibonacci matrix to the 5th power
        """,
        """
        -------------
        | 8.0   5.0 |
        | 5.0   3.0 |
        -------------
        """
    ),
]


@pytest.mark.parametrize("program,correct_output", programs_and_outputs)
def test_interpreter_program(program, correct_output, capsys):
    source = SourceString(program)
    lexer = Lexer(source)
    parser = Parser(lexer)
    interpreter = Interpreter(parser.parse_program())
    interpreter.run()
    captured = capsys.readouterr()
    assert re.sub(r'\s+', '', captured.out) == re.sub(r'\s+', '', correct_output)