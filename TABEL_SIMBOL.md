# Tabel Simbol (Symbol Table) — Bahasa BosoJowo

Dokumen ini mendefinisikan struktur dan mekanisme **Tabel Simbol** (*Symbol Table*) yang digunakan dalam tahap **Analisis Semantik** compiler BosoJowo.

Tabel Simbol menyimpan informasi tentang semua *identifier* (variabel, konstanta, fungsi, parameter) yang dideklarasikan dalam program.

---

## 1. Apa itu Tabel Simbol?

Tabel Simbol adalah struktur data yang digunakan compiler untuk:
- **Menyimpan** informasi setiap identifier yang dideklarasikan
- **Mencari** (*lookup*) apakah identifier sudah terdefinisi
- **Memvalidasi** penggunaan identifier (tipe, scope, mutabilitas)
- **Mendeteksi kesalahan** semantik seperti variabel belum dideklarasikan atau konstanta diubah nilainya

---

## 2. Struktur Data Tabel Simbol

### 2.1 Entri Variabel

Setiap variabel/konstanta yang dideklarasikan disimpan dengan struktur berikut:

| Field      | Tipe Data | Deskripsi                                              |
|------------|-----------|--------------------------------------------------------|
| `name`     | `string`  | Nama identifier (nama variabel)                        |
| `type`     | `string`  | Tipe data: `NUMBER`, `FLOAT`, `STRING`, `BOOLEAN`, `ANY` |
| `is_const` | `boolean` | `True` jika dideklarasikan dengan `ginaris` (konstanta)|

**Format Internal (Python dict):**
```python
{
    'nama_variabel': {
        'type': 'NUMBER',      # Tipe data
        'is_const': False       # Apakah konstanta
    }
}
```

### 2.2 Entri Fungsi

Setiap fungsi yang dideklarasikan disimpan secara terpisah:

| Field          | Tipe Data | Deskripsi                                |
|----------------|-----------|------------------------------------------|
| `name`         | `string`  | Nama fungsi                              |
| `params_count` | `integer` | Jumlah parameter yang diterima           |

**Format Internal (Python dict):**
```python
{
    'nama_fungsi': {
        'params_count': 2       # Jumlah parameter
    }
}
```

---

## 3. Mekanisme Scope (Lingkup)

Tabel Simbol menggunakan sistem **scope bertingkat** (*nested scopes*) yang diimplementasikan sebagai **stack (tumpukan) dari dictionary**.

### 3.1 Jenis Scope

| No | Jenis Scope     | Kapan Dibuat                         | Contoh                          |
|----|-----------------|--------------------------------------|---------------------------------|
| 1  | **Global Scope**| Saat program dimulai (selalu ada)    | Variabel di level atas program  |
| 2  | **Function Scope** | Saat memasuki deklarasi fungsi    | Parameter & variabel lokal fungsi|

### 3.2 Ilustrasi Stack Scope

```
Program:
    wadah x = 10;                    ← Scope Global
    fungsi tambah(a, b) {            ← Scope Fungsi (ditambahkan ke stack)
        wadah hasil = a + b;
        balekno hasil;
    }                                ← Scope Fungsi (dihapus dari stack)
    tulis(x);                        ← Kembali ke Scope Global
```

**Visualisasi Stack:**

```
Saat di dalam fungsi:            Saat kembali ke global:
┌──────────────────────┐         ┌──────────────────────┐
│ Scope Fungsi         │         │                      │
│   a    → {NUMBER}    │         │                      │
│   b    → {NUMBER}    │         └──────────────────────┘
│   hasil→ {NUMBER}    │         ┌──────────────────────┐
├──────────────────────┤         │ Scope Global          │
│ Scope Global         │         │   x → {NUMBER}        │
│   x   → {NUMBER}     │         │   tambah → func(2)    │
└──────────────────────┘         └──────────────────────┘
```

### 3.3 Aturan Pencarian (Lookup)

Pencarian variabel dilakukan dari **scope terdalam ke terluar**:

```
lookup("x"):
  1. Cari di Scope Fungsi    → tidak ditemukan
  2. Cari di Scope Global    → ditemukan ✓
```

---

## 4. Tipe Data yang Dikenali

| No | Tipe Data  | Token Sumber        | Contoh Nilai       | Deskripsi                     |
|----|------------|---------------------|---------------------|-------------------------------|
| 1  | `NUMBER`   | `NUMBER`            | `0`, `42`, `100`    | Bilangan bulat                |
| 2  | `FLOAT`    | `FLOAT`             | `3.14`, `0.5`       | Bilangan desimal              |
| 3  | `STRING`   | `STRING`            | `"Halo"`            | Teks/string                   |
| 4  | `BOOLEAN`  | `TRUE` / `FALSE`    | `bener`, `salah`    | Nilai kebenaran               |
| 5  | `ANY`      | *(parameter fungsi)*| —                   | Tipe dinamis (belum diketahui)|

---

## 5. Aturan Semantik (Validasi)

### 5.1 Aturan Variabel

| No | Aturan                                         | Pesan Error (Boso Jowo)                                                    |
|----|-------------------------------------------------|----------------------------------------------------------------------------|
| 1  | Variabel harus dideklarasikan sebelum digunakan | `Variabel 'x' durung dideklarasikake (belum dideklarasikan).`              |
| 2  | Variabel tidak boleh dideklarasikan ulang di scope yang sama | `Variabel 'x' wis dideklarasikake (sudah dideklarasikan) ing scope iki.` |
| 3  | Konstanta (`ginaris`) tidak boleh diubah nilainya | `Variabel 'x' iku ginaris (konstanta), ora bisa diowahi (tidak bisa diubah).` |

### 5.2 Aturan Fungsi

| No | Aturan                                          | Pesan Error (Boso Jowo)                                                    |
|----|-------------------------------------------------|----------------------------------------------------------------------------|
| 1  | Fungsi harus dideklarasikan sebelum dipanggil   | `Fungsi 'f' durung dideklarasikake.`                                       |
| 2  | Jumlah argumen harus sesuai parameter           | `Fungsi 'f' butuh 2 argumen, nanging diwenehi 3 argumen.`                 |
| 3  | `balekno` hanya boleh di dalam fungsi           | `Pernyataan 'balekno' (return) kudu ana ing njero fungsi.`                 |

### 5.3 Aturan Operasi Tipe Data

| No | Aturan                                                     | Pesan Error                                                              |
|----|------------------------------------------------------------|--------------------------------------------------------------------------|
| 1  | Operasi `-`, `*`, `/` tidak berlaku untuk tipe `STRING`    | `Operasi aritmatika '-' ora kena kanggo tipe data STRING.`               |
| 2  | Operator perbandingan menghasilkan tipe `BOOLEAN`          | —                                                                        |
| 3  | Operator logika (`lan`, `utawa`) menghasilkan tipe `BOOLEAN` | —                                                                      |

---

## 6. Contoh Tabel Simbol Lengkap

### Kode Sumber:
```
wadah nama = "Dito";
ginaris umur = 21;
wadah aktif = bener;

fungsi sapa(pesan) {
    wadah hasil = pesan + " " + nama;
    balekno hasil;
}

wadah output = sapa("Halo");
tulis(output);
```

### Tabel Simbol — Scope Global:

| No | Nama       | Tipe Data | Konstanta | Scope  |
|----|------------|-----------|-----------|--------|
| 1  | `nama`     | `STRING`  | Tidak     | Global |
| 2  | `umur`     | `NUMBER`  | Ya        | Global |
| 3  | `aktif`    | `BOOLEAN` | Tidak     | Global |
| 4  | `output`   | `ANY`     | Tidak     | Global |

### Tabel Simbol — Scope Fungsi `sapa`:

| No | Nama       | Tipe Data | Konstanta | Scope        |
|----|------------|-----------|-----------|--------------|
| 1  | `pesan`    | `ANY`     | Tidak     | Fungsi: sapa |
| 2  | `hasil`    | `STRING`  | Tidak     | Fungsi: sapa |

### Tabel Fungsi:

| No | Nama Fungsi | Jumlah Parameter |
|----|-------------|------------------|
| 1  | `sapa`      | 1                |

---

## 7. Diagram Alur Analisis Semantik

```
Kode Sumber (.jowo)
        │
        ▼
   ┌──────────┐
   │  Lexer   │  → Menghasilkan Token
   └────┬─────┘
        │
        ▼
   ┌──────────┐
   │  Parser  │  → Menghasilkan AST
   └────┬─────┘
        │
        ▼
   ┌────────────────────┐
   │ Semantic Analyzer  │
   │                    │
   │  ┌──────────────┐  │
   │  │ Symbol Table │  │  → Menyimpan variabel & fungsi
   │  │  (Scoped)    │  │
   │  └──────────────┘  │
   │                    │
   │  Validasi:         │
   │  ✓ Deklarasi       │
   │  ✓ Tipe Data       │
   │  ✓ Konstanta       │
   │  ✓ Scope           │
   └────────┬───────────┘
            │
            ▼
     AST yang Tervalidasi
            │
            ▼
   ┌──────────────┐
   │  Code Gen    │  → Menghasilkan kode Python (.py)
   └──────────────┘
```
