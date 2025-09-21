---
outline: deep
---

<script setup>
import NeoEditor from './components/NeoEditor.vue'
</script>

# Neo Matrix Language Editor

Welcome to the interactive Neo Matrix Language editor! You can write and execute Neo code directly in your browser with real-time feedback and beautiful matrix visualization.

## Try It Out

Below is a live editor where you can write and run Neo code:

<NeoEditor />

## How to Use

1. **Write your code** in the first panel
2. **Click "Run Code"** or press `Ctrl+Enter`
3. **View the output** in the second panel
4. **Debug errors** using the detailed error messages

The editor will execute your Neo code and display any output, return values, or error messages.

## Features

- **Real-time Execution**: Run Neo code instantly with immediate feedback
- **Matrix Visualization**: See matrices displayed in a beautiful, readable format
- **Error Handling**: Clear error messages and debugging information
- **Syntax Highlighting**: Color-coded syntax for better readability
- **No Installation**: Works in any web browser

## Example Code

Here are some examples you can try in the editor:

### Matrix Operations
```neo
# Create and manipulate matrices
var A = [1, 2 | 3, 4]
var B = [5, 6 | 7, 8]

# Matrix arithmetic
var sum = A + B
var product = A * B

print("Matrix A:")
A |> print
print("Matrix B:")
B |> print
print("Sum A + B:")
sum |> print
print("Product A * B:")
product |> print
```

### Functions
```neo
# Function definition
func factorial(n) {
    if (n <= 1) {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}

# Use the function
print("5! = " + factorial(5))
```

### Functional Programming
```neo
# Higher-order functions and closures
func createCounter() {
    var mut count = 0
    return func() {
        count = count + 1
        return count
    }
}

var counter = createCounter()
print("Count: " + counter())  # 1
print("Count: " + counter())  # 2
print("Count: " + counter())  # 3

# Function composition
func compose(f, g) {
    return func(x) {
        return f(g(x))
    }
}

var square = func(x) { x * x }
var addOne = func(x) { x + 1 }
var squareThenAddOne = compose(addOne, square)

print("Square then add one: " + squareThenAddOne(3))  # 10
```