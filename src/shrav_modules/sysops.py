import os
import subprocess
from environment import ShravScriptModule, ShravScriptNativeFunction

def create_module(interpreter):
    module = ShravScriptModule("sysops")
    
    # List directory contents
    def listdir_fn(path="."):
        try:
            return os.listdir(path)
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Run system command
    def run_fn(command):
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error (code {result.returncode}): {result.stderr}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Get environment variable
    def getenv_fn(key):
        return os.environ.get(key, "")
    
    module.add_function("listdir", ShravScriptNativeFunction(1, listdir_fn))
    module.add_function("run", ShravScriptNativeFunction(1, run_fn))
    module.add_function("getenv", ShravScriptNativeFunction(1, getenv_fn))
    
    return module 