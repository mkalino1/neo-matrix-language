# Function Declaration

Functions in Neo are first-class citizens, meaning they can be assigned to variables, passed as arguments, and returned from other functions. This page covers how to declare functions.

## Named Functions

Use the `func` keyword to declare a named function:

```neo
func greet(name) {
    return "Hello, " + name + "!"
}

# Call the function
var message = greet("Alice")
print(message)  # "Hello, Alice!"
```

## Anonymous Functions

Create anonymous functions using `func` without a name:

```neo
var square = func(x) {
    return x * x
}

var result = square(5)
print("Square of 5: " + result)  # 25
```

### Assigning Functions to Variables

```neo
# Assign named function to variable
func originalFunction(x) {
    return x * 2
}

var alias = originalFunction
print("Alias result: " + alias(5))  # 10

# Assign anonymous function to variable
var double = func(x) {
    return x * 2
}

print("Double result: " + double(5))  # 10
```

### Inline function declaration

```neo
func applyFunction(f, x) { f(x) }

# Declare function as an argument inline
var result = applyFunction(func(x){ x * 2 }, 5)

print("Result: " + result)  # 10
```

## Function Patterns

### Function Factories

Create functions that return other functions:

```neo
func createMultiplier(factor) {
    return func(x) {
        return x * factor
    }
}

var double = createMultiplier(2)
var triple = createMultiplier(3)

print("Double 5: " + double(5))  # 10
print("Triple 5: " + triple(5))  # 15
```

### Function Composition

Combine functions to create new functionality:

```neo
func compose(f, g) {
    return func(x) {
        return f(g(x))
    }
}

var square = func(x) { return x * x }
var addOne = func(x) { return x + 1 }

var squareThenAddOne = compose(addOne, square)
print("Square then add one: " + squareThenAddOne(3))  # 10
```

### Parameter Names

- Parameter names must be valid identifiers
- Parameters are local to the function
- Parameter names can shadow outer variables

```neo
var global = 10

func example(global) {  # Parameter shadows global
    print("Inner variable: " + global)
}
```

### Return Statements

Without explicit return statment function will return the last expression

```neo
func doubled(x) {
    # No need for return keyword here
    x * 2
}
```