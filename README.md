# ShravScript

<div align="center">
  
![ShravScript Logo](website/icon.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/downloads/)

</div>

ShravScript is a custom programming language that combines features from Python and JavaScript. It offers a clean syntax with curly braces for blocks while maintaining readability.

## Features

- Clean syntax with curly braces for blocks
- First-class functions with closures and lambdas
- Variables and rich data types (numbers, strings, booleans, null)
- Control structures (if/elif/else, while, for)
- Functions with parameters and return values
- Lists and dictionaries
- Object-oriented programming with classes
- Error handling with try/catch
- Import system for modularity
- Built-in modules for file I/O, networking, and more

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ShravanShankarCS/ShravScript.git
cd ShravScript
```

### 2. Run a ShravScript file

**On Windows:**

```bash
shrav.bat src\examples\hello_world.shs
```

**On all platforms:**

```bash
python src/main.py src/examples/hello_world.shs
```

### 3. Start the interactive REPL

**On Windows:**

```bash
shrav.bat --repl
```

**On all platforms:**

```bash
python src/main.py --repl
```

## Example Code

```javascript
# Fibonacci sequence
fn fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

for (i in 0 to 10) {
    print fibonacci(i);
}
```

## Project Structure

- `src/` - The main source code of the interpreter
  - `main.py` - Entry point for the interpreter
  - `tokenizer.py` - Lexical analyzer that converts source code to tokens
  - `parser.py` - Converts tokens into an abstract syntax tree (AST)
  - `interpreter.py` - Evaluates the AST
  - `environment.py` - Handles variable scoping and bindings
  - `repl.py` - Interactive shell for ShravScript
  - `shrav_modules/` - Built-in libraries implementation
  - `examples/` - Example ShravScript programs
- `docs/` - Documentation files
- `website/` - Website resources including icons

## Built-in Modules

ShravScript comes with several built-in modules:

- **fileio** - File input/output operations
- **netgear** - Networking capabilities (HTTP requests)
- **mathex** - Extended math functions
- **sysops** - System operations and information

## Extending ShravScript

### Adding a new built-in module

1. Create a new Python file in the `src/shrav_modules/` directory
2. Implement the module's functionality
3. Add the module name to the list in `interpreter.py`

## Requirements

- Python 3.6 or higher

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Author

[Shravan Shankar C S](https://shravan.org)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 