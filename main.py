import sys
import os
import argparse
import subprocess

from lexer import lexer
from parser_ast import Parser
from semantic import SemanticAnalyzer, SemanticError
from optimizer import ASTOptimizer
from codegen import CodeGenerator

LOGO = """
===============================================
    K O M P I L E R   B O S O J O W O
       (Mini Compiler Bahasa Jawa)
===============================================
"""

def compile_code(source_code, run_after=False, optimize=True):
    # 1. Lexical Analysis
    print("[1/5] Memindai token (Lexer)...")
    tokens, lex_errors = lexer(source_code)
    if lex_errors:
        print("\n[!] KESALAHAN LEKSIKAL DITEMUKAN:")
        for err in lex_errors:
            print(f"  - {err}")
        return None

    # 2. Syntax Analysis (Parsing to AST)
    print("[2/5] Menganalisis sintaks dan membangun AST (Parser)...")
    parser = Parser(tokens)
    try:
        ast = parser.parse()
    except SyntaxError as e:
        print(f"\n[!] KESALAHAN SINTAKS DITEMUKAN:")
        print(f"  - {e}")
        return None

    # 3. Semantic Analysis
    print("[3/5] Menganalisis makna kode (Semantic Analyzer)...")
    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(ast)
    except SemanticError as e:
        print(f"\n[!] KESALAHAN SEMANTIK DITEMUKAN:")
        print(f"  - {e}")
        return None
    except Exception as e:
        print(f"\n[!] KESALAHAN SEMANTIK TIDAK TERDUGA:")
        print(f"  - {e}")
        return None

    # 4. Optimization
    if optimize:
        print("[4/5] Mengoptimalkan pohon AST (Optimizer)...")
        opt = ASTOptimizer()
        ast = opt.optimize(ast)
    else:
        print("[4/5] Melewati fase optimasi (--no-opt)...")

    # 5. Code Generation
    print("[5/5] Membangkitkan kode target Python (Code Generator)...")
    codegen = CodeGenerator()
    try:
        python_code = codegen.generate(ast)
    except Exception as e:
        print(f"\n[!] GAGAL MEMBANGKITKAN KODE:")
        print(f"  - {e}")
        return None

    print("\n[+] Kompilasi Berhasil Sempurna!")
    return python_code

def main():
    print(LOGO)
    
    parser = argparse.ArgumentParser(description="Compiler BosoJowo - Kompilasikan kode .jowo kamu menjadi Python.")
    parser.add_argument("input_file", help="Path ke file sumber BosoJowo (.jowo)")
    parser.add_argument("-o", "--output", help="Path file output (.py). Default: nama_file_sumber.py")
    parser.add_argument("-r", "--run", action="store_true", help="Jalankan program Python langsung setelah kompilasi sukses")
    parser.add_argument("--no-opt", action="store_true", help="Jangan lakukan optimasi AST (lewati Constant Folding)")
    
    # Jika tidak ada argumen, tampilkan bantuan
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"[!] Error: File '{args.input_file}' tidak ditemukan.")
        sys.exit(1)
        
    # Tentukan file output default jika tidak diberikan
    output_file = args.output
    if not output_file:
        base_name, _ = os.path.splitext(args.input_file)
        output_file = base_name + ".py"
        
    print(f"[*] Membaca file: {args.input_file}...")
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"[!] Gagal membaca file: {e}")
        sys.exit(1)
        
    # Jalankan proses kompilasi
    python_code = compile_code(source_code, run_after=args.run, optimize=not args.no_opt)
    
    if python_code is None:
        print("\n[!] Kompilasi gagal. Silakan perbaiki kesalahan di atas.")
        sys.exit(1)
        
    # Tulis hasil ke file output
    print(f"[*] Menulis kode hasil kompilasi ke: {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_code)
    except Exception as e:
        print(f"[!] Gagal menulis file output: {e}")
        sys.exit(1)
        
    # Jalankan program jika diminta
    if args.run:
        print(f"\n[*] MENJALANKAN PROGRAM ({output_file}):")
        print("-----------------------------------------------")
        try:
            # Jika dibekukan dengan PyInstaller, gunakan perintah 'python' dari PATH sistem
            if getattr(sys, 'frozen', False):
                python_executable = 'python'
            else:
                python_executable = sys.executable
            subprocess.run([python_executable, output_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n[!] Terjadi kesalahan saat menjalankan program: {e}")
        except Exception as e:
            print(f"\n[!] Gagal menjalankan program: {e}")
        print("-----------------------------------------------")

if __name__ == '__main__':
    main()
