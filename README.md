# Project Description

Interpreter for my own programming language called Neo, which features native support for matrix operations.
The interpreter reads and executes Neo source files, allowing users to perform matrix calculations with simple syntax.

## Example

Suppose you have a Neo source file called `example.neo`:

```neo
matrix1 = [1, 2, 3 | 4, 5, 6];
matrix2 = [7, 8 | 9, 10 | 11, 12];
matrix3 = matrix1 * matrix2;

print("Matrix1: ");
print(matrix1);

print("Matrix2: ");
print(matrix2);

print("Matrix3: ");
print(matrix3);

print("Determinant of matrix3: ", matrix3.det);
```

You can run it with:

```bash
python Neo.py example.neo
```

**Output:**
```
Matrix1: 
-------------------
| 1.0   2.0   3.0 |
| 4.0   5.0   6.0 |
-------------------
Matrix2:
---------------
|  7.0    8.0 |
|  9.0   10.0 |
| 11.0   12.0 |
---------------
Matrix3:
-----------------
|  58.0    64.0 |
| 139.0   154.0 |
-----------------
Determinant of matrix3:  36.0
```