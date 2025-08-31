---
outline: deep
---

<script setup>
import NeoEditor from './components/NeoEditor.vue'
</script>

# Neo Matrix Language Editor

Welcome to the interactive Neo Matrix Language editor! You can write and execute Neo code directly in your browser.

## Try It Out

Below is a live editor where you can write and run Neo code:

<NeoEditor />

## Example Code

Here are some examples you can try in the editor:

### Basic Function
```neo
function greet(name) {
    print("Hello, " + name + "!");
}

greet("World");
```

### Control Flow
```neo
let age = 18;
if (age >= 18) {
    print("You are an adult");
} else {
    print("You are a minor");
}
```

## How to Use

1. **Write your code** in the left panel
2. **Click "Run Code"** or press `Ctrl+Enter`
3. **View the output** in the right panel
4. **Debug errors** using the detailed error messages

The editor will execute your Neo code and display any output, return values, or error messages.