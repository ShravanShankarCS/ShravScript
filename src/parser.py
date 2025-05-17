from tokenizer import TokenType

class Node:
    pass

class Program(Node):
    def __init__(self, statements=None):
        self.statements = statements or []
    
    def add_statement(self, statement):
        self.statements.append(statement)

class BinaryOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class Literal(Node):
    def __init__(self, value):
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class VariableDeclaration(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Assignment(Node):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class FunctionDeclaration(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Return(Node):
    def __init__(self, value):
        self.value = value

class IfStatement(Node):
    def __init__(self, condition, if_body, elif_conditions=None, elif_bodies=None, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.elif_conditions = elif_conditions or []
        self.elif_bodies = elif_bodies or []
        self.else_body = else_body

class WhileLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoop(Node):
    def __init__(self, var_name, range_start, range_end, body):
        self.var_name = var_name
        self.range_start = range_start
        self.range_end = range_end
        self.body = body

class ListLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

class DictLiteral(Node):
    def __init__(self, items):
        self.items = items

class IndexAccess(Node):
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

class PropertyAccess(Node):
    def __init__(self, obj, prop):
        self.obj = obj
        self.prop = prop

class LambdaExpression(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class TryCatch(Node):
    def __init__(self, try_body, catch_var, catch_body):
        self.try_body = try_body
        self.catch_var = catch_var
        self.catch_body = catch_body

class ImportStatement(Node):
    def __init__(self, module_name):
        self.module_name = module_name

class ClassDeclaration(Node):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

class Print(Node):
    def __init__(self, value):
        self.value = value

class BreakStatement(Node):
    pass

class ContinueStatement(Node):
    pass

class WithStatement(Node):
    def __init__(self, expression, var_name, body):
        self.expression = expression
        self.var_name = var_name
        self.body = body

class SwitchStatement(Node):
    def __init__(self, expression, cases, values, bodies, default_body=None):
        self.expression = expression
        self.cases = cases
        self.values = values
        self.bodies = bodies
        self.default_body = default_body

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return Program(statements)
    
    def statement(self):
        if self.match(TokenType.KEYWORD, 'let'):
            return self.variable_declaration()
        elif self.match(TokenType.KEYWORD, 'fn'):
            # Create a function declaration
            # Get the function name
            if not self.check(TokenType.IDENTIFIER):
                self.error(self.peek(), "Expected function name")
            
            name = self.advance().value  # directly advance to get the identifier
            
            # Parse parameters
            self.consume(TokenType.DELIMITER, '(', "Expected '(' after function name")
            
            params = []
            if not self.check(TokenType.DELIMITER, ')'):
                while True:
                    if not self.check(TokenType.IDENTIFIER):
                        self.error(self.peek(), "Expected parameter name")
                    
                    param = self.advance().value
                    params.append(param)
                    
                    if not self.match(TokenType.DELIMITER, ','):
                        break
            
            self.consume(TokenType.DELIMITER, ')', "Expected ')' after parameters")
            
            # Parse function body
            self.consume(TokenType.DELIMITER, '{', "Expected '{' before function body")
            
            body = self.block()
            return FunctionDeclaration(name, params, body)
        elif self.match(TokenType.KEYWORD, 'if'):
            return self.if_statement()
        elif self.match(TokenType.KEYWORD, 'switch'):
            return self.switch_statement()
        elif self.match(TokenType.KEYWORD, 'while'):
            return self.while_loop()
        elif self.match(TokenType.KEYWORD, 'for'):
            return self.for_loop()
        elif self.match(TokenType.KEYWORD, 'with'):
            return self.with_statement()
        elif self.match(TokenType.KEYWORD, 'break'):
            self.consume_optional(TokenType.DELIMITER, ';')
            return BreakStatement()
        elif self.match(TokenType.KEYWORD, 'continue'):
            self.consume_optional(TokenType.DELIMITER, ';')
            return ContinueStatement()
        elif self.match(TokenType.KEYWORD, 'return'):
            return self.return_statement()
        elif self.match(TokenType.KEYWORD, 'try'):
            return self.try_catch()
        elif self.match(TokenType.KEYWORD, 'import'):
            return self.import_statement()
        elif self.match(TokenType.KEYWORD, 'class'):
            return self.class_declaration()
        elif self.match(TokenType.KEYWORD, 'print'):
            return self.print_statement()
        else:
            return self.expression_statement()
    
    def variable_declaration(self):
        if not self.check(TokenType.IDENTIFIER):
            self.error(self.peek(), "Expected variable name after 'let'")
        
        name = self.advance().value
        value = None
        
        if self.match(TokenType.OPERATOR, '='):
            value = self.expression()
        
        self.consume_optional(TokenType.DELIMITER, ';')
        return VariableDeclaration(name, value)
    
    def if_statement(self):
        condition = self.expression()
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after if condition")
        if_body = self.block()
        
        elif_conditions = []
        elif_bodies = []
        
        # Handle multiple elif blocks
        while self.match(TokenType.KEYWORD, 'elif'):
            elif_condition = self.expression()
            self.consume(TokenType.DELIMITER, '{', "Expected '{' after elif condition")
            elif_body = self.block()
            
            elif_conditions.append(elif_condition)
            elif_bodies.append(elif_body)
        
        # Handle the optional else block
        else_body = None
        if self.match(TokenType.KEYWORD, 'else'):
            self.consume(TokenType.DELIMITER, '{', "Expected '{' after else")
            else_body = self.block()
        
        return IfStatement(condition, if_body, elif_conditions, elif_bodies, else_body)
    
    def switch_statement(self):
        self.consume(TokenType.DELIMITER, '(', "Expected '(' after switch")
        expression = self.expression()
        self.consume(TokenType.DELIMITER, ')', "Expected ')' after switch expression")
        
        cases = []  # To store the 'case' keyword position
        values = []  # To store the case values
        bodies = []  # To store the case bodies
        default_body = None
        
        # Parse the actual cases
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after switch expression")
        
        while not self.check(TokenType.DELIMITER, '}') and not self.is_at_end():
            if self.match(TokenType.KEYWORD, 'case'):
                cases.append('case')
                
                # Parse the case value
                value = self.expression()
                values.append(value)
                
                self.consume(TokenType.DELIMITER, '{', "Expected '{' after case value")
                body = self.block()
                bodies.append(body)
            elif self.match(TokenType.KEYWORD, 'default'):
                self.consume(TokenType.DELIMITER, '{', "Expected '{' after default")
                default_body = self.block()
            else:
                self.error(self.peek(), "Expected 'case' or 'default' in switch statement")
        
        self.consume(TokenType.DELIMITER, '}', "Expected '}' after switch statement")
        
        return SwitchStatement(expression, cases, values, bodies, default_body)
    
    def while_loop(self):
        condition = self.expression()
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after while condition")
        body = self.block()
        
        return WhileLoop(condition, body)
    
    def for_loop(self):
        if not self.check(TokenType.IDENTIFIER):
            self.error(self.peek(), "Expected variable name in for loop")
        
        var_name = self.advance().value
        
        self.consume(TokenType.KEYWORD, 'in', "Expected 'in' keyword in for loop")
        
        range_start = self.expression()
        
        # Handle both '..' and '...' range operators
        if self.match(TokenType.OPERATOR, '..'):
            range_end = self.expression()
        else:
            self.error(self.peek(), "Expected '..' operator in range")
            return None
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after for loop range")
        body = self.block()
        
        return ForLoop(var_name, range_start, range_end, body)
    
    def return_statement(self):
        value = None
        if not self.check(TokenType.DELIMITER, ';') and not self.check(TokenType.DELIMITER, '}'):
            value = self.expression()
        
        self.consume_optional(TokenType.DELIMITER, ';')
        return Return(value)
    
    def try_catch(self):
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after try")
        try_body = self.block()
        
        self.consume(TokenType.KEYWORD, 'catch', "Expected 'catch' after try block")
        self.consume(TokenType.DELIMITER, '(', "Expected '(' after catch")
        
        # Allow both identifiers and keywords for exception variable names
        if self.check(TokenType.IDENTIFIER):
            catch_var = self.advance().value
        elif self.check(TokenType.KEYWORD):
            catch_var = self.advance().value
        else:
            self.error(self.peek(), "Expected exception variable name")
            catch_var = "error"  # Default name
        
        self.consume(TokenType.DELIMITER, ')', "Expected ')' after catch variable")
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after catch")
        catch_body = self.block()
        
        return TryCatch(try_body, catch_var, catch_body)
    
    def import_statement(self):
        # Check if the next token is a string literal (for import "module")
        if self.check(TokenType.STRING):
            module_name = self.advance().value
        # Otherwise check for an identifier (for import module)
        elif self.check(TokenType.IDENTIFIER):
            module_name = self.advance().value
        else:
            self.error(self.peek(), "Expected module name as string or identifier")
            
        self.consume_optional(TokenType.DELIMITER, ';')
        return ImportStatement(module_name)
    
    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected class name").value
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after class name")
        
        methods = []
        while not self.check(TokenType.DELIMITER, '}') and not self.is_at_end():
            # Parse method declarations within the class
            if self.match(TokenType.KEYWORD, 'fn'):
                # Get method name directly
                if not self.check(TokenType.IDENTIFIER):
                    self.error(self.peek(), "Expected method name")
                
                method_name = self.advance().value
                
                # Parse parameters
                self.consume(TokenType.DELIMITER, '(', "Expected '(' after method name")
                
                params = []
                if not self.check(TokenType.DELIMITER, ')'):
                    while True:
                        if not self.check(TokenType.IDENTIFIER):
                            self.error(self.peek(), "Expected parameter name")
                        
                        param = self.advance().value
                        params.append(param)
                        
                        if not self.match(TokenType.DELIMITER, ','):
                            break
                
                self.consume(TokenType.DELIMITER, ')', "Expected ')' after parameters")
                
                # Parse method body
                self.consume(TokenType.DELIMITER, '{', "Expected '{' before method body")
                
                body = self.block()
                methods.append(FunctionDeclaration(method_name, params, body))
            else:
                # Skip invalid tokens
                self.error(self.peek(), "Expected method declaration starting with 'fn'")
                self.advance()
        
        self.consume(TokenType.DELIMITER, '}', "Expected '}' after class body")
        return ClassDeclaration(name, methods)
    
    def print_statement(self):
        self.consume(TokenType.DELIMITER, '(', "Expected '(' after print")
        value = self.expression()
        self.consume(TokenType.DELIMITER, ')', "Expected ')' after print value")
        self.consume_optional(TokenType.DELIMITER, ';')
        return Print(value)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume_optional(TokenType.DELIMITER, ';')
        return expr
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.or_expr()
        
        if self.match(TokenType.OPERATOR, '='):
            value = self.assignment()
            
            if isinstance(expr, Identifier) or isinstance(expr, PropertyAccess) or isinstance(expr, IndexAccess):
                return Assignment(expr, value)
            
            self.error(self.previous(), "Invalid assignment target")
        
        return expr
    
    def or_expr(self):
        expr = self.and_expr()
        
        while self.match(TokenType.KEYWORD, 'or'):
            operator = self.previous().value
            right = self.and_expr()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def and_expr(self):
        expr = self.equality()
        
        while self.match(TokenType.KEYWORD, 'and'):
            operator = self.previous().value
            right = self.equality()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def equality(self):
        expr = self.comparison()
        
        while self.match_any(TokenType.OPERATOR, ['==', '!=']):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def comparison(self):
        expr = self.addition()
        
        while self.match_any(TokenType.OPERATOR, ['<', '>', '<=', '>=']):
            operator = self.previous().value
            right = self.addition()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def addition(self):
        expr = self.multiplication()
        
        while self.match_any(TokenType.OPERATOR, ['+', '-']):
            operator = self.previous().value
            right = self.multiplication()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def multiplication(self):
        expr = self.unary()
        
        while self.match_any(TokenType.OPERATOR, ['*', '/', '%']):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def unary(self):
        if self.match_any(TokenType.OPERATOR, ['-']) or self.match_any(TokenType.KEYWORD, ['not']):
            operator = self.previous().value
            right = self.unary()
            return UnaryOp(operator, right)
        
        return self.power()
    
    def power(self):
        expr = self.call()
        
        if self.match(TokenType.OPERATOR, '**'):
            right = self.unary()  # Right-associative
            return BinaryOp(expr, '**', right)
        
        return expr
    
    def call(self):
        expr = self.primary()
        
        while True:
            if self.match(TokenType.DELIMITER, '('):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DELIMITER, '['):
                index = self.expression()
                self.consume(TokenType.DELIMITER, ']', "Expected ']' after index")
                expr = IndexAccess(expr, index)
            elif self.match(TokenType.OPERATOR, '.'):
                # Check if we have an identifier
                if self.check(TokenType.IDENTIFIER):
                    name = self.advance()
                    expr = PropertyAccess(expr, name.value)
                else:
                    # Allow keywords and other identifiers after dot notation for method names
                    if self.check(TokenType.KEYWORD) or self.check(TokenType.IDENTIFIER):
                        name = self.advance()
                        expr = PropertyAccess(expr, name.value)
                    else:
                        self.error(self.peek(), "Expected property name after '.'")
            else:
                break
        
        return expr
    
    def finish_call(self, callee):
        args = []
        
        if not self.check(TokenType.DELIMITER, ')'):
            while True:
                args.append(self.expression())
                
                if not self.match(TokenType.DELIMITER, ','):
                    break
        
        self.consume(TokenType.DELIMITER, ')', "Expected ')' after arguments")
        return FunctionCall(callee, args)
    
    def primary(self):
        if self.match(TokenType.KEYWORD, 'true'):
            return Literal(True)
        if self.match(TokenType.KEYWORD, 'false'):
            return Literal(False)
        if self.match(TokenType.KEYWORD, 'null'):
            return Literal(None)
        
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().value)
        
        if self.match(TokenType.STRING):
            return Literal(self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().value)
        
        if self.match(TokenType.DELIMITER, '('):
            expr = self.expression()
            self.consume(TokenType.DELIMITER, ')', "Expected ')' after expression")
            return expr
        
        if self.match(TokenType.DELIMITER, '['):
            return self.list_literal()
        
        if self.match(TokenType.DELIMITER, '{'):
            # Could be either a block or an object literal
            if self.check(TokenType.IDENTIFIER) and self.check_next(TokenType.OPERATOR, ':'):
                return self.dict_literal()
            else:
                self.current -= 1  # Put back the '{' token
                return self.error(self.peek(), "Unexpected '{'")
        
        if self.match(TokenType.DELIMITER, '('):
            # Lambda expression
            params = []
            
            if not self.check(TokenType.DELIMITER, ')'):
                while True:
                    params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
                    
                    if not self.match(TokenType.DELIMITER, ','):
                        break
            
            self.consume(TokenType.DELIMITER, ')', "Expected ')' after parameters")
            self.consume(TokenType.OPERATOR, '=>', "Expected '=>' in lambda expression")
            
            if self.match(TokenType.DELIMITER, '{'):
                body = self.block()
                return LambdaExpression(params, body)
            else:
                body = [Return(self.expression())]
                return LambdaExpression(params, body)
        
        return self.error(self.peek(), "Expected expression")
    
    def list_literal(self):
        elements = []
        
        if not self.check(TokenType.DELIMITER, ']'):
            while True:
                elements.append(self.expression())
                
                if not self.match(TokenType.DELIMITER, ','):
                    break
        
        self.consume(TokenType.DELIMITER, ']', "Expected ']' after list elements")
        return ListLiteral(elements)
    
    def dict_literal(self):
        items = {}
        
        if not self.check(TokenType.DELIMITER, '}'):
            while True:
                key = self.consume(TokenType.IDENTIFIER, "Expected property name").value
                self.consume(TokenType.OPERATOR, ':', "Expected ':' after property name")
                value = self.expression()
                
                items[key] = value
                
                if not self.match(TokenType.DELIMITER, ','):
                    break
        
        self.consume(TokenType.DELIMITER, '}', "Expected '}' after object properties")
        return DictLiteral(items)
    
    def block(self):
        statements = []
        
        while not self.check(TokenType.DELIMITER, '}') and not self.is_at_end():
            statements.append(self.statement())
        
        self.consume(TokenType.DELIMITER, '}', "Expected '}' after block")
        return statements
    
    def with_statement(self):
        expression = self.expression()
        self.consume(TokenType.KEYWORD, 'as', "Expected 'as' after with expression")
        
        if not self.check(TokenType.IDENTIFIER):
            self.error(self.peek(), "Expected variable name after 'as'")
        
        var_name = self.advance().value
        
        self.consume(TokenType.DELIMITER, '{', "Expected '{' after with statement")
        body = self.block()
        
        return WithStatement(expression, var_name, body)
    
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def peek_next(self):
        if self.current + 1 >= len(self.tokens):
            return None
        return self.tokens[self.current + 1]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def check(self, token_type, value=None):
        if self.is_at_end():
            return False
        
        if value is not None:
            return self.peek().type == token_type and self.peek().value == value
        else:
            return self.peek().type == token_type
    
    def check_next(self, token_type, value=None):
        next_token = self.peek_next()
        if next_token is None:
            return False
        
        if value is not None:
            return next_token.type == token_type and next_token.value == value
        else:
            return next_token.type == token_type
    
    def match(self, token_type, value=None):
        if self.check(token_type, value):
            self.advance()
            return True
        return False
    
    def match_any(self, token_type, values):
        for value in values:
            if self.check(token_type, value):
                self.advance()
                return True
        return False
    
    def consume(self, token_type, value=None, error_message=None):
        if self.check(token_type, value):
            return self.advance()
        
        error_msg = error_message or f"Expected {token_type}" + (f" '{value}'" if value else "")
        return self.error(self.peek(), error_msg)
    
    def consume_optional(self, token_type, value=None):
        if self.check(token_type, value):
            self.advance()
            return True
        return False
    
    def error(self, token, message):
        line = token.line if hasattr(token, 'line') else "?"
        col = token.column if hasattr(token, 'column') else "?"
        token_text = token.value if hasattr(token, 'value') else str(token)
        
        raise SyntaxError(f"{message} at line {line}, column {col} (got '{token_text}')") 