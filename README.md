# BosoJowo Compiler

📺 **[Tonton Video Presentasi Project BosoJowo Compiler di YouTube](https://youtu.be/nWoHYclq0_s?si=Cd33E2ZDCZyw6a-1)**

Kompilator (Compiler) mini untuk **BosoJowo**, sebuah bahasa pemrograman fiktif/edukasi berbasis bahasa Jawa. Proyek ini akan mengkompilasi kode sumber `.jowo` dan mengubahnya menjadi kode target berupa Python (`.py`) yang kemudian dapat langsung dieksekusi.

## Fitur Utama

Compiler ini melewati 5 tahap utama dari teori kompilasi standar:
1. **Lexical Analysis (Lexer)**: Membaca teks mentah dan mengklasifikasikannya menjadi serangkaian *Token*.
2. **Syntax Analysis (Parser)**: Membangun struktur *Abstract Syntax Tree (AST)* untuk memastikan tata bahasa (sintaks) sudah benar.
3. **Semantic Analysis**: Melakukan pengecekan makna kode, seperti memastikan variabel dideklarasikan sebelum digunakan.
4. **AST Optimization**: (Opsional) Mengoptimalkan AST, misalnya dengan teknik *Constant Folding* pada ekspresi matematika.
5. **Code Generation**: Mengubah AST menjadi kode program Python murni (`.py`).

## Persyaratan
- Python 3.x terinstal di sistem.

---

## Dokumentasi Bahasa

### 📋 Tabel Token
> Dokumentasi lengkap: [`TABEL_TOKEN.md`](TABEL_TOKEN.md)

Berikut ringkasan token yang dikenali oleh lexer BosoJowo:

#### Kata Kunci (Keywords)

| Token     | Kata Kunci BosoJowo | Padanan Umum   | Deskripsi                              |
|-----------|----------------------|----------------|----------------------------------------|
| `VAR`     | `wadah`              | `var` / `let`  | Deklarasi variabel                     |
| `CONST`   | `ginaris`            | `const`        | Deklarasi konstanta                    |
| `IF`      | `yen`                | `if`           | Percabangan kondisional                |
| `ELSE`    | `liyane`             | `else`         | Cabang alternatif                      |
| `WHILE`   | `suwene`             | `while`        | Perulangan berbasis kondisi            |
| `FOR`     | `kanggo`             | `for`          | Perulangan berbasis iterasi            |
| `PRINT`   | `tulis`              | `print`        | Mencetak output ke layar               |
| `FUNC`    | `fungsi`             | `function`     | Deklarasi fungsi                       |
| `RETURN`  | `balekno`            | `return`       | Mengembalikan nilai dari fungsi        |
| `TRUE`    | `bener`              | `true`         | Boolean benar                          |
| `FALSE`   | `salah`              | `false`        | Boolean salah                          |
| `AND`     | `lan`                | `and` / `&&`   | Operator logika DAN                    |
| `OR`      | `utawa`              | `or` / `\|\|`  | Operator logika ATAU                   |
| `NOT`     | `ora`                | `not` / `!`    | Operator logika NEGASI                 |

#### Operator

| Token       | Simbol                         | Deskripsi                |
|-------------|--------------------------------|--------------------------|
| `PLUS`      | `+`                            | Penjumlahan/Konkatenasi  |
| `MINUS`     | `-`                            | Pengurangan/Unary minus  |
| `MULT`      | `*`                            | Perkalian                |
| `DIV`       | `/`                            | Pembagian                |
| `COMPLEX_OP`| `==` `!=` `<` `>` `<=` `>=`   | Perbandingan             |
| `ASSIGN`    | `=`                            | Penugasan                |

#### Delimiter

| Token       | Simbol | Deskripsi                    |
|-------------|--------|------------------------------|
| `LPAREN`    | `(`    | Kurung buka                  |
| `RPAREN`    | `)`    | Kurung tutup                 |
| `LBRACE`    | `{`    | Kurung kurawal buka          |
| `RBRACE`    | `}`    | Kurung kurawal tutup         |
| `DELIMITER` | `;`    | Akhir pernyataan             |
| `DELIMITER` | `,`    | Pemisah argumen              |

#### Literal & Identifier

| Token    | Pola / Contoh          | Deskripsi                |
|----------|------------------------|--------------------------|
| `NUMBER` | `0`, `42`, `100`       | Bilangan bulat           |
| `FLOAT`  | `3.14`, `0.5`          | Bilangan desimal         |
| `STRING` | `"Halo Dunia"`         | String literal           |
| `ID`     | `x`, `angka`, `_temp`  | Nama variabel/fungsi     |

---

### 📖 Grammar Formal (CFG/BNF)
> Dokumentasi lengkap: [`GRAMMAR.md`](GRAMMAR.md)

Berikut ringkasan aturan grammar utama bahasa BosoJowo:

```bnf
program            ::= ( statement )*

statement          ::= var_decl | assignment_or_call | if_statement
                     | while_statement | for_statement | print_statement
                     | func_decl | return_statement | expression ';'

var_decl           ::= ('wadah' | 'ginaris') ID '=' expression ';'

assignment_or_call ::= ID '=' expression ';'
                     | ID '(' args_list ')' ';'

if_statement       ::= 'yen' '(' expression ')' '{' program '}'
                       ( 'liyane' 'yen' '(' expression ')' '{' program '}' )*
                       ( 'liyane' '{' program '}' )?

while_statement    ::= 'suwene' '(' expression ')' '{' program '}'

for_statement      ::= 'kanggo' '(' for_init ';' expression ';' for_update ')' '{' program '}'

print_statement    ::= 'tulis' '(' expression ')' ';'

func_decl          ::= 'fungsi' ID '(' param_list ')' '{' program '}'

return_statement   ::= 'balekno' expression ';'
```

#### Precedence Operator (Rendah → Tinggi)

| Tingkat | Operator                       | Deskripsi              |
|---------|--------------------------------|------------------------|
| 1       | `utawa`                        | Logika OR              |
| 2       | `lan`                          | Logika AND             |
| 3       | `==` `!=` `<` `>` `<=` `>=`   | Perbandingan           |
| 4       | `+` `-`                        | Penjumlahan/Pengurangan|
| 5       | `*` `/`                        | Perkalian/Pembagian    |
| 6       | `ora` (unary), `-` (unary)     | Unary NOT / Negasi     |

---

### 🗂️ Tabel Simbol (Symbol Table)
> Dokumentasi lengkap: [`TABEL_SIMBOL.md`](TABEL_SIMBOL.md)

Tabel Simbol digunakan dalam tahap Analisis Semantik untuk menyimpan dan memvalidasi semua identifier.

#### Struktur Entri Variabel

| Field      | Tipe      | Deskripsi                                              |
|------------|-----------|--------------------------------------------------------|
| `name`     | `string`  | Nama identifier                                        |
| `type`     | `string`  | Tipe data: `NUMBER`, `FLOAT`, `STRING`, `BOOLEAN`, `ANY` |
| `is_const` | `boolean` | `True` jika konstanta (`ginaris`)                      |

#### Struktur Entri Fungsi

| Field          | Tipe      | Deskripsi                     |
|----------------|-----------|-------------------------------|
| `name`         | `string`  | Nama fungsi                   |
| `params_count` | `integer` | Jumlah parameter              |

#### Aturan Validasi Semantik

| No | Aturan                                                    |
|----|-----------------------------------------------------------|
| 1  | Variabel harus dideklarasikan (`wadah`/`ginaris`) sebelum digunakan |
| 2  | Variabel tidak boleh dideklarasikan ulang dalam scope yang sama      |
| 3  | Konstanta (`ginaris`) tidak boleh diubah nilainya                    |
| 4  | Fungsi harus dideklarasikan sebelum dipanggil                        |
| 5  | Jumlah argumen pemanggilan harus sesuai jumlah parameter             |
| 6  | `balekno` (return) hanya boleh digunakan di dalam fungsi             |
| 7  | Operasi `-`, `*`, `/` tidak berlaku untuk tipe `STRING`              |

#### Tipe Data yang Dikenali

| Tipe Data  | Contoh Nilai          | Deskripsi              |
|------------|-----------------------|------------------------|
| `NUMBER`   | `0`, `42`, `100`      | Bilangan bulat         |
| `FLOAT`    | `3.14`, `0.5`         | Bilangan desimal       |
| `STRING`   | `"Halo"`              | Teks/string            |
| `BOOLEAN`  | `bener`, `salah`      | Nilai kebenaran        |
| `ANY`      | *(parameter fungsi)*  | Tipe dinamis           |

---

## Contoh Kode (`sukses.jowo`)

Berikut adalah beberapa sintaks dasar dari BosoJowo:

```text
// 1. Deklarasi Fungsi
fungsi petung_tambah(a, b) {
    balekno a + b;
}

// 2. Deklarasi Variabel
wadah angka = 10;
ginaris wates = 3; // Konstan

// 3. Menulis ke layar (print)
tulis("Angka: " + angka);

// 4. Percabangan
yen (angka > 5) {
    tulis("Lebih dari lima");
} liyane {
    tulis("Kurang dari atau sama dengan lima");
}

// 5. Perulangan
kanggo (wadah i = 0; i < wates; i = i + 1) {
    tulis(i);
}
```

## Cara Menjalankan Compiler

Jalankan file `main.py` melalui *command line / terminal*:

```bash
# Kompilasi file dan simpan hasilnya (menghasilkan file .py)
python main.py sukses.jowo

# Kompilasi file, simpan hasil, dan langsung jalankan programnya
python main.py sukses.jowo -r

# Melihat bantuan / opsi argumen lain
python main.py --help
```

## Struktur Proyek

```
boso_jowo_compiler/
├── main.py            # Entry point compiler
├── lexer.py           # Lexical Analyzer (tokenizer)
├── parser_ast.py      # Syntax Analyzer (parser → AST)
├── ast_nodes.py       # Definisi node AST
├── semantic.py        # Semantic Analyzer & Symbol Table
├── optimizer.py       # AST Optimizer (constant folding)
├── codegen.py         # Code Generator (AST → Python)
├── TABEL_TOKEN.md     # 📋 Dokumentasi Tabel Token
├── GRAMMAR.md         # 📖 Dokumentasi Grammar Formal (CFG/BNF)
├── TABEL_SIMBOL.md    # 🗂️ Dokumentasi Tabel Simbol
├── sukses.jowo        # Contoh kode BosoJowo (sukses)
├── error_syntax.jowo  # Contoh kode error sintaks
├── error_semantik.jowo# Contoh kode error semantik
└── README.md          # Dokumentasi proyek (file ini)
```

## Pengujian Error

Proyek ini juga dilengkapi skenario kegagalan:
- `error_syntax.jowo` - Contoh kode jika melanggar aturan tanda baca/sintaks.
- `error_semantik.jowo` - Contoh kode jika menggunakan variabel yang belum dideklarasikan.
