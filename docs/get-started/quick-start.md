# Quick Start

This tutorial will get you up and running with Neo in just a few minutes. We'll cover the basics and build up to more complex examples.

## Your First Neo Program

Let's start with the classic "Hello, World!" program:

```neo
print("Hello, World!")
```

**Output:**
```
Hello, World!
```

## Variables and Data Types

Neo supports several data types. Let's explore them:

```neo
# Numbers (scalars)
var age = 25
var pi = 3.14159

# Strings
var name = "Alice"
var message = "Hello, " + name

# Booleans
var isStudent = True
var isWorking = False

# Print using function call or pipe operator
print(age)
print(pi)
name |> print
message |> print
isStudent |> print
```

**Output:**
```
25
3.14159
Alice
Hello, Alice
True
```

## Your First Matrix

Matrices are Neo's specialty! Here's how to create and work with them:

```neo
# Create a 2x3 matrix
var matrix = [1, 2, 3 | 4, 5, 6]

# Print the matrix
matrix |> print
```

**Output:**
```
-------------
| 1   2   3 |
| 4   5   6 |
-------------
```

## Matrix Operations

Let's perform some basic matrix operations:

```neo
# Create two matrices
var A = [1, 2 | 3, 4]
var B = [5, 6 | 7, 8]


# Matrix multiplication
var product = A * B
product |> print

# Scalar multiplication
var scaled = A * 2
scaled |> print
```

**Output:**
```
----------
| 19  22 |
| 43  50 |
----------
---------
| 2   4 |
| 6   8 |
---------
```

## Functions

Functions are first-class citizens in Neo. Let's create some:

```neo
# Named function
func greet(name) {
    return "Hello, " + name
}

# Anonymous function
var exclamation = func(str) { str + "!" }


# Piping with both named and anonymous function
"World" |> greet |> exclamation |> print
```

**Output:**
```
Hello, World!
```

## A Complete Example

Let's put it all together with a more complex example:

```neo
# Function to create a matrix with sequential numbers
func createMatrix(rows, cols) {
    var mut matrix = zeros(rows, cols)
    var mut i = 0
    while (i < rows) {
        var mut j = 0
        while (j < cols) {
            matrix[i, j] = i * cols + j + 1
            j = j + 1
        }
        i = i + 1
    }
    return matrix
}

# Create and display a matrix
var myMatrix = createMatrix(3, 4)
myMatrix |> print

# Transpose the matrix
"Transposed:" |> print
myMatrix.transposed |> print
```

**Output:**
```
--------------------
| 1   2    3    4  |
| 5   6    7    8  |
| 9   10   11   12 |
--------------------
Transposed:
--------------
| 1   5   9  |
| 2   6   10 |
| 3   7   11 |
| 4   8   12 |
--------------
```

## What's Next?

Congratulations! You've learned the basics of Neo. Explore other topics to learn more