from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, IfNode, ElifNode, WhileNode,
    ForNode, PrintNode, FuncDeclNode, ReturnNode, FuncCallNode,
    BinOpNode, UnaryOpNode, LiteralNode, VarNode
)

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        # Menyimpan daftar scope (dimulai dengan scope global)
        self.scopes = [{}]
        # Menyimpan fungsi yang dideklarasikan
        self.functions = {}

    def current_scope(self):
        return self.scopes[-1]

    def lookup_var(self, name):
        # Cari variabel dari scope terdalam ke terluar
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def declare_var(self, name, var_type, is_const=False):
        self.current_scope()[name] = {'type': var_type, 'is_const': is_const}

    def analyze(self, node):
        """Metode utama untuk menjalankan analisis secara rekursif"""
        method_name = f"analyze_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_analyze)
        return visitor(node)

    def generic_analyze(self, node):
        if hasattr(node, 'statements'):
            for stmt in node.statements:
                self.analyze(stmt)
        return None

    def analyze_ProgramNode(self, node):
        for stmt in node.statements:
            self.analyze(stmt)
        return None

    def analyze_VarDeclNode(self, node):
        # Pastikan variabel belum dideklarasikan di scope yang sama
        if node.name in self.current_scope():
            raise SemanticError(f"Variabel '{node.name}' wis dideklarasikake (sudah dideklarasikan) ing scope iki.")
        
        val_type = self.analyze(node.value)
        is_const = getattr(node, 'is_const', False)
        self.declare_var(node.name, val_type, is_const=is_const)
        return None

    def analyze_AssignNode(self, node):
        # Pastikan variabel sudah dideklarasikan sebelumnya
        var_info = self.lookup_var(node.name)
        if var_info is None:
            raise SemanticError(f"Variabel '{node.name}' durung dideklarasikake (belum dideklarasikan).")
        
        if var_info.get('is_const'):
            raise SemanticError(f"Variabel '{node.name}' iku ginaris (konstanta), ora bisa diowahi (tidak bisa diubah).")
        
        val_type = self.analyze(node.value)
        return None

    def analyze_VarNode(self, node):
        # Pastikan variabel terdefinisi
        var_info = self.lookup_var(node.name)
        if var_info is None:
            raise SemanticError(f"Variabel '{node.name}' durung dideklarasikake (belum dideklarasikan).")
        return var_info['type']

    def analyze_LiteralNode(self, node):
        # Mengembalikan tipe data literal
        return node.value_type

    def analyze_BinOpNode(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        # Aturan tipe data sederhana
        if node.op in ('+', '-', '*', '/'):
            # Jika salah satu operand bertipe ANY, maka hasil operasi bertipe ANY
            if left_type == 'ANY' or right_type == 'ANY':
                return 'ANY'
            # Perkalian, pengurangan, pembagian string tidak diperbolehkan
            if node.op in ('-', '*', '/'):
                if left_type == 'STRING' or right_type == 'STRING':
                    raise SemanticError(
                        f"Operasi aritmatika '{node.op}' ora kena kanggo tipe data STRING."
                    )
            # Penjumlahan (penggabungan) diperbolehkan
            return 'NUMBER' if left_type == 'NUMBER' and right_type == 'NUMBER' else 'STRING'
            
        elif node.op in ('==', '!=', '<', '>', '<=', '>='):
            return 'BOOLEAN'
            
        elif node.op in ('lan', 'utawa'):
            return 'BOOLEAN'
            
        return left_type

    def analyze_UnaryOpNode(self, node):
        expr_type = self.analyze(node.expr)
        if node.op == 'ora':
            if expr_type != 'BOOLEAN':
                # Opsional: kita bisa meloloskannya atau memperingatkan tipe data
                pass
            return 'BOOLEAN'
        return expr_type

    def analyze_IfNode(self, node):
        self.analyze(node.condition)
        
        # Jalankan analisis pada then branch
        self.analyze(node.then_branch)
        
        # Jalankan analisis pada elif branches
        for elif_branch in node.elif_branches:
            self.analyze(elif_branch)
            
        # Jalankan analisis pada else branch jika ada
        if node.else_branch:
            self.analyze(node.else_branch)
        return None

    def analyze_ElifNode(self, node):
        self.analyze(node.condition)
        self.analyze(node.body)
        return None

    def analyze_WhileNode(self, node):
        self.analyze(node.condition)
        self.analyze(node.body)
        return None

    def analyze_ForNode(self, node):
        # Inisialisasi loop
        if node.init:
            self.analyze(node.init)
        # Kondisi loop
        if node.condition:
            self.analyze(node.condition)
        # Update loop
        if node.update:
            self.analyze(node.update)
        # Body loop
        self.analyze(node.body)
        return None

    def analyze_PrintNode(self, node):
        self.analyze(node.value)
        return None

    def analyze_FuncDeclNode(self, node):
        # Daftarkan fungsi ke daftar fungsi global agar bisa dipanggil
        self.functions[node.name] = {
            'params_count': len(node.params)
        }
        
        # Buat scope baru untuk fungsi
        func_scope = {}
        for param in node.params:
            func_scope[param] = {'type': 'ANY', 'is_const': False} # Tipe bebas untuk parameter dinamis
            
        self.scopes.append(func_scope)
        
        # Analisis body fungsi
        self.analyze(node.body)
        
        # Hapus scope fungsi
        self.scopes.pop()
        return None

    def analyze_ReturnNode(self, node):
        if len(self.scopes) <= 1:
            raise SemanticError("Pernyataan 'balekno' (return) kudu ana ing njero fungsi.")
        return self.analyze(node.value)

    def analyze_FuncCallNode(self, node):
        # Cek apakah fungsi telah dideklarasikan
        if node.name not in self.functions:
            raise SemanticError(f"Fungsi '{node.name}' durung dideklarasikake.")
            
        func_info = self.functions[node.name]
        if len(node.args) != func_info['params_count']:
            raise SemanticError(
                f"Fungsi '{node.name}' butuh {func_info['params_count']} argumen, nanging diwenehi {len(node.args)} argumen."
            )
            
        for arg in node.args:
            self.analyze(arg)
            
        return 'ANY'

if __name__ == '__main__':
    # Uji coba analisis semantik
    from lexer import lexer
    from parser_ast import Parser
    
    # 1. Kasus Sukses
    test_ok = """
    wadah a = 10;
    yen (a > 5) {
        a = a + 5;
    }
    """
    
    # 2. Kasus Error: Variabel belum dideklarasikan
    test_err_scope = """
    x = 10; // Error: x durung dideklarasikake nganggo 'wadah'
    """
    
    # 3. Kasus Error: Operasi aritmatika ilegal pada string
    test_err_type = """
    wadah s = "halo";
    wadah hasil = s - 5; // Error: minus ora kena kanggo tipe data STRING
    """

    for name, code in [("OK", test_ok), ("Error Scope", test_err_scope), ("Error Type", test_err_type)]:
        print(f"\n--- Menguji {name} ---")
        tokens, errs = lexer(code)
        if errs:
            print("Lexer error:", errs)
            continue
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            print("Analisis Semantik Sukses (Valid)")
        except Exception as e:
            print("Analisis Semantik Gagal (Ada Error Semantik):", e)
