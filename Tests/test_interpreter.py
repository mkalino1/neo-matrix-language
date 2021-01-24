from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceString
import sys
import io
old_stdout = sys.stdout # Memorize the default stdout stream

programs = []
correct_outputs = []


################# FIBBONACCI TEST ##################
programs.append("""
function fibonnaci(n){
   if (n <= 1){
        return n;
   }
   else{
       return fibonnaci(n-1) + fibonnaci(n-2);
   }
}
print(fibonnaci(10));
""")
correct_outputs.append("""55.0
""")


################# SCOPE TEST ##################
programs.append("""
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
""")
correct_outputs.append("""2.0
4.0
8.0
0.0
""")


################# WHILE TEST ##################
programs.append("""
m = zeros(3, 4);
i = 0;
while(i < m.rowlen){
    j = 0;
    while( j < m.collen){
        m[i][j] = i * j;
        j = j+1;
    }
    i = i+1;
}
print(m);
""")
correct_outputs.append("""[0.0, 0.0, 0.0, 0.0]
[0.0, 1.0, 2.0, 3.0]
[0.0, 2.0, 4.0, 6.0]
""")


################# IF ELSE WHILE TEST ##################
programs.append("""
function fun(arg){
    m = [[3, 2][3, 4]];
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
""")
correct_outputs.append("""Not arg
Not arg
Arg found
Not arg
Not arg
""")


################# TRUTHY TEST ##################
programs.append("""
if([[0]]){
    print(0);
}
if([[0, 0][0, 0][0, 0]]){
    print(1);
}
if([[0.1]]){
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
""")
correct_outputs.append("""2.0
4.0
6.0
7.0
""")


################# MATRIX-SCALAR OPERATIONS TEST ##################
programs.append("""
m = [[1, 2][3, 4]];
n = [[11, 22][33, 44]];

print(10+m*2);
print(-10-m*2);
print(n + m == n - (-m));
""")
correct_outputs.append("""[12.0, 14.0]
[16.0, 18.0]
[-12.0, -14.0]
[-16.0, -18.0]
True
""")


################# DEEP COPY TEST ##################
programs.append("""
m = zeros(2);
n = m.copy;
m[0][0] = 5;

print(n);
print(m);
""")
correct_outputs.append("""[0, 0]
[0, 0]
[5.0, 0]
[0, 0]
""")


################# TRANSPOSED TEST ##################
programs.append("""
m = zeros(2, 3);
n = m.transposed;

print(n);
print(m);
""")
correct_outputs.append("""[0, 0]
[0, 0]
[0, 0]
[0, 0, 0]
[0, 0, 0]
""")


################# STRING CONCAT TEST ##################
programs.append("""
function test(arg1, arg2){
    print(arg1);
    print(arg2);
}
test("kra"+"kow", "" or 4);
""")
correct_outputs.append("""krakow
4.0
""")

################# FACTORIAL TEST ##################
programs.append("""
function factorial(n){
   if (n == 1){
        return n;
   }
   else{
       return n*factorial(n-1);
   }
}
print(factorial(5));
""")
correct_outputs.append("""120.0
""")


for program, correct_output in zip(programs, correct_outputs):
    sys.stdout = buffer = io.StringIO()
    source = SourceString(program)
    lexer = Lexer(source)
    parser = Parser(lexer)
    interpreter = Interpreter(parser.parse_program())
    interpreter.run()
    program_output = buffer.getvalue() # Return a str containing the entire contents of the buffer.

    assert program_output == correct_output


sys.stdout = old_stdout # Put the old stream back in place