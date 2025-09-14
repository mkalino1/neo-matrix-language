# Introduction

Welcome to Neo Matrix Language! This guide will help you get up and running with Neo quickly.

## What is Neo?

Neo is a programming language with built-in matrix type. It combines:

- **Native matrix support** with intuitive operations
- **Functional programming** features like first-class functions, piping and closures
- **Friendly syntax** designed for great developer experience

## Quick Example

Here's a simple Neo program that demonstrates matrices multiplication:

```neo
# Create two matrices (2x3 and 3x2)
var matrixA = [1, 2, 3 | 4, 5, 6]
var matrixB = [1, 2 | 3, 4 | 5, 6]

# Multiply them
var result = matrixA * matrixB

# Print the result
result |> print
```

**Output:**
```
-----------
| 22   28 |
| 49   64 |
-----------
```

## Main features

### Matrix Operations
- **Intuitive syntax**: `[1, 2 | 3, 4]` instead of complex 2D array declarations
- **Built-in operations**: Multiplication, transpose, determinant, and more
- **Visual output**: Matrices are displayed in a readable format

### Functional Programming
- **First-class functions**: Functions are values that can be passed around
- **Closures**: Functions can capture variables from their environment
- **Pipe operator**: Chain operations with `|>` for readable code

### Educational value
- **Simple syntax**: Easy to learn
- **Mathematical focus**: Perfect for linear algebra and matrix operations
- **Interactive**: Try code immediately in the online editor

## Next Steps

Ready to start coding? Here are your options:

**[Try the Online Editor](/editor)** - No installation needed, start coding immediately

**[Learn the Basics](/get-started/quick-start)** - Follow tutorial

**[Explore Examples](/examples/)** - See what's possible with Neo
