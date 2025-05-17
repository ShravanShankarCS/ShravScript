# ShravScript User Guide

## Introduction

ShravScript is a custom programming language that combines the best features of Python and JavaScript. It uses curly braces for block definitions, making code structure explicit, while maintaining a clean and readable syntax.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Requests library (`pip install requests`) - only needed for network operations

### Using the Source Code

1. Clone or download the repository:
   ```bash
   git clone https://github.com/ShravanShankarCS/ShravScript.git
   cd ShravScript
   ```

2. Run a ShravScript program directly:
   ```bash
   python src/main.py src/examples/hello_world.shs
   ```

### Running the REPL

You can use the interactive REPL (Read-Eval-Print Loop) to test code:

```bash
python src/main.py --repl
```

### Your First ShravScript Program

Create a file called `hello.shs` with the following content:

```
print("Hello, World!")
```

Run it with:

```bash
python src/main.py hello.shs
```

### Basic Syntax

ShravScript uses curly braces for blocks and semicolons are optional:

```
let x = 10
let y = 20

if x < y {
    print("x is less than y")
} else {
    print("x is greater than or equal to y")
}
```

### Variables

Variables are declared using the `let` keyword:

```
let name = "Alice"
let age = 30
let is_active = true
```

### Functions

Functions are defined using the `fn` keyword:

```
fn greet(name) {
    return "Hello, " + name
}

print(greet("Alice"))  # Outputs: Hello, Alice
```

### Control Structures

#### If-Elif-Else

```
if condition {
    // code
} elif other_condition {
    // code
} else {
    // code
}
```

#### Loops

```
// While loop
let i = 0
while i < 5 {
    print(i)
    i = i + 1
}

// For loop
for i in 0..5 {
    print(i)
}
```

### Data Structures

#### Lists

```
let fruits = ["apple", "banana", "cherry"]
print(fruits[0])  // Outputs: apple

// Add to a list
fruits[3] = "date"
```

#### Dictionaries

```
let person = {
    name: "Bob",
    age: 25,
    city: "New York"
}

print(person.name)  // Outputs: Bob
```

## Built-in Libraries

ShravScript comes with several built-in libraries:

### fileio

For file operations:

```
import "fileio"

// Write to a file
fileio.write("output.txt", "Hello, World!")

// Read from a file
let content = fileio.read("output.txt")
print(content)
```

### netgear

For network operations:

```
import "netgear"

// Make a GET request
let response = netgear.get("https://example.com")
print(response)
```

### mathex

For mathematical operations:

```
import "mathex"

let root = mathex.sqrt(16)    // 4
let power = mathex.pow(2, 3)  // 8
let random = mathex.random()  // Random value between 0 and 1
```

### sysops

For system operations:

```
import "sysops"

let files = sysops.listdir(".")
print(files)

let home_dir = sysops.getenv("HOME")
print(home_dir)
```

## Error Handling

ShravScript provides try-catch blocks for error handling:

```
try {
    // Code that might throw an error
    let response = netgear.get("https://example.com")
    print(response)
} catch (err) {
    print("An error occurred: " + err)
}
```

## Interactive REPL

ShravScript includes a REPL (Read-Eval-Print Loop) for testing code interactively:

```bash
shravscript --repl
```

In the REPL, you can enter ShravScript code line by line:

```
shs> let x = 10
shs> let y = 20
shs> x + y
30
```

## Advanced Features

### String Interpolation

```
let name = "Alice"
let greeting = "Hello, ${name}!"
print(greeting)  // Outputs: Hello, Alice!
```

### Lambda Functions

```
let double = (x) => x * 2
print(double(5))  // Outputs: 10
```

## Contributing

If you'd like to contribute to ShravScript, please see our [contribution guidelines](https://github.com/ShravanShankarCS/ShravScript/blob/main/CONTRIBUTING.md).

## Resources

### Official Repository

The official repository for ShravScript is available at:
[https://github.com/ShravanShankarCS/ShravScript](https://github.com/ShravanShankarCS/ShravScript)

### Author

ShravScript is created and maintained by [Shravan Shankar C S](https://shravan.org). 