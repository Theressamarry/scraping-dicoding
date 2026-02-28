# Dicoding Offering Scraper

Sebuah script Python untuk melakukan scraping data peserta dari halaman Coding Camp Offering di Dicoding dan menyimpannya ke file CSV serta Excel.

---

## Deskripsi

Program ini akan:

- Mengecek jumlah total halaman dari pagination.
- Mengambil data tabel pada setiap halaman.
- Mengumpulkan data:
  - **Nomor**
  - **Nama Siswa**
  - **Asal Sekolah/Universitas**
- Menyimpan hasil scraping ke:
  - `dicoding_offering_data.csv`
  - `dicoding_offering_data.xlsx`
- Menampilkan daftar siswa dari **Universitas Pembangunan Nasional Veteran Jawa Timur** (jika ada).

---

## Teknologi yang Digunakan

- Python
- `requests`
- `BeautifulSoup` (bs4)
- `pandas`
- `openpyxl`

---

## Alur Proses Scraping

### 1. Mengecek Total Halaman

- Mengakses halaman pertama.
- Membaca pagination.
- Mengambil angka halaman terbesar.
- Jika gagal, otomatis menggunakan 1 halaman.

---

### 2. Mengambil Data Per Halaman

Untuk setiap halaman:

- Mengirim request ke URL.
- Mencari elemen `<table>`.
- Mengambil seluruh baris data (`<tr>`).
- Mengekstrak:
  - No
  - Nama
  - Asal Sekolah/Universitas
- Menyimpan ke dalam list data.

---

### 3. Membuat DataFrame

Seluruh data dikonversi menjadi `pandas.DataFrame`.

---

### 4. Menyimpan ke File

- Disimpan ke CSV dengan encoding UTF-8.
- Dicoba juga simpan ke Excel menggunakan `openpyxl`.
- Jika penyimpanan Excel gagal, program tetap berjalan.

---

### 5. Filter Data Universitas Tertentu

Program memfilter data berdasarkan teks:

Universitas Pembangunan Nasional Veteran Jawa Timur

Jika ditemukan:

- Ditampilkan daftar nama mahasiswa.
- Ditampilkan total jumlah mahasiswa.

Jika tidak ditemukan:

- Akan muncul pesan bahwa data tidak tersedia.

---

## Cara Menjalankann

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### 2. Jalankan Program

```bash
python scrape_dicoding_offering.py
```

---

## Output yang Dihasilkan

- `dicoding_offering_data.csv`
- `dicoding_offering_data.xlsx`
- Preview 10 data pertama di terminal
- Total data yang berhasil diambil
- Daftar mahasiswa UPN Veteran Jawa Timur (jika ada)

---

## Tujuan

Script ini dibuat untuk:

- Mengumpulkan data peserta secara otomatis.
- Mempermudah analisis data.
- Melakukan filtering berdasarkan institusi tertentu.