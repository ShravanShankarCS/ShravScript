import os
from environment import ShravScriptModule, ShravScriptNativeFunction

class ShravScriptFile:
    def __init__(self, file_obj):
        self.file = file_obj
    
    def read(self):
        return self.file.read()
    
    def write(self, content):
        self.file.write(content)
        return True
    
    def close(self):
        self.file.close()

def create_module(interpreter):
    module = ShravScriptModule("fileio")
    
    # Read file function
    def read_fn(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Write file function
    def write_fn(path, content):
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Check if file exists
    def exists_fn(path):
        return os.path.exists(path)
    
    # Append to file
    def append_fn(path, content):
        try:
            with open(path, 'a', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Delete file
    def delete_fn(path):
        try:
            if os.path.exists(path):
                os.remove(path)
                return True
            return False
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Open file function
    def open_fn(path, mode='r'):
        try:
            file_obj = open(path, mode, encoding='utf-8')
            return ShravScriptFile(file_obj)
        except Exception as e:
            return f"Error: {str(e)}"
    
    module.add_function("read", ShravScriptNativeFunction(1, read_fn))
    module.add_function("write", ShravScriptNativeFunction(2, write_fn))
    module.add_function("exists", ShravScriptNativeFunction(1, exists_fn))
    module.add_function("append", ShravScriptNativeFunction(2, append_fn))
    module.add_function("delete", ShravScriptNativeFunction(1, delete_fn))
    module.add_function("open", ShravScriptNativeFunction(2, open_fn))
    
    return module 