# Tabel Token — Bahasa BosoJowo

Dokumen ini mendefinisikan seluruh token yang dikenali oleh **Lexer** bahasa BosoJowo.  
Token adalah unit terkecil yang bermakna dalam kode sumber, hasil dari proses *Lexical Analysis*.

Format token yang dihasilkan lexer: `(JENIS_TOKEN, NILAI, BARIS, KOLOM)`

---

## 1. Kata Kunci (Keywords)

Kata kunci adalah kata-kata yang telah dipesan (*reserved words*) oleh bahasa dan tidak boleh digunakan sebagai nama variabel/fungsi.

| No | Token     | Kata Kunci BosoJowo | Padanan Umum (ID/EN) | Deskripsi                              |
|----|-----------|----------------------|----------------------|----------------------------------------|
| 1  | `VAR`     | `wadah`              | `var` / `let`        | Deklarasi variabel                     |
| 2  | `CONST`   | `ginaris`            | `const`              | Deklarasi konstanta (tidak bisa diubah)|
| 3  | `IF`      | `yen`                | `if`                 | Percabangan kondisional                |
| 4  | `ELSE`    | `liyane`             | `else`               | Cabang alternatif                      |
| 5  | `WHILE`   | `suwene`             | `while`              | Perulangan berbasis kondisi            |
| 6  | `FOR`     | `kanggo`             | `for`                | Perulangan berbasis iterasi            |
| 7  | `PRINT`   | `tulis`              | `print`              | Mencetak output ke layar               |
| 8  | `FUNC`    | `fungsi`             | `function`           | Deklarasi fungsi                       |
| 9  | `RETURN`  | `balekno`            | `return`             | Mengembalikan nilai dari fungsi        |
| 10 | `TRUE`    | `bener`              | `true`               | Literal boolean bernilai benar         |
| 11 | `FALSE`   | `salah`              | `false`              | Literal boolean bernilai salah         |
| 12 | `AND`     | `lan`                | `and` / `&&`         | Operator logika DAN                    |
| 13 | `OR`      | `utawa`              | `or` / `\|\|`        | Operator logika ATAU                   |
| 14 | `NOT`     | `ora`                | `not` / `!`          | Operator logika NEGASI                 |

---

## 2. Literal

Literal adalah nilai tetap yang ditulis langsung dalam kode sumber.

| No | Token    | Pola Regex                  | Contoh          | Deskripsi                          |
|----|----------|-----------------------------|-----------------|------------------------------------|
| 1  | `NUMBER` | `\d+`                       | `0`, `42`, `100`| Bilangan bulat (integer)           |
| 2  | `FLOAT`  | `\d+\.\d+`                  | `3.14`, `0.5`   | Bilangan desimal (float)           |
| 3  | `STRING` | `"(?:\\\\.\|[^"\\\\])*"`    | `"Halo Dunia"`  | String literal (dengan escape)     |
| 4  | `TRUE`   | `\bbener\b`                 | `bener`         | Boolean benar                      |
| 5  | `FALSE`  | `\bsalah\b`                 | `salah`         | Boolean salah                      |

---

## 3. Operator

### 3.1 Operator Aritmatika

| No | Token   | Simbol | Deskripsi                |
|----|---------|--------|--------------------------|
| 1  | `PLUS`  | `+`    | Penjumlahan / Konkatenasi|
| 2  | `MINUS` | `-`    | Pengurangan / Unary minus|
| 3  | `MULT`  | `*`    | Perkalian                |
| 4  | `DIV`   | `/`    | Pembagian                |

### 3.2 Operator Perbandingan (COMPLEX_OP)

| No | Simbol | Deskripsi                    |
|----|--------|------------------------------|
| 1  | `==`   | Sama dengan                  |
| 2  | `!=`   | Tidak sama dengan            |
| 3  | `<`    | Kurang dari                  |
| 4  | `>`    | Lebih dari                   |
| 5  | `<=`   | Kurang dari atau sama dengan |
| 6  | `>=`   | Lebih dari atau sama dengan  |

### 3.3 Operator Penugasan

| No | Token    | Simbol | Deskripsi                  |
|----|----------|--------|----------------------------|
| 1  | `ASSIGN` | `=`    | Menetapkan nilai ke variabel|

### 3.4 Operator Logika

| No | Token | Kata Kunci | Deskripsi     |
|----|-------|------------|---------------|
| 1  | `AND` | `lan`      | Logika DAN    |
| 2  | `OR`  | `utawa`    | Logika ATAU   |
| 3  | `NOT` | `ora`      | Logika NEGASI |

---

## 4. Delimiter & Tanda Baca

| No | Token       | Simbol | Deskripsi                           |
|----|-------------|--------|-------------------------------------|
| 1  | `LPAREN`    | `(`    | Kurung buka                         |
| 2  | `RPAREN`    | `)`    | Kurung tutup                        |
| 3  | `LBRACE`    | `{`    | Kurung kurawal buka (awal blok)     |
| 4  | `RBRACE`    | `}`    | Kurung kurawal tutup (akhir blok)   |
| 5  | `DELIMITER` | `;`    | Pemisah/akhir pernyataan (semicolon)|
| 6  | `DELIMITER` | `,`    | Pemisah argumen/parameter (koma)    |

---

## 5. Identifier

| No | Token | Pola Regex          | Contoh                  | Deskripsi                                |
|----|-------|---------------------|-------------------------|------------------------------------------|
| 1  | `ID`  | `[a-zA-Z_]\w*`      | `x`, `angka`, `_temp`   | Nama variabel, fungsi, atau parameter    |

> **Catatan:** Identifier tidak boleh sama dengan kata kunci yang telah dipesan.

---

## 6. Komentar (Diabaikan oleh Lexer)

| No | Jenis           | Pola                  | Contoh                     |
|----|-----------------|-----------------------|----------------------------|
| 1  | Baris tunggal   | `//...`               | `// Iki komentar`          |
| 2  | Multi-baris     | `/* ... */`            | `/* Komentar panjang */`   |

---

## 7. Token Khusus

| No | Token       | Deskripsi                                               |
|----|-------------|---------------------------------------------------------|
| 1  | `EOF`       | Penanda akhir file, ditambahkan otomatis oleh lexer     |
| 2  | `MISMATCH`  | Karakter ilegal yang tidak cocok dengan pola manapun    |
| 3  | `WHITESPACE`| Spasi, tab, newline — diabaikan oleh lexer              |

---

## 8. Urutan Prioritas Pencocokan Token

Urutan pencocokan pada lexer sangat penting untuk menghindari ambiguitas:

```
1. Komentar multi-line   →  /* ... */
2. Komentar baris        →  // ...
3. String literal        →  "..."
4. Float                 →  123.45  (sebelum NUMBER agar tidak terpecah)
5. Number                →  123
6. Kata Kunci            →  wadah, ginaris, yen, dll. (sebelum ID)
7. Operator Perbandingan →  ==, !=, <=, >= (sebelum ASSIGN =)
8. Operator Penugasan    →  =
9. Identifier            →  nama_variabel
10. Operator Aritmatika  →  +, -, *, /
11. Delimiter            →  (, ), {, }, ;, ,
12. Whitespace           →  (diabaikan)
13. Mismatch             →  karakter ilegal (error)
```

---

## Contoh Tokenisasi

**Kode Sumber:**
```
wadah angka = 10;
```

**Hasil Tokenisasi:**
| No | Token   | Nilai   | Baris | Kolom |
|----|---------|---------|-------|-------|
| 1  | `VAR`   | `wadah` | 1     | 1     |
| 2  | `ID`    | `angka` | 1     | 7     |
| 3  | `ASSIGN`| `=`     | 1     | 13    |
| 4  | `NUMBER`| `10`    | 1     | 15    |
| 5  | `DELIMITER`| `;`  | 1     | 17    |
| 6  | `EOF`   | ``      | 1     | 18    |
