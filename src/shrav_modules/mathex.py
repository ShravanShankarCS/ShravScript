import math
import random
from environment import ShravScriptModule, ShravScriptNativeFunction

def create_module(interpreter):
    module = ShravScriptModule("mathex")
    
    # Square root function
    def sqrt_fn(x):
        try:
            return math.sqrt(x)
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Power function
    def pow_fn(x, y):
        try:
            return math.pow(x, y)
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Random number function (0.0 to 1.0)
    def random_fn():
        return random.random()
    
    # Trigonometric functions
    def sin_fn(x):
        return math.sin(x)
    
    def cos_fn(x):
        return math.cos(x)
    
    def tan_fn(x):
        return math.tan(x)
    
    module.add_function("sqrt", ShravScriptNativeFunction(1, sqrt_fn))
    module.add_function("pow", ShravScriptNativeFunction(2, pow_fn))
    module.add_function("random", ShravScriptNativeFunction(0, random_fn))
    module.add_function("sin", ShravScriptNativeFunction(1, sin_fn))
    module.add_function("cos", ShravScriptNativeFunction(1, cos_fn))
    module.add_function("tan", ShravScriptNativeFunction(1, tan_fn))
    
    return module 