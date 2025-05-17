#!/usr/bin/env python3
import sys
import os

# Add the src directory to path when running directly
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Import using absolute imports
from interpreter import Interpreter

def run_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            source = file.read()
        
        interpreter = Interpreter()
        interpreter.interpret(source)
        return 0
    except FileNotFoundError:
        print(f"Error: Could not find file '{path}'")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def print_usage():
    print("ShravScript Interpreter")
    print("Usage:")
    print("  shrav [script.shs]")
    print("  shrav --repl")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    if sys.argv[1] == "--repl":
        # Launch the REPL
        import repl
        return repl.start_repl()
    else:
        # Run a script file
        script_path = sys.argv[1]
        return run_file(script_path)

# Entry point for the command-line tool
def entry_point():
    sys.exit(main())

if __name__ == "__main__":
    entry_point() 