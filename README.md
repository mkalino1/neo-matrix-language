# Project Description

Interpreter for my own programming language called Neo, which features native support for matrix operations.
The interpreter reads and executes Neo source files, allowing users to perform matrix calculations with simple syntax.

## Example

Suppose you have a Neo source file called `example.neo`:

```neo
firstMatrix = [1, 2, 3 | 4, 5, 6];
secondMatrix = [1, 2 | 3, 4 | 5, 6];
multiplied = firstMatrix * secondMatrix;

resultMatrix = [
  "First matrix", "Second matrix", "Multiplied", "Transposed" |
  firstMatrix, secondMatrix, multiplied, multiplied.transposed
];

print(resultMatrix);
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