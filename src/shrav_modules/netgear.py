import requests
from environment import ShravScriptModule, ShravScriptNativeFunction

def create_module(interpreter):
    module = ShravScriptModule("netgear")
    
    # HTTP GET function
    def get_fn(url):
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    # HTTP POST function
    def post_fn(url, body=None):
        try:
            response = requests.post(url, json=body)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    # HTTP headers function
    def headers_fn(headers=None):
        if headers is None:
            return {"User-Agent": "ShravScript/1.0"}
        return headers
    
    module.add_function("get", ShravScriptNativeFunction(1, get_fn))
    module.add_function("post", ShravScriptNativeFunction(2, post_fn))
    module.add_function("headers", ShravScriptNativeFunction(1, headers_fn))
    
    return module 