# Neo Language

Interpreter for my own programming language called Neo, which features native support for matrix operations.
The interpreter reads and executes Neo source files, allowing users to perform matrix calculations with simple syntax.

You can also use it online and read more about it here:
[neolang.vercel.app](http://neolang.vercel.app/)

# Quick Syntax Overview
Neo's syntax is designed to be simple and intuitive, with a focus on matrix operations. Here are some key features of Neo's syntax:

### **Matrix Literals**
Matrices can be defined using square brackets `[]` with rows separated by `|` and elements separated by commas.
```
# 2x3 matrix
var matrix = [1, 2, 3 | 4, 5, 6]
```

### **Variable Declarations**
Variables `var` are immutable by default and can be declared using as mutable using `mut` keyword.
```
var mut counter = 0
```

### **Function Declarations**
Functions are first class citizens that are declared using the `func` keyword and can be named or anonymous.
```
# Create a named function
func add(a, b) {
    return a + b
}
# Create an anonymous function and assign it to a variable
var multiply = func(x) {
    return x * x
}
```

### **Pipelines**
Neo supports pipelines using the `|>` operator, allowing you to chain operations together.
```
matrix |> reverse |> print
```

### **Closures**
Functions in Neo can capture variables from their enclosing scope, allowing for powerful functional programming patterns and simulate object-oriented behavior.
```
func makeCounter() {
    var mut count = 0
    return func() {
        count = count + 1
        return count
    }
}
var counter = makeCounter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### **Matrix Operations**
Neo provides built-in support for matrix operations such as addition, multiplication, and transposition.
```
var A = [1, 2 | 3, 4]
var B = [5, 6 | 7, 8]
var C = A + B
var D = A * B
var E = B.transposed
```

### **Immediate function invocation**
You can declare and invoke a function immediately without assigning it to a variable.
```
func(x) {
    print("The value is: " + x)
}(42)
```

# How does the interpreter work?

The interpreter itself is implemented in Python and consists of several components:
1. **Lexer**: This component is responsible for tokenizing the input Neo source code. It breaks down the code into a stream of tokens that represent keywords, identifiers, literals, operators, and other syntactic elements.
2. **Parser**: The parser takes the stream of tokens produced by the lexer and constructs an Abstract Syntax Tree (AST). The AST is a hierarchical representation of the program's structure, capturing the relationships between different elements of the code.
3. **Interpreter**: The interpreter traverses the AST and executes the program according to the semantics defined by the Neo language. It handles variable declarations, control flow, function calls, and matrix operations.


## Example of Abstract Syntax Tree:
Following Neo code and its corresponding AST builded by the parser:

```neo
    var mut matrix = zeros(3, 4)
    var mut i = 0
    while (i < matrix.rowlen) {
        var mut j = 0
        while (j < matrix.collen) {
            matrix[i, j] = i * j
            j = j + 1
        }
        i = i + 1
    }
    print(matrix)

```

```
Program
├── Declaration: mutable m = FunctionCall: zeros [Scalar: 3, Scalar: 4]
├── Declaration: mutable i = Scalar: 0
├── WhileLoop: BinaryOperator: OperatorType.LESS < i Property: m.rowlen >
│   └── Block
│       ├── Declaration: mutable j = Scalar: 0
│       ├── WhileLoop: BinaryOperator: OperatorType.LESS < j Property: m.collen >
│       │   └── Block
│       │       ├── Assignment: m [i, j] BinaryOperator: OperatorType.MULTIPLY < i j >
│       │       └── Assignment: j BinaryOperator: OperatorType.PLUS < j Scalar: 1 >
│       └── Assignment: i BinaryOperator: OperatorType.PLUS < i Scalar: 1 >
└── FunctionCall: print [matrix]
```

## How does the online editor work?

When you write Neo code in the online editor and click the "Run" button, the editor sends your code to a backend serverless Vercel function where the Neo interpreter is hosted. The server processes the code using the interpreter, executes it, and returns the output back to the editor, which then displays it in the console area. This allows users to quickly test and experiment with Neo code without needing to set up a local environment.

## How to run it locally?

Suppose you have a Neo source file called `example.neo`:

```neo
var firstMatrix = [1, 2, 3 | 4, 5, 6]
var secondMatrix = [1, 2 | 3, 4 | 5, 6]
var multiplied = firstMatrix * secondMatrix

var resultMatrix = [
  "First matrix", "Second matrix", "Multiplied", "Transposed" |
  firstMatrix, secondMatrix, multiplied, multiplied.transposed
]

resultMatrix |> print
```

You can run it with:

```bash
python Neo.py example.neo
```

**Output:**
```
---------------------------------------------------------------------------
|     First matrix      Second matrix      Multiplied        Transposed   |
| -------------------   -------------   ---------------   --------------- |
| | 1.0   2.0   3.0 |   | 1.0   2.0 |   | 22.0   28.0 |   | 22.0   49.0 | |
| | 4.0   5.0   6.0 |   | 3.0   4.0 |   | 49.0   64.0 |   | 28.0   64.0 | |
| -------------------   | 5.0   6.0 |   ---------------   --------------- |
|                       -------------                                     |
---------------------------------------------------------------------------
```