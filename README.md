<div align="center">

<!-- ============================================================ -->
<!-- HEADER BANNER WITH LOGO                                       -->
<!-- ============================================================ -->

<img src="https://www.kehutanan.go.id/images/logo.png" alt="Logo Kementerian Kehutanan" width="120" />

# 🌿IPSDH — Sortir Bukti Dukung SIMOJANG

### **SIGAP Award 2025**

**Sistem Otomasi Penggabungan & Penyortiran Bukti Dukung**
*Direktorat Inventarisasi dan Pemantauan Sumber Daya Hutan (IPSDH)*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Engine-FF6F00?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](https://www.reportlab.com)
[![Pillow](https://img.shields.io/badge/Pillow-Image_Processing-8B5CF6?style=for-the-badge&logo=python&logoColor=white)](https://pillow.readthedocs.io)
[![pypdf](https://img.shields.io/badge/pypdf-PDF_Merge-E53E3E?style=for-the-badge&logo=files&logoColor=white)](https://pypdf.readthedocs.io)
[![License](https://img.shields.io/badge/Internal-Kemenhut-1B5E20?style=for-the-badge&logo=shield&logoColor=white)](#)

---

<p>
  <strong>Mengotomasi proses penggabungan ribuan file bukti dukung dari seluruh BPKH & Produsen DG se-Indonesia menjadi dokumen PDF terstruktur per-soal penilaian SIGAP Award 2025.</strong>
</p>

</div>

---

## 📋 Daftar Isi

- [🎯 Tentang Proyek](#-tentang-proyek)
- [✨ Fitur Utama](#-fitur-utama)
- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
- [📁 Struktur Folder](#-struktur-folder)
- [⚙️ Instalasi & Persiapan](#️-instalasi--persiapan)
- [🚀 Cara Penggunaan](#-cara-penggunaan)
- [📊 Daftar Soal Penilaian](#-daftar-soal-penilaian)
- [🔧 Konfigurasi](#-konfigurasi)
- [📝 Format Output](#-format-output)
- [🤝 Tim Pengembang](#-tim-pengembang)

---

## 🎯 Tentang Proyek

<table>
<tr>
<td width="60%">

**SIMOJANG Sortir Bukti Dukung** adalah *toolkit* otomasi Python yang dikembangkan untuk mendukung proses penilaian **SIGAP Award 2025** di lingkungan Kementerian Kehutanan RI. Sistem ini menyelesaikan masalah penggabungan dan penyortiran **ribuan file bukti dukung** (PDF, gambar) yang dikumpulkan dari seluruh unit kerja se-Indonesia.

Proyek ini terdiri dari **dua script utama** yang masing-masing menangani kategori penilaian berbeda:

| Script | Kategori | Jumlah Soal |
|--------|----------|:-----------:|
| `merge_bukti_dukung.py` | **BPKH** (Balai Pemantapan Kawasan Hutan) | 28 soal |
| `merge_bukti_dukung_produsen_dg.py` | **Produsen DG** (Data Geospasial) | 38 soal |

</td>
<td width="40%" align="center">

```
    🌲🌲🌲
   🌲🌲🌲🌲🌲
  📄 → 📑 → 📕
   BPKH I..XXII
  Produsen 1..N
    🌲🌲🌲
```

**Dari ribuan file tersebar**
**→ menjadi PDF terstruktur**

</td>
</tr>
</table>

---

## ✨ Fitur Utama

<table>
<tr>
<td align="center" width="25%">
<h3>📂</h3>
<strong>Auto-Scan</strong><br/>
Pemindaian otomatis seluruh folder BPKH/Produsen DG dan pengindeksan file berdasarkan nomor soal
</td>
<td align="center" width="25%">
<h3>🔀</h3>
<strong>Smart Sort</strong><br/>
Pengurutan BPKH berdasarkan angka Romawi (I→XXII) dan Produsen DG secara alfabetis
</td>
<td align="center" width="25%">
<h3>📄</h3>
<strong>Multi-Format</strong><br/>
Mendukung file PDF, PNG, JPG, JPEG, dan WebP — konversi otomatis gambar ke halaman A4
</td>
<td align="center" width="25%">
<h3>📊</h3>
<strong>Summary Report</strong><br/>
Laporan ringkasan lengkap jumlah file yang submitted vs missing per soal
</td>
</tr>
</table>

<table>
<tr>
<td align="center" width="25%">
<h3>📑</h3>
<strong>Cover Page</strong><br/>
Halaman sampul profesional untuk setiap soal penilaian
</td>
<td align="center" width="25%">
<h3>🟢</h3>
<strong>Separator Page</strong><br/>
Halaman pemisah hijau gelap (<code>#1B5E20</code>) antar BPKH/Produsen
</td>
<td align="center" width="25%">
<h3>⚠️</h3>
<strong>Missing Alert</strong><br/>
Halaman kuning peringatan untuk unit kerja yang belum melampirkan bukti dukung
</td>
<td align="center" width="25%">
<h3>⏭️</h3>
<strong>Skip Logic</strong><br/>
Soal tanpa bukti dukung otomatis di-skip sesuai konfigurasi
</td>
</tr>
</table>

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    SIGAP Award 2025                      │
│              Sortir Bukti Dukung Pipeline                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                   │
│  │  BPKH Script │    │ Produsen DG  │                   │
│  │  (22 BPKH    │    │   Script     │                   │
│  │   Wilayah)   │    │ (N Instansi) │                   │
│  └──────┬───────┘    └──────┬───────┘                   │
│         │                   │                           │
│         ▼                   ▼                           │
│  ┌─────────────────────────────────────┐                │
│  │        Step 1: SCAN & INDEX         │                │
│  │  • Deteksi folder BPKH/Produsen    │                │
│  │  • Parse filename → question key    │                │
│  │  • Build index per soal × instansi  │                │
│  └──────────────┬──────────────────────┘                │
│                 ▼                                       │
│  ┌─────────────────────────────────────┐                │
│  │        Step 2: MERGE & BUILD        │                │
│  │  • Generate Cover Page (white)      │                │
│  │  • Generate Separator Page (green)  │                │
│  │  • Append files / Missing Page      │                │
│  │  • Convert images → A4 PDF          │                │
│  └──────────────┬──────────────────────┘                │
│                 ▼                                       │
│  ┌─────────────────────────────────────┐                │
│  │       Step 3: OUTPUT & SUMMARY      │                │
│  │  • Write MERGED_{soal}.pdf          │                │
│  │  • Print summary table              │                │
│  └─────────────────────────────────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Struktur Folder

```
simojang-sortir-buktidukung/
│
├── 📄 merge_bukti_dukung.py              # Script utama BPKH
├── 📄 merge_bukti_dukung_produsen_dg.py   # Script utama Produsen DG
│
├── 📁 bpkh/                               # 📥 Input — Bukti Dukung BPKH
│   ├── bpkh_wilayah_i_medan/
│   │   ├── no_1_1_sk_pokja.pdf
│   │   ├── no_2_1_surat_edaran.pdf
│   │   └── no_5_1_inovasi.png
│   ├── bpkh_wilayah_ii_palembang/
│   ├── bpkh_wilayah_iii_banjarmasin/
│   └── ... (s.d. bpkh_wilayah_xxii_...)
│
├── 📁 produsen_form/                      # 📥 Input — Bukti Dukung Produsen DG
│   ├── produsen_bina_usaha_pemanfaatan_hutan/
│   │   ├── no_1_1_sk_tim.pdf
│   │   └── no_4_1_geodetik.jpg
│   ├── produsen_planologi_kehutanan/
│   └── ... (N instansi produsen)
│
├── 📁 output/                             # 📤 Output — BPKH Merged PDFs
│   ├── 1_1_pembentukan_kelompok_kerja_dan_kelembagaan/
│   │   └── MERGED_1_1_pembentukan_kelompok_kerja_dan_kelembagaan.pdf
│   ├── 2_1_berbagi_data/
│   │   └── MERGED_2_1_berbagi_data.pdf
│   └── ...
│
├── 📁 produsen_output/                    # 📤 Output — Produsen DG Merged PDFs
│   ├── 1_1_pembentukan_kelompok_kerja/
│   │   └── MERGED_1_1_pembentukan_kelompok_kerja.pdf
│   └── ...
│
├── 📄 SIGAP_AWARD_2025_Daftar_Soal_bpkh.txt
├── 📄 SIGAP_AWARD_2025_Daftar_Soal_produsen.txt
├── 📄 BPKH - HASIL BUKTI DUKUNG DAN FORM PENILAIAN SIGAP AWARD 2025.xlsx
├── 📄 PRODUSEN DG - HASI BUKTI DUKUNG DAN FORM PENILAIAN SIGAP AWARD 2025.xlsx
├── 📄 .gitignore
└── 📄 README.md                           # ← Anda di sini!
```

---

## ⚙️ Instalasi & Persiapan

### Prasyarat

| Komponen | Versi Minimum | Keterangan |
|----------|:------------:|------------|
| 🐍 Python | 3.10+ | Menggunakan fitur `type union` (`str \| None`) |
| 📦 pip | terbaru | Package manager Python |

### Langkah Instalasi

**1. Clone repository**

```bash
git clone https://github.com/HolitSky/sortir-buktidukung-sigapaward.git
cd sortir-buktidukung-sigapaward
```

**2. Install dependencies**

```bash
pip install Pillow reportlab pypdf
```

| Package | Kegunaan |
|---------|----------|
| `Pillow` | Memproses dan mengkonversi gambar (PNG, JPG, WebP) |
| `reportlab` | Membuat halaman PDF (cover, separator, missing alert) |
| `pypdf` | Membaca dan menggabungkan file PDF |

**3. Siapkan folder input**

Pastikan struktur folder `bpkh/` dan/atau `produsen_form/` sudah terisi dengan file bukti dukung sesuai konvensi penamaan:

```
no_{X}_{Y}_{deskripsi}.{ext}
```

> **Contoh:** `no_1_1_sk_pokja_jaringan_digt.pdf`, `no_5_2_foto_server.jpg`

---

## 🚀 Cara Penggunaan

### Script 1 — Merge Bukti Dukung BPKH

```bash
python merge_bukti_dukung.py
```

<details>
<summary>📋 <strong>Contoh Output Console</strong> (klik untuk expand)</summary>

```
=================================================================
  Merge Bukti Dukung — SIGAP Award 2025
=================================================================

[1/3] Scanning: D:\...\bpkh
      Found 22 BPKH folders (sorted):
        • BPKH WILAYAH I - MEDAN
        • BPKH WILAYAH II - PALEMBANG
        • BPKH WILAYAH III - BANJARMASIN
        • ...

[2/3] Merging 24 questions (4 skipped) → output

  ✔ 1_1  →  MERGED_1_1_pembentukan_kelompok_kerja_dan_kelembagaan.pdf  (20 submitted, 2 missing)
  ✔ 1_3  →  MERGED_1_3_strategi_geospasial.pdf  (22 submitted, 0 missing)
  –  1_2  →  SKIPPED (no bukti dukung required)
  ...

[3/3] Done!
=================================================================
=== SUMMARY ===
=================================================================
Question | Total BPKH | Submitted | Missing
-----------------------------------------------------------------
1_1      |         22 |        20 |       2
1_3      |         22 |        22 |       0
...
=================================================================
```

</details>

---

### Script 2 — Merge Bukti Dukung Produsen DG

```bash
python merge_bukti_dukung_produsen_dg.py
```

<details>
<summary>📋 <strong>Contoh Output Console</strong> (klik untuk expand)</summary>

```
=================================================================
  Merge Bukti Dukung — SIGAP Award 2025 (PRODUSEN DG)
=================================================================

[1/3] Scanning: D:\...\produsen_form
      Found N Produsen DG folders (sorted):
        • PRODUSEN DG - BINA USAHA PEMANFAATAN HUTAN
        • PRODUSEN DG - PLANOLOGI KEHUTANAN
        • ...

[2/3] Merging 28 questions (10 skipped) → produsen_output

  ✔  1_1  →  MERGED_1_1_pembentukan_kelompok_kerja.pdf  (N submitted, M missing)
  ...

[3/3] Done!
=================================================================
=== SUMMARY ===
=================================================================
```

</details>

---

## 📊 Daftar Soal Penilaian

### 🏢 Kategori BPKH — 28 Soal

<details>
<summary><strong>📋 Pilar 1 — Tata Kelola & Kelembagaan</strong> (4 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 1.1 | Pembentukan Kelompok Kerja & Kelembagaan | ✅ SK Terbaru |
| 1.2 | Peran Geospasial Kelembagaan | ❌ Tidak perlu |
| 1.3 | Strategi Geospasial | ✅ Renstra/Roadmap |
| 1.4 | Pemantauan dan Evaluasi / Indikator Keberhasilan | ✅ Dokumen Laporan |

</details>

<details>
<summary><strong>📋 Pilar 2 — Kebijakan & Hukum</strong> (2 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 2.1 | Berbagi Data | ✅ Dokumen Regulasi |
| 2.2 | Strategi Kepatuhan | ✅ BAST/Pakta Integritas |

</details>

<details>
<summary><strong>📋 Pilar 3 — Keuangan</strong> (2 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 3.1 | Tata Kelola Keuangan dan Akuntabilitas | ✅ RKAKL |
| 3.2 | Sumber Pendanaan | ✅ Agreement/AWP |

</details>

<details>
<summary><strong>📋 Pilar 4 — Data</strong> (2 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 4.1 | Berbagi Data (SOP) | ✅ SOP/Alur |
| 4.2 | Penyimpanan dan Pengambilan Data | ✅ Foto Media Penyimpanan |

</details>

<details>
<summary><strong>📋 Pilar 5 — Inovasi & Teknologi</strong> (4 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 5.1 | Strategi Inovasi Geospasial | ✅ Deskripsi Inovasi |
| 5.2 | Infrastruktur ICT Inti | ✅ Dokumentasi Sarana |
| 5.3 | Modernisasi Aset Data | ✅ Screenshot Lisensi |
| 5.4 | Sistem Terpadu dari Sistem | ✅ Dokumentasi |

</details>

<details>
<summary><strong>📋 Pilar 6 — Standar</strong> (1 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 6.1 | ISO 9001:2015 Manajemen Mutu | ✅ Dokumen ISO |

</details>

<details>
<summary><strong>📋 Pilar 7 — Kemitraan</strong> (3 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 7.1 | Kesadaran dan Peluang Kemitraan | ✅ Dokumentasi Kegiatan |
| 7.2 | Kolaborasi Lintas Sektor | ✅ Dokumentasi Kegiatan |
| 7.3 | Mengelola Kemitraan | ❌ Tidak perlu |

</details>

<details>
<summary><strong>📋 Pilar 8 — Kapasitas SDM</strong> (7 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 8.1 | Kelompok Kerja Peningkatan Kapasitas | ✅ Surat Dukung |
| 8.2 | Penilaian dan Analisis | ✅ Hasil Analisis |
| 8.3 | Strategi dan Rencana Implementasi | ❌ Tidak perlu |
| 8.4 | Program Pendidikan Tinggi | ✅ Surat/Dokumentasi |
| 8.5 | Pendekatan Pengembangan Profesional | ✅ Surat/Dokumentasi |
| 8.6 | JF Surveyor Pemetaan | ✅ SK/Karpeg |
| 8.7 | JF Pranata Komputer | ✅ SK/Karpeg |

</details>

<details>
<summary><strong>📋 Pilar 9 — Komunikasi</strong> (3 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 9.1 | Tata Kelola Komunikasi | ❌ Tidak perlu |
| 9.2 | Tim Komunikasi | ❌ Tidak perlu |
| 9.3 | Penggunaan DIGT oleh Pengguna | ✅ Analisis Penggunaan |

</details>

---

### 🏭 Kategori Produsen DG — 38 Soal

<details>
<summary><strong>📋 Pilar 1 — Tata Kelola & Kelembagaan</strong> (3 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 1.1 | Pembentukan Kelompok Kerja | ✅ SK Terbaru |
| 1.2 | Peran Geospasial Kelembagaan | ❌ Tidak perlu |
| 1.3 | Strategi Geospasial | ✅ Renstra/Roadmap |

</details>

<details>
<summary><strong>📋 Pilar 2 — Kebijakan & Hukum</strong> (2 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 2.1 | Berbagi Data | ✅ Dokumen Kebijakan |
| 2.2 | Hak Kekayaan Intelektual | ✅ Dokumen HKI |

</details>

<details>
<summary><strong>📋 Pilar 3 — Keuangan</strong> (2 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 3.1 | Tata Kelola Keuangan dan Akuntabilitas | ✅ RKAKL |
| 3.2 | Sumber Pendanaan | ✅ Agreement/AWP |

</details>

<details>
<summary><strong>📋 Pilar 4 — Data</strong> (9 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 4.1 | Infrastruktur Geodetik | ✅ Dokumentasi |
| 4.2 | Inventaris Data dan Profil Data | ✅ Dokumentasi |
| 4.3 | Analisis Kesenjangan Data | ✅ Dokumentasi |
| 4.4 | Peta Jalan Tema Data | ❌ Tidak perlu |
| 4.5 | Kualitas Data | ✅ Dokumentasi |
| 4.6 | Metadata | ✅ Dokumentasi |
| 4.7 | Penyimpanan dan Pengambilan Data | ✅ Dokumentasi |
| 4.8 | Siklus Aliran Data | ✅ SOP |
| 4.9 | Interoperabilitas Data | ✅ Dokumentasi |

</details>

<details>
<summary><strong>📋 Pilar 5 — Inovasi & Teknologi</strong> (5 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 5.1 | Strategi Inovasi Geospasial | ✅ Deskripsi Inovasi |
| 5.2 | Infrastruktur ICT Inti | ✅ Dokumentasi |
| 5.3 | Modernisasi Aset Data | ✅ Screenshot Lisensi |
| 5.4 | Sistem Inovasi Nasional | ❌ Tidak perlu |
| 5.5 | Sistem Terpadu dari Sistem | ✅ Dokumentasi |

</details>

<details>
<summary><strong>📋 Pilar 6 — Standar</strong> (4 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 6.1 | Tata Kelola Standar | ✅ Standar Penyusunan IGT |
| 6.2 | Strategi/Rencana Standar | ❌ Tidak perlu |
| 6.3 | Implementasi | ✅ Standar Teknologi |
| 6.4 | Kepatuhan Standar | ❌ Tidak perlu |

</details>

<details>
<summary><strong>📋 Pilar 7 — Kemitraan</strong> (3 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 7.1 | Kesadaran dan Peluang Kemitraan | ✅ Dokumentasi/Perjanjian |
| 7.2 | Kolaborasi Lintas Sektor | ✅ Dokumentasi/Perjanjian |
| 7.3 | Mengelola Kemitraan | ❌ Tidak perlu |

</details>

<details>
<summary><strong>📋 Pilar 8 — Kapasitas SDM</strong> (7 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 8.1 | Kelompok Kerja Peningkatan Kapasitas | ✅ Surat Dukung |
| 8.2 | Penilaian dan Analisis | ✅ Analisis Kebutuhan |
| 8.3 | Strategi dan Rencana Implementasi | ❌ Tidak perlu |
| 8.4 | Program Pendidikan Tinggi | ✅ Surat/Dokumentasi |
| 8.5 | Pendekatan Pengembangan Profesional | ✅ Surat/Dokumentasi |
| 8.6 | JF Surveyor Pemetaan | ✅ SK/Karpeg |
| 8.7 | JF Pranata Komputer | ✅ SK/Karpeg |

</details>

<details>
<summary><strong>📋 Pilar 9 — Komunikasi</strong> (3 soal)</summary>

| No | Soal | Bukti Dukung |
|----|------|:------------:|
| 9.1 | Tata Kelola Komunikasi | ❌ Tidak perlu |
| 9.2 | Basis Data Studi Kasus | ❌ Tidak perlu |
| 9.3 | Tautan ke SDGs | ❌ Tidak perlu |

</details>

---

## 🔧 Konfigurasi

### Konvensi Penamaan File

Sistem mengenali file bukti dukung berdasarkan **pola nama file** berikut:

```
no_{PILAR}_{SOAL}_{deskripsi_bebas}.{ekstensi}
```

| Bagian | Contoh | Keterangan |
|--------|--------|------------|
| `no_` | — | Prefix wajib (case-insensitive) |
| `{PILAR}` | `1`, `5`, `9` | Nomor pilar penilaian |
| `{SOAL}` | `1`, `2`, `3` | Nomor soal dalam pilar |
| `{deskripsi}` | `sk_pokja`, `foto_server` | Deskripsi bebas (diabaikan oleh parser) |
| `{ekstensi}` | `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp` | Format file yang didukung |

### Format File yang Didukung

| Format | Ekstensi | Perlakuan |
|--------|----------|-----------|
| 📄 PDF | `.pdf` | Langsung digabungkan (all pages) |
| 🖼️ PNG | `.png` | Dikonversi ke halaman A4 (fit, maintain aspect ratio) |
| 🖼️ JPEG | `.jpg`, `.jpeg` | Dikonversi ke halaman A4 (fit, maintain aspect ratio) |
| 🖼️ WebP | `.webp` | Dikonversi ke halaman A4 (fit, maintain aspect ratio) |

### Konvensi Penamaan Folder BPKH

```
bpkh_wilayah_{romawi}_{kota}
```

> **Contoh:** `bpkh_wilayah_i_medan`, `bpkh_wilayah_xii_tanjungredeb`

Folder diurutkan berdasarkan **angka Romawi** (I → XXII).

### Konvensi Penamaan Folder Produsen DG

```
produsen_{nama_instansi}
```

> **Contoh:** `produsen_bina_usaha_pemanfaatan_hutan`, `produsen_planologi_kehutanan`

Folder diurutkan secara **alfabetis**.

---

## 📝 Format Output

Setiap file `MERGED_{soal}.pdf` yang dihasilkan memiliki struktur halaman berikut:

```
┌─────────────────────────┐
│    📄 COVER PAGE        │  ← Halaman putih, judul soal
│    (White Background)    │     + "SIGAP Award 2025"
├─────────────────────────┤
│  🟩 SEPARATOR PAGE      │  ← Halaman hijau gelap (#1B5E20)
│  "BPKH WILAYAH I -     │     + nama instansi
│       MEDAN"            │
├─────────────────────────┤
│  📎 Bukti Dukung #1     │  ← File PDF / gambar yang
│  📎 Bukti Dukung #2     │     di-upload instansi
│  ...                    │
├─────────────────────────┤
│  🟩 SEPARATOR PAGE      │  ← Instansi berikutnya
│  "BPKH WILAYAH II -    │
│     PALEMBANG"          │
├─────────────────────────┤
│  📎 Bukti Dukung #1     │
│  ...                    │
├─────────────────────────┤
│  🟩 SEPARATOR PAGE      │
│  "BPKH WILAYAH III"    │
├─────────────────────────┤
│  🟡 MISSING PAGE        │  ← Halaman kuning (#FFF9C4)
│  "⚠ BELUM MELAMPIRKAN  │     jika instansi belum
│   BUKTI DUKUNG"         │     mengirim file
└─────────────────────────┘
```

### Palet Warna Halaman

| Halaman | Background | Foreground | Kode Warna |
|---------|:----------:|:----------:|:----------:|
| Cover Page | ⬜ Putih | ⬛ Hitam | `#FFFFFF` |
| Separator Page | 🟩 Hijau Gelap | ⬜ Putih | `#1B5E20` |
| Missing Page | 🟨 Kuning Muda | 🟧 Amber | `#FFF9C4` / `#F57F17` |

---

## 🧩 Alur Kerja Teknis

```
                          ┌──────────────┐
                          │  START       │
                          └──────┬───────┘
                                 │
                    ┌────────────▼────────────┐
                    │  scan_bpkh_folders()    │
                    │  atau                   │
                    │  scan_produsen_folders() │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────▼───────────────────┐
              │  parse_question_key(filename)         │
              │  "no_1_1_sk_pokja.pdf" → "1_1"       │
              └──────────────────┬───────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Loop: QUESTION_MAP     │
                    │  (skip NO_BUKTI_DUKUNG) │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────▼───────────────────┐
              │  merge_question(q_key, q_folder, ...) │
              │                                       │
              │  ┌─ make_cover_page()                 │
              │  │                                    │
              │  ├─ for each instansi:                │
              │  │   ├─ make_separator_page()         │
              │  │   ├─ if files: append_file()       │
              │  │   └─ else: make_missing_page()     │
              │  │                                    │
              │  └─ PdfWriter.write(output)           │
              └──────────────────┬───────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  print_summary()        │
                    │  (table output)         │
                    └────────────┬────────────┘
                                 │
                          ┌──────▼───────┐
                          │     END      │
                          └──────────────┘
```

---

## ⚠️ Troubleshooting

<details>
<summary><strong>❌ FileNotFoundError: BPKH input directory not found</strong></summary>

Pastikan folder `bpkh/` ada di direktori yang sama dengan script. Buat folder tersebut dan isi dengan subfolder BPKH.

```bash
mkdir bpkh
mkdir bpkh\bpkh_wilayah_i_medan
```

</details>

<details>
<summary><strong>❌ ModuleNotFoundError: No module named 'reportlab'</strong></summary>

Install dependensi yang dibutuhkan:

```bash
pip install Pillow reportlab pypdf
```

</details>

<details>
<summary><strong>⚠️ [WARN] Could not read PDF / Could not convert image</strong></summary>

File mungkin rusak atau menggunakan format yang tidak didukung. Script akan melewatkan file bermasalah dan melanjutkan proses. Periksa file secara manual.

</details>

<details>
<summary><strong>❓ File tidak terdeteksi / soal tidak cocok</strong></summary>

Pastikan nama file mengikuti konvensi:
- **Benar:** `no_1_1_sk_pokja.pdf`
- **Salah:** `sk_pokja_1_1.pdf`, `1_1_sk_pokja.pdf`, `bukti_no1.pdf`

Prefix `no_` diikuti `{pilar}_{soal}_` adalah **wajib**.

</details>

---

## 🤝 Tim Pengembang

<div align="center">

| Organisasi |
|:----------:|
| **Direktorat Inventarisasi dan Pemantauan Sumber Daya Hutan (IPSDH)** |
| Kementerian Kehutanan Republik Indonesia |

---

<sub>

🌿 *Dibangun dengan ikhlas untuk mendukung pengelolaan Data dan Informasi Geospasial Tematik (DIGT) Kehutanan Indonesia* 🌿

**SIGAP Award 2025** — Sistem Informasi Geospasial Alam Peta

</sub>

<img src="https://www.kehutanan.go.id/images/logo.png" alt="Logo Kementerian Kehutanan" width="64" />

</div>
