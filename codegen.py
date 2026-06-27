from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, IfNode, ElifNode, WhileNode,
    ForNode, PrintNode, FuncDeclNode, ReturnNode, FuncCallNode,
    BinOpNode, UnaryOpNode, LiteralNode, VarNode
)

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def generate(self, node):
        """Metode utama rekursif untuk menghasilkan kode Python"""
        if node is None:
            return ""
        method_name = f"gen_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_gen)
        return visitor(node)

    def generic_gen(self, node):
        raise NotImplementedError(f"Metode gen_{type(node).__name__} durung diimplementasikan.")

    def gen_ProgramNode(self, node):
        # Tambahkan helper untuk operasi "+" agar mendukung penggabungan string & angka
        helpers = ""
        if self.indent_level == 0:
            helpers = (
                "# Helper kanggo operasi penjumlahan utawa penggabungan string\n"
                "def _tambah(a, b):\n"
                "    if isinstance(a, str) or isinstance(b, str):\n"
                "        return str(a) + str(b)\n"
                "    return a + b\n\n"
            )
            
        lines = []
        for stmt in node.statements:
            line_code = self.generate(stmt)
            if line_code:
                lines.append(line_code)
        
        if not lines:
            return self.indent() + "pass\n"
            
        return helpers + "".join(lines)

    def gen_VarDeclNode(self, node):
        val_code = self.generate(node.value)
        return f"{self.indent()}{node.name} = {val_code}\n"

    def gen_AssignNode(self, node):
        val_code = self.generate(node.value)
        return f"{self.indent()}{node.name} = {val_code}\n"

    def gen_PrintNode(self, node):
        val_code = self.generate(node.value)
        return f"{self.indent()}print({val_code})\n"

    def gen_ReturnNode(self, node):
        val_code = self.generate(node.value)
        return f"{self.indent()}return {val_code}\n"

    def gen_FuncDeclNode(self, node):
        params_str = ", ".join(node.params)
        header = f"{self.indent()}def {node.name}({params_str}):\n"
        
        # Tingkatkan indentasi untuk body fungsi
        self.indent_level += 1
        body_code = self.generate(node.body)
        self.indent_level -= 1
        
        return header + body_code

    def gen_IfNode(self, node):
        cond_code = self.generate(node.condition)
        code = f"{self.indent()}if {cond_code}:\n"
        
        # Body THEN
        self.indent_level += 1
        then_code = self.generate(node.then_branch)
        self.indent_level -= 1
        code += then_code
        
        # Elif Branches
        for elif_branch in node.elif_branches:
            elif_cond = self.generate(elif_branch.condition)
            code += f"{self.indent()}elif {elif_cond}:\n"
            self.indent_level += 1
            elif_body = self.generate(elif_branch.body)
            self.indent_level -= 1
            code += elif_body
            
        # Else Branch
        if node.else_branch:
            code += f"{self.indent()}else:\n"
            self.indent_level += 1
            else_code = self.generate(node.else_branch)
            self.indent_level -= 1
            code += else_code
            
        return code

    def gen_WhileNode(self, node):
        cond_code = self.generate(node.condition)
        code = f"{self.indent()}while {cond_code}:\n"
        
        self.indent_level += 1
        body_code = self.generate(node.body)
        self.indent_level -= 1
        code += body_code
        return code

    def gen_ForNode(self, node):
        # Transpilasikan kanggo (for-loop) C-style menjadi while-loop Python agar semantiknya tetap sama
        # kanggo (init; cond; update) { body } menjadi:
        # init
        # while cond:
        #     body
        #     update
        
        code = ""
        # 1. Output Statement Inisialisasi
        if node.init:
            code += self.generate(node.init)
            
        # 2. Output Header Loop
        cond_code = self.generate(node.condition) if node.condition else "True"
        code += f"{self.indent()}while {cond_code}:\n"
        
        # 3. Output Loop Body + Statement Update di bagian paling akhir body
        self.indent_level += 1
        body_code = self.generate(node.body)
        
        update_code = ""
        if node.update:
            # Karena node.update adalah statement, gen_AssignNode akan memberikan indentasi & newline otomatis
            update_code = self.generate(node.update)
            
        self.indent_level -= 1
        
        # Gabungkan body dan update
        # Jika body kosong, pasang 'pass' sebelum update
        if not body_code.strip():
            body_code = f"{self.indent() + '    '}pass\n"
            
        code += body_code + update_code
        return code

    # --- EKSPRESI ---

    def gen_FuncCallNode(self, node):
        args_code = [self.generate(arg) for arg in node.args]
        args_str = ", ".join(args_code)
        # Jika dipanggil sebagai ekspresi murni
        return f"{node.name}({args_str})"

    def gen_BinOpNode(self, node):
        left_code = self.generate(node.left)
        right_code = self.generate(node.right)
        
        op = node.op
        if op == '+':
            return f"_tambah({left_code}, {right_code})"
            
        # Terjemahkan operator logika BosoJowo ke Python
        if op == 'lan':
            op = 'and'
        elif op == 'utawa':
            op = 'or'
            
        return f"({left_code} {op} {right_code})"

    def gen_UnaryOpNode(self, node):
        expr_code = self.generate(node.expr)
        
        op = node.op
        if op == 'ora':
            op = 'not'
            
        return f"({op} {expr_code})"

    def gen_LiteralNode(self, node):
        if node.value_type in ('TRUE', 'FALSE') or isinstance(node.value, bool):
            return "True" if node.value else "False"
        elif node.value_type == 'STRING' or isinstance(node.value, str):
            return repr(node.value)
        return str(node.value)

    def gen_VarNode(self, node):
        return node.name

if __name__ == '__main__':
    # Uji coba Code Generator
    from lexer import lexer
    from parser_ast import Parser
    from optimizer import ASTOptimizer
    
    test_code = """
    fungsi tambah(a, b) {
        balekno a + b;
    }
    
    wadah x = tambah(10, 20);
    
    yen (x > 15 lan bener) {
        tulis("Luwih gede!");
    } liyane {
        tulis("Luwih cilik!");
    }
    
    // Uji coba C-Style Loop kanggo
    kanggo (wadah i = 0; i < 3; i = i + 1) {
        tulis(i);
    }
    """
    
    tokens, errs = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    
    optimizer = ASTOptimizer()
    optimized_ast = optimizer.optimize(ast)
    
    codegen = CodeGenerator()
    python_code = codegen.generate(optimized_ast)
    
    print("--- HASIL KODE PYTHON ---")
    print(python_code)
