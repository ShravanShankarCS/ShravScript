import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    EOF = auto()
    
class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class Tokenizer:
    KEYWORDS = {
        # Variable declaration and literals
        'let', 'const', 'null', 'true', 'false',
        
        # Control flow
        'if', 'elif', 'else', 'switch', 'case', 'default',
        'while', 'for', 'in', 'do', 'break', 'continue', 
        'return', 'yield', 'await', 'async',
        'try', 'catch', 'finally', 'throw', 'raise', 'assert',
        
        # Functions and scope
        'fn', 'lambda', 'global', 'nonlocal',
        
        # Class and OOP
        'class', 'this', 'new', 'public', 'private', 'protected',
        'virtual', 'override', 'operator',
        
        # Declarations
        'def', 'del', 'typedef',
        
        # Modules and imports
        'import', 'from', 'as', 'with', 'using',
        
        # Logical operators
        'and', 'or', 'not', 'is',
        
        # Bitwise operators
        'bitand', 'bitor', 'xor', 'not_eq', 'and_eq', 'or_eq', 'xor_eq',
        
        # Type system
        'int', 'float', 'string', 'bool', 'char', 'void', 'typeid', 'typename',
        
        # Memory and pointers
        'sizeof', 'decltype', 'nullptr', 'delete', 'const_cast',
        'static_cast', 'dynamic_cast', 'reinterpret_cast', 'thread_local', 'static_assert',
        
        # Concurrency
        'co_await', 'co_yield', 'co_return',
        
        # Namespaces
        'namespace',
        
        # Miscellaneous
        'pass', 'goto', 'register', 'inline',
        
        # Basic commands
        'print'
    }
    
    OPERATORS = {
        '+', '-', '*', '/', '%', '**', '=', '==', '!=', '<', '>', '<=', '>=',
        '.', '..', '=>', ':'
    }
    
    DELIMITERS = {
        '(', ')', '{', '}', '[', ']', ',', ';'
    }
    
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if self.source else None
    
    def advance(self):
        self.position += 1
        self.column += 1
        
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
    
    def peek(self, offset=1):
        peek_pos = self.position + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def tokenize(self):
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.advance()
                continue
            
            # Skip comments
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Tokenize strings
            if self.current_char == '"' or self.current_char == "'":
                self.tokens.append(self.tokenize_string())
                continue
            
            # Tokenize numbers
            if self.current_char.isdigit():
                self.tokens.append(self.tokenize_number())
                continue
            
            # Tokenize identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.tokenize_identifier())
                continue
            
            # Tokenize operators
            if self.is_operator_start():
                self.tokens.append(self.tokenize_operator())
                continue
            
            # Tokenize delimiters
            if self.current_char in self.DELIMITERS:
                self.tokens.append(Token(
                    TokenType.DELIMITER, 
                    self.current_char,
                    self.line,
                    self.column
                ))
                self.advance()
                continue
            
            # If we get here, we have an unrecognized character
            raise SyntaxError(f"Unrecognized character: '{self.current_char}' at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.line, self.column))
        return self.tokens
    
    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def tokenize_string(self):
        quote_type = self.current_char
        start_line, start_column = self.line, self.column
        self.advance()  # Skip the opening quote
        
        string_value = ""
        while self.current_char is not None and self.current_char != quote_type:
            if self.current_char == '\\' and self.peek() is not None:
                self.advance()  # Skip the backslash
                if self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                elif self.current_char == quote_type:
                    string_value += quote_type
                else:
                    string_value += '\\' + self.current_char
            else:
                string_value += self.current_char
            self.advance()
        
        if self.current_char is None:
            raise SyntaxError(f"Unterminated string at line {start_line}, column {start_column}")
        
        self.advance()  # Skip the closing quote
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def tokenize_number(self):
        start_line, start_column = self.line, self.column
        
        num_str = ""
        is_float = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:  # Already found a decimal point
                    break
                is_float = True
            num_str += self.current_char
            self.advance()
        
        if is_float:
            value = float(num_str)
        else:
            value = int(num_str)
        
        return Token(TokenType.NUMBER, value, start_line, start_column)
    
    def tokenize_identifier(self):
        start_line, start_column = self.line, self.column
        
        identifier = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        if identifier in self.KEYWORDS:
            token_type = TokenType.KEYWORD
        else:
            token_type = TokenType.IDENTIFIER
        
        return Token(token_type, identifier, start_line, start_column)
    
    def is_operator_start(self):
        for op in self.OPERATORS:
            if self.source[self.position:self.position + len(op)] == op:
                # Make sure we're not matching a prefix of a longer operator
                longer_op = False
                for long_op in self.OPERATORS:
                    if len(long_op) > len(op) and long_op.startswith(op) and self.source[self.position:self.position + len(long_op)] == long_op:
                        longer_op = True
                        break
                if not longer_op:
                    return True
        return False
    
    def tokenize_operator(self):
        start_line, start_column = self.line, self.column
        
        # Find the longest matching operator
        matched_op = None
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.position + len(op) <= len(self.source) and self.source[self.position:self.position + len(op)] == op:
                matched_op = op
                break
        
        if matched_op:
            for _ in range(len(matched_op)):
                self.advance()
            return Token(TokenType.OPERATOR, matched_op, start_line, start_column)
        
        # If we get here, there's an error
        raise SyntaxError(f"Unrecognized operator at line {start_line}, column {start_column}") 