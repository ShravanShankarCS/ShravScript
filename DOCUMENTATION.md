# ShravScript Documentation

## Table of Contents
- [Introduction](#introduction)
- [Language Syntax](#language-syntax)
  - [Basic Syntax](#basic-syntax)
  - [Variables](#variables)
  - [Data Types](#data-types)
  - [Control Structures](#control-structures)
  - [Functions](#functions)
  - [Classes and Objects](#classes-and-objects)
  - [Modules and Imports](#modules-and-imports)
  - [Error Handling](#error-handling)
- [Built-in Libraries](#built-in-libraries)
  - [fileio](#fileio)
  - [netgear](#netgear)
  - [mathex](#mathex)
  - [sysops](#sysops)
- [Using ShravScript](#using-shravscript)
  - [Running Scripts](#running-scripts)
  - [Using the REPL](#using-the-repl)
- [Example Programs](#example-programs)
- [Language Reference](#language-reference)
  - [Keywords](#keywords)
  - [Operators](#operators)

## Introduction

ShravScript is a custom programming language implemented in Python that combines the best features of Python and JavaScript. It features a clean, readable syntax with curly braces for block definitions, making it both powerful and user-friendly.

The language supports first-class functions, rich data types, flexible control structures, and comes with built-in libraries for file operations, networking, mathematics, and system interactions.

## Language Syntax

### Basic Syntax

ShravScript uses curly braces `{}` to define blocks of code, similar to JavaScript. Unlike Python, indentation is not syntactically significant but is recommended for readability.

```javascript
// This is a comment in ShravScript
print("Hello, World!")  // Prints to the console
```

### Variables

Variables are declared using the `let` keyword. Constants can be declared using `const`.

```javascript
let name = "Alice"
let age = 30
let isActive = true

const PI = 3.14159
```

### Data Types

ShravScript supports the following data types:

- **Numbers**: integers and floating-point numbers
- **Strings**: text enclosed in quotes
- **Booleans**: `true` or `false`
- **Lists**: ordered collections using `[]`
- **Dictionaries**: key-value pairs using `{}`
- **null**: represents absence of a value

```javascript
// Numbers
let count = 42
let price = 9.99

// Strings
let greeting = "Hello, World!"

// Booleans
let isReady = true

// Lists
let fruits = ["apple", "banana", "cherry"]

// Dictionaries
let person = {
    name: "Bob",
    age: 25,
    city: "New York"
}

// Null
let empty = null
```

### Control Structures

#### If-Elif-Else

```javascript
if condition {
    // code executed if condition is true
} elif otherCondition {
    // code executed if otherCondition is true
} else {
    // code executed if all conditions are false
}
```

#### While Loop

```javascript
let i = 0
while i < 5 {
    print(i)
    i = i + 1
}
```

#### For Loop

```javascript
for i in 0..5 {
    print(i)  // Prints 0, 1, 2, 3, 4
}
```

#### Switch-Case

```javascript
let day = 3
switch (day) {
    case 1 {
        print("Monday")
    }
    case 2 {
        print("Tuesday")
    }
    case 3 {
        print("Wednesday")
    }
    default {
        print("Unknown day")
    }
}
```

### Functions

Functions are defined using the `fn` keyword.

```javascript
fn greet(name) {
    return "Hello, " + name
}

print(greet("Alice"))  // Outputs: Hello, Alice
```

#### Lambda Functions

ShravScript supports anonymous lambda functions:

```javascript
let double = (x) => x * 2
print(double(5))  // Outputs: 10

// Using lambda with map
let numbers = [1, 2, 3]
let doubled = numbers.map((x) => x * 2)
print(doubled)  // Outputs: [2, 4, 6]
```

### Classes and Objects

```javascript
class Dog {
    fn bark() {
        print("Woof")
    }
    
    fn eat(food) {
        print("Eating " + food)
    }
}

let myDog = new Dog()
myDog.bark()     // Outputs: Woof
myDog.eat("kibble")  // Outputs: Eating kibble
```

### Modules and Imports

ShravScript allows importing modules:

```javascript
import "mathex"
print(mathex.sqrt(16))  // Outputs: 4

// Importing specific functions
from "mathex" import sqrt
print(sqrt(16))  // Outputs: 4
```

### Error Handling

ShravScript provides try-catch blocks for error handling:

```javascript
try {
    // Code that might throw an error
    let result = 1 / 0
} catch (err) {
    print("An error occurred: " + err)
} finally {
    print("This always runs")
}
```

## Built-in Libraries

ShravScript comes with several built-in libraries:

### fileio

For file operations:

```javascript
import "fileio"

// Write to a file
fileio.write("output.txt", "Hello, World!")

// Read from a file
let content = fileio.read("output.txt")
print(content)

// Check if file exists
if fileio.exists("output.txt") {
    print("File exists")
}

// Open a file with a context manager
with fileio.open("output.txt", "w") as f {
    f.write("This is written using the context manager")
}
```

### netgear

For network operations:

```javascript
import "netgear"

// Make a GET request
let response = netgear.get("https://example.com")
print(response)

// Make a POST request
let postResponse = netgear.post("https://example.com/api", "data=example")
print(postResponse)

// Get headers
let headers = netgear.headers()
print(headers)
```

### mathex

For mathematical operations:

```javascript
import "mathex"

let root = mathex.sqrt(16)        // 4
let power = mathex.pow(2, 3)      // 8
let random = mathex.random()      // Random value between 0 and 1
let sine = mathex.sin(0)          // 0
let cosine = mathex.cos(0)        // 1
let tangent = mathex.tan(0)       // 0
```

### sysops

For system operations:

```javascript
import "sysops"

// List files in a directory
let files = sysops.listdir(".")
print(files)

// Get environment variable
let home = sysops.getenv("HOME")
print(home)

// Run a system command
let result = sysops.run("echo Hello from ShravScript")
print(result)
```

## Using ShravScript

### Running Scripts

To run a ShravScript program, use:

```bash
python src/main.py path/to/your/script.shs
```

For example:

```bash
python src/main.py src/examples/hello_world.shs
```

### Using the REPL

ShravScript includes a REPL (Read-Eval-Print Loop) for testing code interactively:

```bash
python src/main.py --repl
```

In the REPL, you can enter ShravScript code line by line:

```
shs> let x = 10
shs> let y = 20
shs> x + y
30
```

## Example Programs

ShravScript comes with several example programs in the `src/examples` directory:

### Hello World (hello_world.shs)

```javascript
print("Welcome to ShravScript!")
```

### Fibonacci (fibonacci.shs)

```javascript
fn fib(n) {
    if n <= 1 {
        return n
    } elif n == 2 {
        return 1
    } else {
        return fib(n - 1) + fib(n - 2)
    }
}

print(fib(8))  // Output: 21
```

### List Iteration (list_iteration.shs)

```javascript
let numbers = [1, 2, 3, 4]
for i in 0..4 {
    if numbers[i] == 3 {
        continue
    }
    if numbers[i] > 3 {
        break
    }
    print(numbers[i])
}
```

### File Operations (file_writing.shs)

```javascript
import "fileio"

with fileio.open("output.txt", "w") as f {
    f.write("This is ShravScript writing to a file!")
}

let content = fileio.read("output.txt")
print(content)
```

### Network Operations (network_call.shs)

```javascript
import "netgear"

try {
    let response = netgear.get("https://example.com")
    print(response)
} catch (err) {
    print("Network error: " + err)
}
```

### System Information (system_info.shs)

```javascript
import "sysops"

print(sysops.listdir("."))
print(sysops.getenv("HOME"))
```

### Lambda and Map (lambda_map.shs)

```javascript
let nums = [1, 2, 3]
let doubled = nums.map((x) => x * 2)
print(doubled)  // Output: [2, 4, 6]
```

## Language Reference

### Keywords

ShravScript uses the following keywords:

- **Variable Declaration**: `let`, `const`
- **Control Flow**: `if`, `elif`, `else`, `switch`, `case`, `default`, `while`, `for`, `do`, `break`, `continue`
- **Functions**: `fn`, `return`, `lambda`
- **Classes**: `class`, `this`, `new`
- **Modules**: `import`, `from`, `as`, `with`
- **Error Handling**: `try`, `catch`, `finally`, `throw`, `raise`, `assert`
- **Logical Operators**: `and`, `or`, `not`, `is`
- **Data Values**: `true`, `false`, `null`
- **Miscellaneous**: `pass`, `global`, `nonlocal`

### Operators

- **Arithmetic**: `+`, `-`, `*`, `/`, `%`, `**`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- **Index Access**: `[]` (for lists and dictionaries)
- **Property Access**: `.` (for objects and modules)
- **Range**: `..` (for for loops) 