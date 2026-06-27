class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({self.statements})"

class VarDeclNode(ASTNode):
    def __init__(self, name, value, is_const=False):
        self.name = name
        self.value = value
        self.is_const = is_const

    def __repr__(self):
        prefix = "CONST " if self.is_const else "VAR "
        return f"VarDeclNode({prefix}{self.name} = {self.value})"

class AssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"AssignNode({self.name} = {self.value})"

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, elif_branches=None, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches if elif_branches is not None else []
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode(cond={self.condition}, then={self.then_branch}, elifs={self.elif_branches}, else={self.else_branch})"

class ElifNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"ElifNode(cond={self.condition}, body={self.body})"

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode(cond={self.condition}, body={self.body})"

class ForNode(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForNode(init={self.init}, cond={self.condition}, update={self.update}, body={self.body})"

class PrintNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value})"

class FuncDeclNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params  # List of parameter names (strings)
        self.body = body

    def __repr__(self):
        return f"FuncDeclNode({self.name}({', '.join(self.params)}) -> {self.body})"

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"

class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FuncCallNode({self.name}({self.args}))"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left} {self.op} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"UnaryOpNode({self.op} {self.expr})"

class LiteralNode(ASTNode):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type  # 'NUMBER', 'FLOAT', 'STRING', 'BOOLEAN'

    def __repr__(self):
        return f"LiteralNode({self.value_type}: {repr(self.value)})"

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VarNode({self.name})"
