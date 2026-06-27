from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, IfNode, ElifNode, WhileNode,
    ForNode, PrintNode, FuncDeclNode, ReturnNode, FuncCallNode,
    BinOpNode, UnaryOpNode, LiteralNode, VarNode
)

class ASTOptimizer:
    def optimize(self, node):
        """Metode rekursif utama untuk optimasi node AST"""
        if node is None:
            return None
            
        method_name = f"optimize_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_optimize)
        return visitor(node)

    def generic_optimize(self, node):
        # Secara default, jika tidak ada logika khusus, biarkan node apa adanya
        # Namun pastikan kita mengoptimalkan node anak-anaknya jika ada.
        for attr, value in list(node.__dict__.items()):
            if isinstance(value, list):
                new_list = []
                for item in value:
                    opt_item = self.optimize(item)
                    if opt_item is not None:
                        new_list.append(opt_item)
                setattr(node, attr, new_list)
            elif hasattr(value, '__class__') and issubclass(value.__class__, getattr(node.__class__, '__mro__')[1]):
                # Jika property adalah ASTNode, optimasi
                setattr(node, attr, self.optimize(value))
        return node

    def optimize_ProgramNode(self, node):
        new_statements = []
        for stmt in node.statements:
            opt_stmt = self.optimize(stmt)
            if opt_stmt is not None:
                new_statements.append(opt_stmt)
        node.statements = new_statements
        return node

    def optimize_VarDeclNode(self, node):
        node.value = self.optimize(node.value)
        return node

    def optimize_AssignNode(self, node):
        node.value = self.optimize(node.value)
        return node

    def optimize_BinOpNode(self, node):
        # Optimasi anak-anak terlebih dahulu (dari bawah ke atas)
        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)
        
        # Lakukan Constant Folding jika kedua sisi adalah LiteralNode
        if isinstance(node.left, LiteralNode) and isinstance(node.right, LiteralNode):
            lval = node.left.value
            rval = node.right.value
            op = node.op
            
            try:
                # Operasi Matematika
                if op == '+':
                    if isinstance(lval, (int, float)) and isinstance(rval, (int, float)):
                        t = 'NUMBER' if isinstance(lval, int) and isinstance(rval, int) else 'FLOAT'
                        return LiteralNode(lval + rval, t)
                    elif isinstance(lval, str) or isinstance(rval, str):
                        # Penggabungan string statis
                        return LiteralNode(str(lval) + str(rval), 'STRING')
                elif op == '-':
                    t = 'NUMBER' if isinstance(lval, int) and isinstance(rval, int) else 'FLOAT'
                    return LiteralNode(lval - rval, t)
                elif op == '*':
                    t = 'NUMBER' if isinstance(lval, int) and isinstance(rval, int) else 'FLOAT'
                    return LiteralNode(lval * rval, t)
                elif op == '/':
                    # Hindari pembagian dengan nol saat compile-time
                    if rval != 0:
                        return LiteralNode(lval / rval, 'FLOAT')
                        
                # Operasi Perbandingan
                elif op == '==':
                    return LiteralNode(lval == rval, 'TRUE' if (lval == rval) else 'FALSE')
                elif op == '!=':
                    return LiteralNode(lval != rval, 'TRUE' if (lval != rval) else 'FALSE')
                elif op == '<':
                    return LiteralNode(lval < rval, 'TRUE' if (lval < rval) else 'FALSE')
                elif op == '>':
                    return LiteralNode(lval > rval, 'TRUE' if (lval > rval) else 'FALSE')
                elif op == '<=':
                    return LiteralNode(lval <= rval, 'TRUE' if (lval <= rval) else 'FALSE')
                elif op == '>=':
                    return LiteralNode(lval >= rval, 'TRUE' if (lval >= rval) else 'FALSE')
                    
                # Operasi Logika
                elif op == 'lan':
                    res = bool(lval and rval)
                    return LiteralNode(res, 'TRUE' if res else 'FALSE')
                elif op == 'utawa':
                    res = bool(lval or rval)
                    return LiteralNode(res, 'TRUE' if res else 'FALSE')
            except Exception:
                # Jika terjadi error (misal tipe tak cocok), biarkan compiler semantik menangkapnya
                pass
                
        return node

    def optimize_UnaryOpNode(self, node):
        node.expr = self.optimize(node.expr)
        
        # Constant folding untuk Unary (Negasi / Minus)
        if isinstance(node.expr, LiteralNode):
            val = node.expr.value
            if node.op == 'ora':
                res = not val
                return LiteralNode(res, 'TRUE' if res else 'FALSE')
            elif node.op == '-':
                if isinstance(val, (int, float)):
                    t = 'NUMBER' if isinstance(val, int) else 'FLOAT'
                    return LiteralNode(-val, t)
                    
        return node

    def optimize_IfNode(self, node):
        node.condition = self.optimize(node.condition)
        node.then_branch = self.optimize(node.then_branch)
        
        # Optimasi Elif
        new_elifs = []
        for elif_branch in node.elif_branches:
            opt_elif = self.optimize(elif_branch)
            if opt_elif is not None:
                new_elifs.append(opt_elif)
        node.elif_branches = new_elifs
        
        if node.else_branch:
            node.else_branch = self.optimize(node.else_branch)
            
        # Dead Branch Elimination
        if isinstance(node.condition, LiteralNode):
            cond_val = node.condition.value
            if cond_val is True:
                # Jika kondisi selalu BENER, kembalikan body program di dalam branch THEN
                return node.then_branch
            elif cond_val is False:
                # Jika kondisi selalu SALAH:
                # 1. Jika ada elif, ubah IfNode ini dengan mengecek elif pertama
                if node.elif_branches:
                    first_elif = node.elif_branches[0]
                    # Sisanya dipasang sebagai elif/else dari if yang baru
                    remaining_elifs = node.elif_branches[1:]
                    return IfNode(first_elif.condition, first_elif.body, remaining_elifs, node.else_branch)
                # 2. Jika tidak ada elif tapi ada else, kembalikan else branch
                elif node.else_branch:
                    return node.else_branch
                # 3. Jika tidak ada liyane, hilangkan seluruh percabangan
                else:
                    return None
                    
        return node

    def optimize_ElifNode(self, node):
        node.condition = self.optimize(node.condition)
        node.body = self.optimize(node.body)
        return node

    def optimize_WhileNode(self, node):
        node.condition = self.optimize(node.condition)
        node.body = self.optimize(node.body)
        
        # Dead Loop Elimination
        if isinstance(node.condition, LiteralNode) and node.condition.value is False:
            # Loop suwene(salah) tidak akan pernah dijalankan
            return None
            
        return node

    def optimize_ForNode(self, node):
        if node.init:
            node.init = self.optimize(node.init)
        if node.condition:
            node.condition = self.optimize(node.condition)
        if node.update:
            node.update = self.optimize(node.update)
        node.body = self.optimize(node.body)
        
        # Dead Loop Elimination untuk FOR
        if isinstance(node.condition, LiteralNode) and node.condition.value is False:
            return None
            
        return node

    def optimize_PrintNode(self, node):
        node.value = self.optimize(node.value)
        return node

    def optimize_FuncDeclNode(self, node):
        node.body = self.optimize(node.body)
        return node

    def optimize_ReturnNode(self, node):
        node.value = self.optimize(node.value)
        return node

    def optimize_FuncCallNode(self, node):
        new_args = []
        for arg in node.args:
            new_args.append(self.optimize(arg))
        node.args = new_args
        return node

if __name__ == '__main__':
    # Uji coba optimasi
    from lexer import lexer
    from parser_ast import Parser
    
    test_code = """
    wadah hasil = (2 + 3) * 4; // Constant folding: kudu dadi 20
    
    yen (bener) {
        tulis("Iki bakal muncul");
    } liyane {
        tulis("Iki dadi dead code lan dihapus");
    }
    
    suwene (salah) {
        tulis("Iki perulangan mati, kudu dihapus");
    }
    """
    
    tokens, errs = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("--- AST Sakdurunge Dioptimasi (Sebelum) ---")
    print(ast)
    
    optimizer = ASTOptimizer()
    optimized_ast = optimizer.optimize(ast)
    
    print("\n--- AST Sakwise Dioptimasi (Sesudah) ---")
    print(optimized_ast)
