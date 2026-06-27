# BosoJowo Compiler

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

## Pengujian Error

Proyek ini juga dilengkapi skenario kegagalan:
- `error_syntax.jowo` - Contoh kode jika melanggar aturan tanda baca/sintaks.
- `error_semantik.jowo` - Contoh kode jika menggunakan variabel yang belum dideklarasikan.
