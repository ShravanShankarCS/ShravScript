# Contributing to ShravScript

Thank you for considering contributing to ShravScript! This document provides guidelines and instructions for contributing.

## How to Contribute

1. **Fork the Repository**
   
   Start by forking the repository to your GitHub account.

2. **Clone the Forked Repository**
   
   ```bash
   git clone https://github.com/yourusername/ShravScript.git
   cd ShravScript
   ```

3. **Create a Branch**
   
   Create a branch for your feature or bugfix:
   
   ```bash
   git checkout -b feature/your-feature-name
   ```
   
   or
   
   ```bash
   git checkout -b fix/your-bugfix-name
   ```

4. **Make Your Changes**
   
   Implement your feature or fix the bug.

5. **Run Tests**
   
   Make sure all existing examples work with your changes.

6. **Commit Your Changes**
   
   ```bash
   git commit -m "Add your meaningful commit message here"
   ```

7. **Push to Your Fork**
   
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   
   Create a pull request from your fork to the main repository [https://github.com/ShravanShankarCS/ShravScript](https://github.com/ShravanShankarCS/ShravScript).

## Coding Guidelines

- Follow PEP 8 style guidelines for Python code
- Keep the ShravScript language syntax consistent
- Document new features in code and update documentation if needed
- Write meaningful commit messages

## Adding New Features to ShravScript

### Adding a New Built-in Module

1. Create a new Python file in `src/shrav_modules/`
2. Implement the module following the pattern of existing modules
3. Add the module to the interpreter's built-in module list
4. Create example script(s) demonstrating the module's usage

### Adding New Language Features

1. Modify the tokenizer if new token types are needed
2. Update the parser to recognize the new syntax
3. Implement the feature in the interpreter
4. Add documentation and examples for the new feature

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best interests of the project

Thank you for contributing to ShravScript! 