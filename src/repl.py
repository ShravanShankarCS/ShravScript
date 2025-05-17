import sys
import os
from interpreter import Interpreter

# Try to import readline but don't require it (for Windows compatibility)
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

def start_repl():
    print("ShravScript REPL (Interactive Shell)")
    print("Type 'exit()' or press Ctrl+C to exit")
    print()
    
    interpreter = Interpreter()
    
    # Try to use readline for history if available
    if READLINE_AVAILABLE:
        try:
            readline.parse_and_bind('tab: complete')
            history_file = os.path.expanduser('~/.shravscript_history')
            
            try:
                readline.read_history_file(history_file)
            except FileNotFoundError:
                pass
        except (AttributeError):
            # readline might not be fully functional
            pass
    
    try:
        while True:
            try:
                line = input("shs> ")
                
                if line.strip() == "exit()":
                    break
                
                # Handle multi-line input for blocks
                if "{" in line and "}" not in line:
                    block_level = 1
                    while block_level > 0:
                        continuation = input(".... ")
                        line += "\n" + continuation
                        
                        block_level += continuation.count("{")
                        block_level -= continuation.count("}")
                
                result = interpreter.interpret(line)
                
                # Only print the result if it's not None (for expressions)
                if result is not None:
                    print(interpreter.stringify(result))
            
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
            except Exception as e:
                print(f"Error: {e}")
    
    finally:
        if READLINE_AVAILABLE:
            try:
                readline.write_history_file(history_file)
            except:
                pass
    
    return 0

if __name__ == "__main__":
    sys.exit(start_repl()) 