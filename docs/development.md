# ShravScript Development Guide

This guide is intended for developers who want to contribute to the ShravScript interpreter or build on top of it.

## Project Structure

The ShravScript project is organized as follows:

- `src/`: Core interpreter components
  - `tokenizer.py`: Lexical analyzer that converts source code to tokens
  - `parser.py`: Parser that generates the Abstract Syntax Tree (AST)
  - `interpreter.py`: Executes the AST
  - `environment.py`: Handles variables and scopes
  - `shrav_modules/`: Built-in library modules
  - `examples/`: Example ShravScript programs

- `docs/`: Documentation files
- `tests/`: Unit tests
- `website/`: Documentation website

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ShravanShankarCS/ShravScript.git
   cd ShravScript
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install requests
   ```

## Running Tests

We use Python's built-in `unittest` framework for testing:

```bash
# Run all tests
python tests/run_tests.py

# Run a specific test file
python tests/test_tokenizer.py
```

## Interpreter Components

### Tokenizer

The tokenizer (`src/tokenizer.py`) converts source code text into a list of tokens. Each token has a type (e.g., NUMBER, STRING, IDENTIFIER) and a value.

```python
# Example of adding a new token type
class TokenType(Enum):
    # ... existing token types ...
    NEW_TOKEN_TYPE = auto()
    
# Example of updating the tokenizer to recognize the new token
def tokenize(self):
    # ... existing code ...
    if self.match('new_pattern'):
        return self.new_token_type()
    # ... existing code ...
```

### Parser

The parser (`src/parser.py`) converts tokens into an Abstract Syntax Tree (AST). Each node in the AST represents a language construct (e.g., variable declaration, function call).

```python
# Example of adding a new AST node type
class NewNode(Node):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        
# Example of adding a parser method for the new construct
def parse_new_construct(self):
    # ... parsing logic ...
    return NewNode(param1, param2)
```

### Interpreter

The interpreter (`src/interpreter.py`) executes the AST by traversing it and performing the appropriate actions.

```python
# Example of adding support for a new AST node type
def evaluate(self, expr):
    # ... existing code ...
    elif expr_type == parser.NewNode:
        return self.evaluate_new_node(expr)
    # ... existing code ...
    
def evaluate_new_node(self, expr):
    # ... evaluation logic ...
    return result
```

## Adding a New Built-in Library

To add a new built-in library:

1. Create a new Python file in the `src/shrav_modules` directory:
   ```python
   # src/shrav_modules/mynewlib.py
   
   def create_module(interpreter):
       """Create and return a new ShravScript module."""
       from interpreter import ShravScriptModule
       
       module = ShravScriptModule("mynewlib")
       
       def my_function(interpreter, args):
           # Implementation
           return result
       
       module.add_function("my_function", my_function)
       
       return module
   ```

2. Update the `__init__.py` file in the `src/shrav_modules` directory:
   ```python
   # src/shrav_modules/__init__.py
   
   __all__ = ["netgear", "sysops", "mathex", "fileio", "mynewlib"]
   
   from . import netgear
   from . import sysops
   from . import mathex
   from . import fileio
   from . import mynewlib
   ```

3. Update the `load_module` method in the interpreter to recognize the new module:
   ```python
   def load_module(self, module_name):
       # ... existing code ...
       if module_name in ["netgear", "sysops", "mathex", "fileio", "mynewlib"]:
           # ... existing code ...
   ```

## Development Workflow

1. Make your changes to the source code
2. Add unit tests for new functionality
3. Run the tests to ensure everything works
4. Test with example ShravScript programs
5. Create a pull request with your changes to the [official repository](https://github.com/ShravanShankarCS/ShravScript)

## Code Style

We follow PEP 8 with the following exceptions:

- Line length limit of 100 characters instead of 79
- Use 4 spaces for indentation

Use `flake8` to check your code style before submitting a pull request.

## Resources

- Official repository: [https://github.com/ShravanShankarCS/ShravScript](https://github.com/ShravanShankarCS/ShravScript)
- Author's website: [https://shravan.org](https://shravan.org) 