class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing
    
    def define(self, name, value):
        self.values[name] = value
    
    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return True
        
        if self.enclosing is not None:
            return self.enclosing.assign(name, value)
        
        raise NameError(f"Undefined variable '{name}'")
    
    def get(self, name):
        if name in self.values:
            return self.values[name]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise NameError(f"Undefined variable '{name}'")
    
    def get_at(self, distance, name):
        return self.ancestor(distance).values.get(name)
    
    def assign_at(self, distance, name, value):
        self.ancestor(distance).values[name] = value
    
    def ancestor(self, distance):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment


class ShravScriptFunction:
    def __init__(self, declaration, closure, is_initializer=False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
    
    def __call__(self, interpreter, arguments):
        environment = Environment(self.closure)
        
        for i, param in enumerate(self.declaration.params):
            if i < len(arguments):
                environment.define(param, arguments[i])
            else:
                environment.define(param, None)  # Default parameter value
        
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnValue as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(self)


class ShravScriptClass:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods
    
    def __str__(self):
        return self.name
    
    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        return None
    
    def __call__(self, interpreter, arguments):
        instance = ShravScriptInstance(self)
        
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance)(interpreter, arguments)
        
        return instance


class ShravScriptInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}
    
    def __str__(self):
        return f"{self.klass.name} instance"
    
    def get(self, name):
        if name in self.fields:
            return self.fields[name]
        
        method = self.klass.find_method(name)
        if method is not None:
            return method.bind(self)
        
        raise AttributeError(f"Undefined property '{name}'")
    
    def set(self, name, value):
        self.fields[name] = value


class ShravScriptCallable:
    def arity(self):
        pass
    
    def __call__(self, interpreter, arguments):
        pass


class ShravScriptNativeFunction(ShravScriptCallable):
    def __init__(self, arity, fn):
        self.arity_count = arity
        self.function = fn
    
    def arity(self):
        return self.arity_count
    
    def __call__(self, interpreter, arguments):
        return self.function(*arguments)
    
    def __str__(self):
        return "<native fn>"


class ShravScriptModule:
    def __init__(self, name, functions=None):
        self.name = name
        self.functions = functions or {}
    
    def add_function(self, name, function):
        self.functions[name] = function
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        raise AttributeError(f"Module '{self.name}' has no function '{name}'")
    
    def __str__(self):
        return f"<module '{self.name}'>" 