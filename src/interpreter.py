import parser as parser_module
from tokenizer import Tokenizer, TokenType
from environment import Environment, ReturnValue, ShravScriptFunction, ShravScriptNativeFunction, ShravScriptModule
import re
import os
import importlib

# Import necessary modules for builtins
import sys
import os
import math
import random

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.modules = {}
        
        # Initialize with native functions
        self.define_native_functions()
    
    def define_native_functions(self):
        self.globals.define("clock", ShravScriptNativeFunction(0, lambda: import_time().time()))
        self.globals.define("len", ShravScriptNativeFunction(1, len))
        self.globals.define("str", ShravScriptNativeFunction(1, str))
        self.globals.define("int", ShravScriptNativeFunction(1, lambda x: int(float(x)) if x is not None else 0))
        self.globals.define("float", ShravScriptNativeFunction(1, lambda x: float(x) if x is not None else 0.0))
    
    def interpret(self, source):
        try:
            tokenizer = Tokenizer(source)
            tokens = tokenizer.tokenize()
            
            parser_instance = parser_module.Parser(tokens)
            program = parser_instance.parse()
            
            return self.evaluate(program)
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            return None
        except Exception as e:
            self.runtime_error(e)
            return None
    
    def runtime_error(self, error):
        print(f"Runtime Error: {error}")
    
    def execute(self, stmt):
        stmt_type = type(stmt)
        
        if stmt_type == parser_module.Print:
            self.execute_print(stmt)
        elif stmt_type == parser_module.VariableDeclaration:
            self.execute_var_declaration(stmt)
        elif stmt_type == parser_module.FunctionDeclaration:
            self.execute_function_declaration(stmt)
        elif stmt_type == parser_module.Return:
            self.execute_return(stmt)
        elif stmt_type == parser_module.IfStatement:
            self.execute_if(stmt)
        elif stmt_type == parser_module.WhileLoop:
            self.execute_while(stmt)
        elif stmt_type == parser_module.ForLoop:
            self.execute_for(stmt)
        elif stmt_type == parser_module.WithStatement:
            self.execute_with(stmt)
        elif stmt_type == parser_module.BreakStatement:
            raise BreakException()
        elif stmt_type == parser_module.ContinueStatement:
            raise ContinueException()
        elif stmt_type == parser_module.TryCatch:
            self.execute_try_catch(stmt)
        elif stmt_type == parser_module.ImportStatement:
            self.execute_import(stmt)
        elif stmt_type == parser_module.ClassDeclaration:
            self.execute_class_declaration(stmt)
        elif stmt_type == parser_module.Program:
            self.execute_program(stmt)
        else:
            self.evaluate(stmt)
    
    def execute_program(self, program):
        for stmt in program.statements:
            self.execute(stmt)
    
    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous
    
    def execute_var_declaration(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        
        self.environment.define(stmt.name, value)
    
    def execute_function_declaration(self, stmt):
        function = ShravScriptFunction(stmt, self.environment)
        self.environment.define(stmt.name, function)
    
    def execute_return(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        
        raise ReturnValue(value)
    
    def execute_if(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute_block(stmt.if_body, Environment(self.environment))
        else:
            # Check elif conditions in order
            for i in range(len(stmt.elif_conditions)):
                if self.is_truthy(self.evaluate(stmt.elif_conditions[i])):
                    self.execute_block(stmt.elif_bodies[i], Environment(self.environment))
                    return  # Exit after executing the first successful elif block
                
            # If no elif conditions matched, try the else block
            if stmt.else_body is not None:
                self.execute_block(stmt.else_body, Environment(self.environment))
    
    def execute_while(self, stmt):
        try:
            while self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    # Just continue with the next iteration
                    continue
                except BreakException:
                    # Break out of the loop
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException)):
                raise e
    
    def execute_for(self, stmt):
        range_start = int(self.evaluate(stmt.range_start))
        range_end = int(self.evaluate(stmt.range_end))
        
        try:
            for i in range(range_start, range_end):
                env = Environment(self.environment)
                env.define(stmt.var_name, i)
                
                try:
                    self.execute_block(stmt.body, env)
                except ContinueException:
                    # Just continue with the next iteration
                    continue
                except BreakException:
                    # Break out of the loop
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException)):
                raise e
    
    def execute_with(self, stmt):
        # Evaluate the resource expression
        resource = self.evaluate(stmt.expression)
        
        # Set up the environment with the 'as' variable
        env = Environment(self.environment)
        env.define(stmt.var_name, resource)
        
        try:
            # Execute the with block
            self.execute_block(stmt.body, env)
        finally:
            # Close the resource if it has a close method
            if hasattr(resource, 'close') and callable(resource.close):
                resource.close()
    
    def execute_try_catch(self, stmt):
        try:
            self.execute_block(stmt.try_body, Environment(self.environment))
        except Exception as e:
            catch_env = Environment(self.environment)
            catch_env.define(stmt.catch_var, str(e))
            self.execute_block(stmt.catch_body, catch_env)
    
    def execute_import(self, stmt):
        module_name = stmt.module_name
        if module_name in self.modules:
            module = self.modules[module_name]
        else:
            module = self.load_module(module_name)
            self.modules[module_name] = module
        
        self.environment.define(module_name, module)
    
    def load_module(self, module_name):
        # Check for builtin modules first
        if module_name in ["netgear", "sysops", "mathex", "fileio"]:
            module_path = f"shrav_modules.{module_name}"
            try:
                module = importlib.import_module(module_path)
                return module.create_module(self)
            except ImportError as e:
                raise RuntimeError(f"Failed to load builtin module: {module_name} - {e}")
        
        # Try to load as a user-defined module
        try:
            with open(f"{module_name}.shs", "r") as f:
                source = f.read()
            
            # Create a new interpreter to evaluate the module
            mod_interpreter = Interpreter()
            mod_interpreter.interpret(source)
            
            # Create and return a module with the module's environment
            module = ShravScriptModule(module_name)
            for name, value in mod_interpreter.environment.values.items():
                if callable(value):
                    module.add_function(name, value)
            
            return module
        except FileNotFoundError:
            raise RuntimeError(f"Module not found: {module_name}")
    
    def execute_class_declaration(self, stmt):
        methods = {}
        for method in stmt.methods:
            function = ShravScriptFunction(method, self.environment)
            methods[method.name] = function
        
        self.environment.define(stmt.name, ShravScriptClass(stmt.name, methods))
    
    def execute_print(self, stmt):
        value = self.evaluate(stmt.value)
        print(self.stringify(value))
    
    def evaluate(self, expr):
        expr_type = type(expr)
        
        if expr_type == parser_module.Literal:
            return expr.value
        elif expr_type == parser_module.Identifier:
            return self.lookup_variable(expr)
        elif expr_type == parser_module.Assignment:
            return self.evaluate_assignment(expr)
        elif expr_type == parser_module.BinaryOp:
            return self.evaluate_binary(expr)
        elif expr_type == parser_module.UnaryOp:
            return self.evaluate_unary(expr)
        elif expr_type == parser_module.FunctionCall:
            return self.evaluate_call(expr)
        elif expr_type == parser_module.ListLiteral:
            return self.evaluate_list(expr)
        elif expr_type == parser_module.DictLiteral:
            return self.evaluate_dict(expr)
        elif expr_type == parser_module.IndexAccess:
            return self.evaluate_index_access(expr)
        elif expr_type == parser_module.PropertyAccess:
            return self.evaluate_property_access(expr)
        elif expr_type == parser_module.LambdaExpression:
            return self.evaluate_lambda(expr)
        elif expr_type == parser_module.Program:
            return self.execute_program(expr)
    
    def lookup_variable(self, expr):
        name = expr.name
        return self.environment.get(name)
    
    def evaluate_assignment(self, expr):
        value = self.evaluate(expr.value)
        
        if isinstance(expr.target, parser_module.Identifier):
            name = expr.target.name
            self.environment.assign(name, value)
        elif isinstance(expr.target, parser_module.PropertyAccess):
            obj = self.evaluate(expr.target.obj)
            if hasattr(obj, 'set'):
                obj.set(expr.target.prop, value)
            else:
                setattr(obj, expr.target.prop, value)
        elif isinstance(expr.target, parser_module.IndexAccess):
            obj = self.evaluate(expr.target.obj)
            index = self.evaluate(expr.target.index)
            obj[index] = value
        
        return value
    
    def evaluate_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator == '+':
            # Handle string concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif expr.operator == '-':
            return left - right
        elif expr.operator == '*':
            return left * right
        elif expr.operator == '/':
            return left / right
        elif expr.operator == '%':
            return left % right
        elif expr.operator == '**':
            return left ** right
        elif expr.operator == '==':
            return left == right
        elif expr.operator == '!=':
            return left != right
        elif expr.operator == '<':
            return left < right
        elif expr.operator == '>':
            return left > right
        elif expr.operator == '<=':
            return left <= right
        elif expr.operator == '>=':
            return left >= right
        elif expr.operator == 'and':
            return self.is_truthy(left) and self.is_truthy(right)
        elif expr.operator == 'or':
            return self.is_truthy(left) or self.is_truthy(right)
    
    def evaluate_unary(self, expr):
        right = self.evaluate(expr.operand)
        
        if expr.operator == '-':
            return -right
        elif expr.operator == 'not':
            return not self.is_truthy(right)
    
    def evaluate_call(self, expr):
        callee = self.evaluate(expr.func)
        
        arguments = []
        for arg in expr.args:
            arguments.append(self.evaluate(arg))
        
        # Handle module functions and methods
        if isinstance(callee, ShravScriptModule):
            # This is just a module reference, not a call
            raise RuntimeError("Cannot call a module directly. Use module.function() instead.")
        elif isinstance(expr.func, parser_module.PropertyAccess):
            # This is a method call: obj.method()
            obj = self.evaluate(expr.func.obj)
            
            if isinstance(obj, ShravScriptModule):
                # This is a module method call: module.function()
                method_name = expr.func.prop
                method = obj.get_function(method_name)
                return method(self, arguments)
            elif isinstance(obj, list):
                method_name = expr.func.prop
                if method_name == "map":
                    # Handle built-in list.map() method
                    if not arguments or not callable(arguments[0]):
                        raise RuntimeError("map() requires a function argument")
                    lambda_func = arguments[0]
                    return [lambda_func(self, [item]) for item in obj]
            
            # For other method calls, proceed normally
        
        if not callable(callee):
            raise RuntimeError(f"Can only call functions and classes, got {type(callee).__name__}")
        
        return callee(self, arguments)
    
    def evaluate_list(self, expr):
        elements = []
        for element in expr.elements:
            elements.append(self.evaluate(element))
        return elements
    
    def evaluate_dict(self, expr):
        result = {}
        for key, value in expr.items.items():
            result[key] = self.evaluate(value)
        return result
    
    def evaluate_index_access(self, expr):
        obj = self.evaluate(expr.obj)
        index = self.evaluate(expr.index)
        
        if isinstance(obj, (list, dict, str)):
            return obj[index]
        else:
            raise RuntimeError(f"Cannot index into a {type(obj).__name__}")
    
    def evaluate_property_access(self, expr):
        obj = self.evaluate(expr.obj)
        
        if isinstance(obj, ShravScriptModule):
            try:
                return obj.get_function(expr.prop)
            except AttributeError:
                # Better error handling for module functions
                functions_list = ", ".join(obj.functions.keys())
                raise AttributeError(f"Module '{obj.name}' has no function '{expr.prop}'. Available functions: {functions_list}")
        elif hasattr(obj, 'get'):
            return obj.get(expr.prop)
        elif hasattr(obj, expr.prop):
            return getattr(obj, expr.prop)
        else:
            raise AttributeError(f"'{type(obj).__name__}' has no attribute '{expr.prop}'")
    
    def evaluate_lambda(self, expr):
        # Create a function from the lambda
        return lambda interpreter, args: self.execute_lambda(expr, args)
    
    def execute_lambda(self, expr, args):
        # Set up the environment
        env = Environment(self.environment)
        
        # Bind parameters
        for i, param in enumerate(expr.params):
            if i < len(args):
                env.define(param, args[i])
            else:
                env.define(param, None)
        
        # Execute body
        try:
            self.execute_block(expr.body, env)
            return None
        except ReturnValue as return_value:
            return return_value.value
    
    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return True
    
    def stringify(self, value):
        if value is None:
            return "null"
        
        if isinstance(value, bool):
            return str(value).lower()
        
        if isinstance(value, (int, float)):
            text = str(value)
            # Remove trailing ".0" for float representation
            if text.endswith(".0"):
                text = text[:-2]
            return text
        
        if isinstance(value, str):
            # Handle string interpolation
            if "${" in value:
                def replace_var(match):
                    var_name = match.group(1)
                    try:
                        var_value = self.environment.get(var_name)
                        return str(var_value)
                    except:
                        return match.group(0)
                
                value = re.sub(r'\${([a-zA-Z_][a-zA-Z0-9_]*)}', replace_var, value)
            return value
        
        if isinstance(value, list):
            items = [self.stringify(item) for item in value]
            return f"[{', '.join(items)}]"
        
        if isinstance(value, dict):
            items = [f"{k}: {self.stringify(v)}" for k, v in value.items()]
            return f"{{{', '.join(items)}}}"
        
        return str(value)


def import_time():
    import time
    return time 

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass 