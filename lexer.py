import re

# Definisikan spesifikasi token untuk bahasa BosoJowo
# Urutan sangat krusial: operator kompleks sebelum operator sederhana, float sebelum number, keyword sebelum ID.
token_spec = [
    ('MULTI_COMMENT',  r'/\*[\s\S]*?\*/'),   # Komentar multi-line (/* ... */)
    ('SINGLE_COMMENT', r'//.*'),             # Komentar satu baris (// ...)
    ('STRING',         r'"(?:\\.|[^"\\])*"'),# String literal dengan escape character
    ('FLOAT',          r'\d+\.\d+'),         # Bilangan desimal
    ('NUMBER',         r'\d+'),              # Bilangan bulat
    
    # Kata Kunci BosoJowo (menggunakan \b agar tidak mencocokkan bagian dari kata/identifier lain)
    ('VAR',            r'\bwadah\b'),
    ('CONST',          r'\bginaris\b'),
    ('IF',             r'\byen\b'),
    ('ELSE',           r'\bliyane\b'),
    ('WHILE',          r'\bsuwene\b'),
    ('FOR',            r'\bkanggo\b'),
    ('PRINT',          r'\btulis\b'),
    ('TRUE',           r'\bbener\b'),
    ('FALSE',          r'\bsalah\b'),
    ('FUNC',           r'\bfungsi\b'),
    ('RETURN',         r'\bbalekno\b'),
    ('AND',            r'\blan\b'),
    ('OR',             r'\butawa\b'),
    ('NOT',            r'\bora\b'),
    
    # Operator
    ('COMPLEX_OP',     r'==|!=|<=|>=|<|>'),
    ('ASSIGN',         r'='),
    ('ID',             r'[a-zA-Z_]\w*'),
    ('PLUS',           r'\+'),
    ('MINUS',          r'-'),
    ('MULT',           r'\*'),
    ('DIV',            r'/'),
    
    # Delimiter
    ('LPAREN',         r'\('),
    ('RPAREN',         r'\)'),
    ('LBRACE',         r'\{'),
    ('RBRACE',         r'\}'),
    ('DELIMITER',      r'[;,]'),
    
    # Whitespace
    ('WHITESPACE',     r'\s+'),
    ('MISMATCH',       r'.'),                # Karakter ilegal
]

# Gabungkan pola-pola regex
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)

def get_line_col(code, index):
    """Fungsi pembantu untuk mendapatkan nomor baris dan kolom berdasarkan indeks karakter"""
    line = code.count('\n', 0, index) + 1
    last_newline = code.rfind('\n', 0, index)
    if last_newline == -1:
        col = index + 1
    else:
        col = index - last_newline
    return line, col

def lexer(code):
    """
    Memecah string kode BosoJowo menjadi daftar token.
    Mengembalikan: (list_of_tokens, list_of_errors)
    Format token: (KIND, VALUE, LINE, COL)
    """
    result = []
    errors = []
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        start_pos = mo.start()
        
        line, col = get_line_col(code, start_pos)
        
        # Lewati komentar dan whitespace
        if kind in ['WHITESPACE', 'SINGLE_COMMENT', 'MULTI_COMMENT']:
            continue
        elif kind == 'MISMATCH':
            errors.append(f"Karakter ilegal '{value}' ing baris {line}, kolom {col}")
        else:
            # Jika token STRING, hapus tanda kutipnya untuk nilai internal
            if kind == 'STRING':
                # Hilangkan tanda kutip terluar
                value = value[1:-1].encode().decode('unicode_escape')
            result.append((kind, value, line, col))
            
    # Tambahkan EOF token di akhir
    line_eof, col_eof = get_line_col(code, len(code))
    result.append(('EOF', '', line_eof, col_eof))
    
    return result, errors

if __name__ == '__main__':
    # Uji coba lexer sederhana
    test_code = """
    wadah x = 10; // Iki variabel
    yen (x == 10 lan bener) {
        tulis("Nilaine x iku: " + x);
    }
    """
    tokens, errs = lexer(test_code)
    print("Tokens:")
    for t in tokens:
        print(t)
    if errs:
        print("Errors:")
        for e in errs:
            print(e)
