---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Neo"
  text: "Intuitive Matrix Language"
  tagline: A friendly functional programming language with matrix operations
  actions:
    - theme: brand
      text: Online Editor
      link: /editor
    - theme: alt
      text: Get Started
      link: /get-started

features:
  - title: Native Matrix Operations
    details: Effortlessly perform matrix calculations. Create matrices, perform arithmetic, transpose, and calculate determinants with ease.
  - title: Functional Programming
    details: First-class functions, closures, higher-order functions, and anonymous functions. Write elegant, composable code with the pipe operator.
  - title: Interactive Development
    details: Write, run, and experiment with Neo code directly in your browser. No installation required.
---

## Quick Example

Here's a taste of what Neo can do:

```neo
# Create matrices
var firstMatrix = [1, 2, 3 | 4, 5, 6]
var secondMatrix = [1, 2 | 3, 4 | 5, 6]

# Perform matrix multiplication
var multiplied = firstMatrix * secondMatrix

# Use functional programming
var result = 5 |> func(x) { x * 2 } |> print
```

## Why Neo?

Neo combines the power of matrix mathematics with modern programming language features:

- **Matrix-First Design**: Built-in support for matrix operations that would be complex in other languages
- **Functional Programming**: First-class functions, closures, and higher-order functions
- **Clean Syntax**: Intuitive, readable syntax that makes mathematical operations clear
- **No Dependencies**: Self-contained interpreter with no external dependencies
- **Online**: Run in the online editor or locally with the same code

