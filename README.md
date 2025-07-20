# Project Description

Interpreter for my own programming language called Neo, which features native support for matrix operations.
The interpreter reads and executes Neo source files, allowing users to perform matrix calculations with simple syntax.

## Example

Suppose you have a Neo source file called `example.neo`:

```neo
A = [[1, 2][3, 4]]
B = [[5, 6][7, 8]]
C = A + B
print(C)
```

You can run it with:

```bash
python Neo.py example.neo
```

**Output:**
```
---------------
|  6.0    8.0 |
| 10.0   12.0 |
---------------
```