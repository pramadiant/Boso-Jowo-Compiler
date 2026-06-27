from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, IfNode, ElifNode, WhileNode,
    ForNode, PrintNode, FuncDeclNode, ReturnNode, FuncCallNode,
    BinOpNode, UnaryOpNode, LiteralNode, VarNode
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def peek_token(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token[0] == token_type:
            self.pos += 1
            return token
        else:
            token_info = f"'{token[1]}' ({token[0]})" if token else "EOF"
            line = token[2] if token else "pungkasan"
            col = token[3] if token else "pungkasan"
            raise SyntaxError(
                f"Kekurangan token '{token_type}' ing baris {line}, kolom {col}. Entuk: {token_info}"
            )

    def parse(self):
        """Memulai proses parsing program"""
        node = self.program()
        curr = self.current_token()
        if curr and curr[0] != 'EOF':
            raise SyntaxError(
                f"Token tidak terduga '{curr[1]}' ({curr[0]}) ing baris {curr[2]}, kolom {curr[3]} setelah program utama selesai."
            )
        return node

    def program(self):
        """program : (statement)*"""
        statements = []
        while self.current_token() and self.current_token()[0] not in ('EOF', 'RBRACE'):
            # Abaikan delimiter kosong (titik koma berlebih)
            if self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ';':
                self.eat('DELIMITER')
                continue
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    def statement(self):
        """
        statement : var_decl
                  | assignment_or_call_statement
                  | if_statement
                  | while_statement
                  | for_statement
                  | print_statement
                  | func_decl
                  | return_statement
        """
        token = self.current_token()
        if not token:
            return None

        if token[0] in ('VAR', 'CONST'):
            return self.var_decl()
        elif token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'WHILE':
            return self.while_statement()
        elif token[0] == 'FOR':
            return self.for_statement()
        elif token[0] == 'PRINT':
            return self.print_statement()
        elif token[0] == 'FUNC':
            return self.func_decl()
        elif token[0] == 'RETURN':
            return self.return_statement()
        elif token[0] == 'ID':
            # Bisa berupa assignment (x = ...) atau function call (tambah(x, y);)
            return self.assignment_or_call_statement()
        else:
            # Mengizinkan ekspresi bebas sebagai statement jika diikuti titik koma (;)
            expr = self.logical_or()
            self.eat('DELIMITER')
            return expr

    def var_decl(self):
        """var_decl : (VAR | CONST) ID ASSIGN logical_or DELIMITER"""
        is_const = False
        if self.current_token()[0] == 'CONST':
            self.eat('CONST')
            is_const = True
        else:
            self.eat('VAR')
            
        id_token = self.eat('ID')
        self.eat('ASSIGN')
        expr = self.logical_or()
        self.eat('DELIMITER')
        return VarDeclNode(id_token[1], expr, is_const=is_const)

    def assignment_or_call_statement(self):
        """assignment_or_call_statement : ID ASSIGN logical_or DELIMITER
                                        | ID LPAREN args_list RPAREN DELIMITER"""
        id_token = self.eat('ID')
        curr = self.current_token()
        
        if curr and curr[0] == 'ASSIGN':
            self.eat('ASSIGN')
            expr = self.logical_or()
            self.eat('DELIMITER')
            return AssignNode(id_token[1], expr)
        elif curr and curr[0] == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.current_token() and self.current_token()[0] != 'RPAREN':
                args.append(self.logical_or())
                while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
                    self.eat('DELIMITER')
                    args.append(self.logical_or())
            self.eat('RPAREN')
            self.eat('DELIMITER')
            return FuncCallNode(id_token[1], args)
        else:
            raise SyntaxError(
                f"Kudu berupa penugasan (=) utawa celukan fungsi () ing baris {id_token[2]}, kolom {id_token[3]}"
            )

    def if_statement(self):
        """
        if_statement : IF LPAREN logical_or RPAREN LBRACE program RBRACE
                       ( ELIF LPAREN logical_or RPAREN LBRACE program RBRACE )*
                       ( ELSE LBRACE program RBRACE )?
        """
        self.eat('IF')
        self.eat('LPAREN')
        cond = self.logical_or()
        self.eat('RPAREN')
        self.eat('LBRACE')
        then_branch = self.program()
        self.eat('RBRACE')

        elif_branches = []
        while self.current_token() and self.current_token()[0] == 'ELSE':
            # Cek apakah setelah ELSE ada IF (liyane yen)
            next_token = self.peek_token()
            if next_token and next_token[0] == 'IF':
                self.eat('ELSE')
                self.eat('IF')
                self.eat('LPAREN')
                elif_cond = self.logical_or()
                self.eat('RPAREN')
                self.eat('LBRACE')
                elif_body = self.program()
                self.eat('RBRACE')
                elif_branches.append(ElifNode(elif_cond, elif_body))
            else:
                break

        else_branch = None
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            else_branch = self.program()
            self.eat('RBRACE')

        return IfNode(cond, then_branch, elif_branches, else_branch)

    def while_statement(self):
        """while_statement : WHILE LPAREN logical_or RPAREN LBRACE program RBRACE"""
        self.eat('WHILE')
        self.eat('LPAREN')
        cond = self.logical_or()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = self.program()
        self.eat('RBRACE')
        return WhileNode(cond, body)

    def for_statement(self):
        """for_statement : FOR LPAREN statement DELIMITER logical_or DELIMITER statement RPAREN LBRACE program RBRACE"""
        # Catatan: statement di dalam for_stmt tidak menggunakan delimiter akhir ; karena delimiter dibaca manual
        self.eat('FOR')
        self.eat('LPAREN')
        
        # Inisialisasi: wadah i = 0 atau i = 0
        init = None
        if self.current_token() and self.current_token()[0] == 'VAR':
            self.eat('VAR')
            id_token = self.eat('ID')
            self.eat('ASSIGN')
            expr = self.logical_or()
            init = VarDeclNode(id_token[1], expr)
        elif self.current_token() and self.current_token()[0] == 'ID':
            id_token = self.eat('ID')
            self.eat('ASSIGN')
            expr = self.logical_or()
            init = AssignNode(id_token[1], expr)
        self.eat('DELIMITER') # Semicolon setelah init
        
        # Kondisi: i < 10
        cond = self.logical_or()
        self.eat('DELIMITER') # Semicolon setelah kondisi
        
        # Update: i = i + 1
        update = None
        if self.current_token() and self.current_token()[0] == 'ID':
            id_token = self.eat('ID')
            self.eat('ASSIGN')
            expr = self.logical_or()
            update = AssignNode(id_token[1], expr)
            
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = self.program()
        self.eat('RBRACE')
        
        return ForNode(init, cond, update, body)

    def print_statement(self):
        """print_statement : PRINT LPAREN logical_or RPAREN DELIMITER"""
        self.eat('PRINT')
        self.eat('LPAREN')
        expr = self.logical_or()
        self.eat('RPAREN')
        self.eat('DELIMITER')
        return PrintNode(expr)

    def func_decl(self):
        """func_decl : FUNC ID LPAREN (ID (COMMA ID)*)? RPAREN LBRACE program RBRACE"""
        self.eat('FUNC')
        id_token = self.eat('ID')
        self.eat('LPAREN')
        params = []
        if self.current_token() and self.current_token()[0] == 'ID':
            params.append(self.eat('ID')[1])
            while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
                self.eat('DELIMITER')
                params.append(self.eat('ID')[1])
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = self.program()
        self.eat('RBRACE')
        return FuncDeclNode(id_token[1], params, body)

    def return_statement(self):
        """return_statement : RETURN logical_or DELIMITER"""
        self.eat('RETURN')
        expr = self.logical_or()
        self.eat('DELIMITER')
        return ReturnNode(expr)

    # --- EKSPRESI (PRECEDENCE) ---

    def logical_or(self):
        """logical_or : logical_and (OR logical_and)*"""
        node = self.logical_and()
        while self.current_token() and self.current_token()[0] == 'OR':
            op = self.eat('OR')[1]
            right = self.logical_and()
            node = BinOpNode(node, op, right)
        return node

    def logical_and(self):
        """logical_and : equality (AND equality)*"""
        node = self.equality()
        while self.current_token() and self.current_token()[0] == 'AND':
            op = self.eat('AND')[1]
            right = self.equality()
            node = BinOpNode(node, op, right)
        return node

    def equality(self):
        """equality : expr (COMPLEX_OP expr)*"""
        node = self.expr()
        while self.current_token() and self.current_token()[0] == 'COMPLEX_OP':
            op = self.eat('COMPLEX_OP')[1]
            right = self.expr()
            node = BinOpNode(node, op, right)
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            op = self.eat(self.current_token()[0])[1]
            right = self.term()
            node = BinOpNode(node, op, right)
        return node

    def term(self):
        """term : factor ((MULT | DIV) factor)*"""
        node = self.factor()
        while self.current_token() and self.current_token()[0] in ('MULT', 'DIV'):
            op = self.eat(self.current_token()[0])[1]
            right = self.factor()
            node = BinOpNode(node, op, right)
        return node

    def factor(self):
        """
        factor : LPAREN logical_or RPAREN
               | NOT factor
               | MINUS factor
               | Literal (NUMBER, FLOAT, STRING, TRUE, FALSE)
               | ID LPAREN args_list RPAREN (Function Call)
               | ID (Variable Access)
        """
        token = self.current_token()
        if not token:
            raise SyntaxError("Kekurangan token ing pungkasan program")

        if token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.logical_or()
            self.eat('RPAREN')
            return node
        
        elif token[0] == 'NOT':
            op = self.eat('NOT')[1]
            expr = self.factor()
            return UnaryOpNode(op, expr)
            
        elif token[0] == 'MINUS':
            op = self.eat('MINUS')[1]
            expr = self.factor()
            return UnaryOpNode(op, expr)

        elif token[0] in ('NUMBER', 'FLOAT', 'STRING', 'TRUE', 'FALSE'):
            lit_token = self.eat(token[0])
            val = lit_token[1]
            
            # Konversi nilai literal ke tipe data Python yang sesuai
            if lit_token[0] == 'NUMBER':
                val = int(val)
            elif lit_token[0] == 'FLOAT':
                val = float(val)
            elif lit_token[0] == 'TRUE':
                val = True
            elif lit_token[0] == 'FALSE':
                val = False
                
            return LiteralNode(val, lit_token[0])

        elif token[0] == 'ID':
            id_token = self.eat('ID')
            # Cek apakah ini pemanggilan fungsi (Function Call) dalam ekspresi
            if self.current_token() and self.current_token()[0] == 'LPAREN':
                self.eat('LPAREN')
                args = []
                if self.current_token() and self.current_token()[0] != 'RPAREN':
                    args.append(self.logical_or())
                    while self.current_token() and self.current_token()[0] == 'DELIMITER' and self.current_token()[1] == ',':
                        self.eat('DELIMITER')
                        args.append(self.logical_or())
                self.eat('RPAREN')
                return FuncCallNode(id_token[1], args)
            else:
                return VarNode(id_token[1])

        else:
            raise SyntaxError(
                f"Sintaks ora valid: token '{token[1]}' ({token[0]}) ing baris {token[2]}, kolom {token[3]}"
            )

if __name__ == '__main__':
    from lexer import lexer
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
    """
    tokens, errs = lexer(test_code)
    if errs:
        print("Lexer errors:", errs)
    else:
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            print("AST Berhasil dibuat:")
            print(ast)
        except Exception as e:
            print("Parser error:", e)
