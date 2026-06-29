# Grammar Formal (CFG/BNF) — Bahasa BosoJowo

Dokumen ini mendefinisikan aturan tata bahasa (*grammar*) formal bahasa BosoJowo menggunakan notasi **Context-Free Grammar (CFG)** dalam format BNF (*Backus-Naur Form*).

Grammar ini menjadi dasar bagi **Parser** untuk membangun *Abstract Syntax Tree (AST)*.

---

## Notasi yang Digunakan

| Simbol        | Arti                                           |
|---------------|-------------------------------------------------|
| `::=`         | Didefinisikan sebagai                           |
| `\|`          | Atau (pilihan alternatif)                       |
| `( ... )*`    | Nol atau lebih pengulangan                      |
| `( ... )?`    | Opsional (nol atau satu kali)                   |
| `( ... )+`    | Satu atau lebih pengulangan                     |
| `HURUF_BESAR` | Terminal (token dari lexer)                     |
| `huruf_kecil` | Non-terminal (aturan grammar)                   |
| `'teks'`      | Literal terminal                                |

---

## 1. Struktur Program

```bnf
program ::= ( statement )*
```

Program terdiri dari nol atau lebih pernyataan (*statement*).

---

## 2. Pernyataan (Statement)

```bnf
statement ::= var_decl
            | assignment_or_call
            | if_statement
            | while_statement
            | for_statement
            | print_statement
            | func_decl
            | return_statement
            | expression ';'
```

---

## 3. Deklarasi Variabel

```bnf
var_decl ::= 'wadah' ID '=' expression ';'
           | 'ginaris' ID '=' expression ';'
```

**Contoh:**
```
wadah angka = 10;
ginaris PI = 3.14;
```

---

## 4. Penugasan & Pemanggilan Fungsi

```bnf
assignment_or_call ::= ID '=' expression ';'
                     | ID '(' args_list ')' ';'
```

**Contoh:**
```
x = x + 1;
tambah(a, b);
```

---

## 5. Percabangan (If-Else)

```bnf
if_statement ::= 'yen' '(' expression ')' '{' program '}'
                 ( 'liyane' 'yen' '(' expression ')' '{' program '}' )*
                 ( 'liyane' '{' program '}' )?
```

**Contoh:**
```
yen (x > 10) {
    tulis("Gedhe");
} liyane yen (x > 5) {
    tulis("Sedeng");
} liyane {
    tulis("Cilik");
}
```

---

## 6. Perulangan While

```bnf
while_statement ::= 'suwene' '(' expression ')' '{' program '}'
```

**Contoh:**
```
suwene (x < 10) {
    x = x + 1;
}
```

---

## 7. Perulangan For

```bnf
for_statement ::= 'kanggo' '(' for_init ';' expression ';' for_update ')' '{' program '}'

for_init ::= 'wadah' ID '=' expression
           | ID '=' expression

for_update ::= ID '=' expression
```

**Contoh:**
```
kanggo (wadah i = 0; i < 10; i = i + 1) {
    tulis(i);
}
```

---

## 8. Cetak (Print)

```bnf
print_statement ::= 'tulis' '(' expression ')' ';'
```

**Contoh:**
```
tulis("Halo Dunia!");
tulis(angka + 5);
```

---

## 9. Deklarasi Fungsi

```bnf
func_decl ::= 'fungsi' ID '(' param_list ')' '{' program '}'

param_list ::= ( ID ( ',' ID )* )?
```

**Contoh:**
```
fungsi tambah(a, b) {
    balekno a + b;
}
```

---

## 10. Pernyataan Return

```bnf
return_statement ::= 'balekno' expression ';'
```

**Contoh:**
```
balekno hasil * 2;
```

---

## 11. Ekspresi (Expression) — Urutan Precedence

Ekspresi didefinisikan secara bertingkat sesuai urutan prioritas operator (*operator precedence*), dari yang **terendah** ke **tertinggi**:

```bnf
expression     ::= logical_or

logical_or     ::= logical_and ( 'utawa' logical_and )*

logical_and    ::= equality ( 'lan' equality )*

equality       ::= additive ( COMPLEX_OP additive )*

additive       ::= multiplicative ( ( '+' | '-' ) multiplicative )*

multiplicative ::= factor ( ( '*' | '/' ) factor )*

factor         ::= '(' expression ')'
                 | 'ora' factor
                 | '-' factor
                 | NUMBER
                 | FLOAT
                 | STRING
                 | 'bener'
                 | 'salah'
                 | ID '(' args_list ')'
                 | ID

args_list      ::= ( expression ( ',' expression )* )?
```

### Tabel Precedence Operator (Rendah → Tinggi)

| Tingkat | Operator                         | Asosiasi  | Deskripsi              |
|---------|----------------------------------|-----------|------------------------|
| 1       | `utawa`                          | Kiri      | Logika OR              |
| 2       | `lan`                            | Kiri      | Logika AND             |
| 3       | `==` `!=` `<` `>` `<=` `>=`     | Kiri      | Perbandingan           |
| 4       | `+` `-`                          | Kiri      | Penjumlahan/Pengurangan|
| 5       | `*` `/`                          | Kiri      | Perkalian/Pembagian    |
| 6       | `ora` (unary), `-` (unary)       | Kanan     | Unary NOT / Negasi     |

---

## 12. Token Terminal

Berikut token-token terminal yang digunakan dalam grammar di atas:

```bnf
ID         ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER     ::= [0-9]+
FLOAT      ::= [0-9]+ '.' [0-9]+
STRING     ::= '"' ( karakter_escape | karakter_biasa )* '"'
COMPLEX_OP ::= '==' | '!=' | '<=' | '>=' | '<' | '>'
```

---

## 13. Ringkasan Derivasi (Parse Tree)

Berikut contoh derivasi untuk kode:
```
wadah x = 5 + 3;
```

```
program
 └── statement
      └── var_decl
           ├── 'wadah'
           ├── ID('x')
           ├── '='
           ├── expression
           │    └── additive
           │         ├── factor → NUMBER(5)
           │         ├── '+'
           │         └── factor → NUMBER(3)
           └── ';'
```

---

## 14. Diagram Railroad (Visualisasi Grammar)

### Statement

```
statement ──┬── var_decl ──────────────────┬──►
            ├── assignment_or_call ────────┤
            ├── if_statement ──────────────┤
            ├── while_statement ───────────┤
            ├── for_statement ─────────────┤
            ├── print_statement ───────────┤
            ├── func_decl ────────────────┤
            └── return_statement ──────────┘
```

### Expression Precedence

```
expression ──► logical_or
                 │
                 ▼
              logical_and ──('utawa')──► logical_and
                 │
                 ▼
              equality ──('lan')──► equality
                 │
                 ▼
              additive ──(COMPLEX_OP)──► additive
                 │
                 ▼
              multiplicative ──('+'/'-')──► multiplicative
                 │
                 ▼
              factor ──('*'/'/')──► factor
```
