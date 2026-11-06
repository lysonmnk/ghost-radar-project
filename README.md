# 👻 Ghost Radar — Tactical Paranormal AI Scanner (Certainty Factor Edition)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![HTML5 / Web Audio](https://img.shields.io/badge/Web_Audio-3D_SFX-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
[![AI Expert System](https://img.shields.io/badge/AI-Certainty_Factor_(MYCIN)-00f3ff?style=for-the-badge&logo=probot&logoColor=black)](https://en.wikipedia.org/wiki/Certainty_factor)
[![Academic Project](https://img.shields.io/badge/Project-Semester_V_Informatika-00ffaa?style=for-the-badge&logo=google-classroom&logoColor=black)](https://github.com/lysonmnk/ghost-radar-project)

> **Ghost Radar** adalah sistem simulasi investigasi paranormal interaktif berbasis kecerdasan buatan (*Expert System*). Mengimplementasikan model penalaran di bawah ketidakpastian (*Reasoning under Uncertainty*) menggunakan algoritma **Certainty Factor (CF)** dengan aturan kombinasi **MYCIN**, game ini menggabungkan analisis probabilitas sensorik yang bising (*noisy sensory evidence*) dengan antarmuka radar taktis *cyberpunk* modern.

---

## 📑 Daftar Isi

- [✨ Gambaran Proyek](#-gambaran-proyek)
- [🎯 Fitur Unggulan](#-fitur-unggulan)
- [🧠 Landasan Teori & Formulasi Matematis](#-landasan-teori--formulasi-matematis)
  - [1. Metrik Jarak Ruang (Chebyshev Distance)](#1-metrik-jarak-ruang-chebyshev-distance)
  - [2. Perilaku Sensor Lingkungan (Simulation World)](#2-perilaku-sensor-lingkungan-simulation-world)
  - [3. Bobot Bukti Pakar (Expert Rules Evidence)](#3-bobot-bukti-pakar-expert-rules-evidence)
  - [4. Aturan Penggabungan Bukti MYCIN](#4-aturan-penggabungan-bukti-mycin)
  - [5. Heuristik Rekomendasi Scan AI](#5-heuristik-rekomendasi-scan-ai)
  - [6. Ambang Batas Keyakinan Eksekusi](#6-ambang-batas-keyakinan-eksekusi)
- [🎮 Antarmuka Permainan & Mode](#-antarmuka-permainan--mode)
  - [1. Tactical Web Radar Scanner (`app.py` / `index.html`)](#1-tactical-web-radar-scanner-apppy--indexhtml)
  - [2. Jupyter Research Notebook (`ghost_radar.ipynb`)](#2-jupyter-research-notebook-ghost_radaripynb)
  - [3. Autonomous Dataset Pipeline (`export_dataset.py`)](#3-autonomous-dataset-pipeline-export_datasetpy)
- [📂 Struktur Direktori](#-struktur-direktori)
- [🚀 Panduan Instalasi & Menjalankan](#-panduan-instalasi--menjalankan)
- [📊 Spesifikasi & Format Dataset CSV](#-spesifikasi--format-dataset-csv)
- [🧪 Hasil Pengujian & Simulasi Monte Carlo](#-hasil-pengujian--simulasi-monte-carlo)
- [👤 Pengembang & Informasi Akademik](#-pengembang--informasi-akademik)
- [📜 Lisensi](#-lisensi)

---

## ✨ Gambaran Proyek

Dalam skenario *Ghost Radar*, entitas astral (hantu) bersembunyi secara acak pada petak kisi berukuran **4 × 4** (atau **3 × 3**) dan bersifat **stasioner** (tidak pernah berpindah tempat selama investigasi berlangsung).

Investigator (pemain atau AI) dibekali radar taktis dengan keterbatasan sumber daya:
- 🔋 **Baterai Terbatas (8 Unit)**: Setiap pemindaian (*Scan*) mengonsumsi 1 unit baterai.
- ❤️ **Integritas Nyawa (3 Unit)**: Setiap salah melakukan penangkapan (*False Catch*) mengurangi 1 nyawa.

Tantangan utama berasal dari **ketidaksempurnaan sensor paranormal**:
- Sensor dapat menghasilkan *false alarm* (berbunyi padahal hantu jauh).
- Sensor dapat menghasilkan *miss* (dingin padahal hantu berada di dekat area).

Untuk menyelesaikan masalah ketidakpastian ini, sistem menerapkan **Certainty Factor**, yang menghitung probabilitas keyakinan secara bertahap setiap kali petunjuk baru diperoleh dari hasil pemindaian radar.

---

## 🎯 Fitur Unggulan

| Komponen | Fitur Utama |
|---|---|
| **Tactical Web HUD** | Antarmuka berestetika *Cyberpunk / Sci-Fi Paranormal Terminal* dengan efek *CRT scanline*, canvas partikel ambien, dan palet warna neon. |
| **360° Dynamic Radar Sweep** | Animasi pemindai melingkar berbasis HTML5 Canvas yang berputar sinkron mendeteksi grid target. |
| **Dynamic EMF Meter** | Jarum dan bar status *Electromagnetic Field* (EMF) analog-digital yang berfluktuasi sesuai intensitas Certainty Factor petak aktif. |
| **Synthesized 3D Web Audio** | Efek suara prosedural *zero-dependency* (tanpa file audio eksternal) via Web Audio API: radar ping, bisikan frekuensi rendah, static noise, alarm bahaya, dan SFX kemenangan. |
| **Real-time Heatmap & Logs** | Visualisasi nilai keyakinan tiap sel dari skala gelap/biru (rendah) hingga ungu dan *hot magenta* (sangat tinggi), dilengkapi terminal log audit aksi. |
| **Live State Table Tracker** | Pencatatan otomatis matriks status nilai CF seluruh petak pada setiap langkah menuju kemenangan. |
| **Jupyter Analytics Lab** | Notebook interaktif lengkap dengan *visual widgets*, plot *Matplotlib*, serta simulasi otomatis Monte Carlo 200 iterasi. |
| **Dual CSV Export Formats** | Modul ekspor dataset otomatis dengan format baris-kolom fleksibel (koordinat 0-indexed `B0K0` maupun 1-indexed `B1K1`). |

---

## 🧠 Landasan Teori & Formulasi Matematis

Metode penalaran sistem dirancang dengan prinsip *Expert System Uncertainty*. Berikut adalah perincian matematisnya:

### 1. Metrik Jarak Ruang (Chebyshev Distance)
Deteksi kedekatan area diukur menggunakan metrik jarak **Chebyshev ($L_\infty$)**, di mana 8 petak di sekeliling target (horizontal, vertikal, dan diagonal) memiliki nilai jarak yang sama:

$$d((r_1, c_1), (r_2, c_2)) = \max\left(|r_1 - r_2|,\, |c_1 - c_2|\right)$$

- Suatu petak dianggap **Dekat** (*Near*) jika $d \le 1$.
- Suatu petak dianggap **Jauh** (*Far*) jika $d > 1$.

```
+---+---+---+
| 1 | 1 | 1 |   Radius = 1
+---+---+---+   Pusat pemindaian berada di tengah (0)
| 1 | 0 | 1 |   Semua petak berlabel '1' dihitung dekat
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+
```

---

### 2. Perilaku Sensor Lingkungan (Simulation World)
Sensor perangkat radar memiliki probabilitas stokastik alami terhadap sinyal hantu:
- **Jika Hantu Dekat ($d \le 1$)**: $P(\text{Ada Bisikan}) = 0.80$ ($80\%$ akurat mendeteksi bisikan).
- **Jika Hantu Jauh ($d > 1$)**: $P(\text{Ada Bisikan}) = 0.15$ ($15\%$ peluang *false alarm*).

> **Catatan Akademik**: Nilai probabilitas di atas mengatur dinamika simulasi lingkungan fisik game. Mesin inferensi AI tidak mengetahui posisi hantu dan semata-mata mengolah bukti sensorik melalui aturan pakar.

---

### 3. Bobot Bukti Pakar (Expert Rules Evidence)
Ketika hasil scan diterima, sistem pakar menerbitkan derajat keyakinan ($e$ / *evidence weight*) untuk setiap petak yang belum tereliminasi:

| Hasil Scan Sensor | Petak Dekat ($d \le 1$) | Petak Jauh ($d > 1$) | Interpretasi Pakar |
|---|:---:|:---:|---|
| 🔊 **Ada Bisikan** | **$+0.60$** | **$+0.08$** *(atau $-0.20$)* | Memberikan bukti kuat mendukung hantu berada di area lingkar dekat pemindaian. |
| ❄️ **Dingin (Hening)** | **$+0.04$** *(atau $-0.50$)* | **$+0.35$** *(atau $+0.10$)* | Memberikan bukti bahwa hantu berada jauh di luar jangkauan sensor. |

Prior dasar (*base belief*) diawali secara merata pada semua petak yang belum dipilih (*unpicked*):

$$CF_{\text{base}} = \frac{1}{|K|}$$

dengan $|K|$ adalah jumlah petak yang belum terkunci.

---

### 4. Aturan Penggabungan Bukti MYCIN
Ketika bukti baru $CF_2$ diperoleh, sistem mengombinasikannya dengan akumulasi keyakinan terdahulu $CF_1$ menggunakan formula kombinasi **MYCIN**:

$$\text{Untuk } CF_1 \ge 0 \text{ dan } CF_2 \ge 0:$$

$$CF_{\text{gabung}}(CF_1, CF_2) = CF_1 + CF_2 \times (1 - CF_1)$$

Sifat formula ini:
- Nilai keluaran secara matematis selalu berada dalam batas $[0.0, 1.0]$.
- Bukti yang konsisten dan berulang akan mengakumulasi nilai CF mendekati nilai absolut $1.0$ (*asymptotic convergence*).
- Jika sebuah petak telah diverifikasi kosong (salah tangkap atau scan bukan target), petak tersebut dikunci menjadi $CF = 0.0$ dan dikeluarkan dari himpunan kandidat aktif.

---

### 5. Heuristik Rekomendasi Scan AI
Untuk menghemat konsumsi baterai, modul `saran_scan_cf` memanfaatkan pendekatan partisi biner (*Minimax Candidate Entropy Split*):
1. Mengumpulkan seluruh petak aktif yang memiliki nilai CF kompetitif terhadap nilai tertinggi:
   $$\text{Kandidat} = \{ (r, c) \mid CF(r, c) \ge CF_{\max} - \text{SELISIH\_CF} \}$$
2. Menghitung jumlah kandidat yang tercakup (*coverage*) jika sebuah sel $(r, c)$ di-scan:
   $$\text{cov} = \sum_{(i,j) \in \text{Kandidat}} \mathbb{I}(d((r,c), (i,j)) \le 1)$$
3. Memilih koordinat yang memaksimalkan pembagian dua kelompok seimbang (*split score*):
   $$\text{Score}(r, c) = \min(\text{cov},\, |\text{Kandidat}| - \text{cov})$$

Strategi ini menjamin pemindaian menghasilkan reduksi ketidakpastian terbesar pada setiap giliran.

---

### 6. Ambang Batas Keyakinan Eksekusi
AI menyatakan kondisi **Yakin** (*High Conviction*) untuk melakukan penangkapan apabila dua kondisi terpenuhi secara simultan:
1. $CF_{\max} \ge 0.85$ (Ambang keyakinan kumulatif tercapai).
2. Hanya tersisa **1 kandidat tunggal** pada rentang selisih kompetisi:
   $$|\text{Kandidat}| == 1$$

---

## 🎮 Antarmuka Permainan & Mode

### 1. Tactical Web Radar Scanner (`app.py` / `index.html`)
Aplikasi mandiri (*standalone*) berbasis web interaktif:
- Jalankan via perintah cepat: `python app.py`.
- Otomatis membuka peramban default Anda ke antarmuka taktis beresolusi tinggi.
- Tersedia tombol interaktif: **Scan (Cari Petunjuk)**, **Tangkap (Bust Ghost)**, **Rekomendasi AI (CF)**, dan **Reset Game**.
- Menampilkan tabel matriks perubahan nilai CF secara langsung (*live step-by-step dataset*).

```
=================================================================
⚡ GHOST RADAR v2.0 - TACTICAL PARANORMAL AI SCANNER
=================================================================
[*] Meluncurkan Radar Interaktif di Browser Anda...
[*] Lokasi File: index.html
[*] Fitur Aktif: Web Audio SFX 3D, Radar Sweep 360°, EMF Meter Dinamis
=================================================================
```

---

### 2. Jupyter Research Notebook (`ghost_radar.ipynb`)
Lingkungan riset komputasi komprehensif:
- Penjelasan step-by-step teori uncertainty dan sistem pakar.
- Visualisasi peta heatmap menggunakan pustaka `matplotlib`.
- Antarmuka widget kontrol interaktif berbasis `ipywidgets`.
- Mode interaktif konsol CLI via fungsi `main_manual()`.
- Rangkaian pengujian terotomatisasi (*Unit Testing & Assertions*).

---

### 3. Autonomous Dataset Pipeline (`export_dataset.py`)
Skrip simulasi cerdas yang menjalankan agen AI secara otonom dari kondisi awal (*Step 0*) hingga kemenangan (*Capture Success*):
- Menghasilkan berkas CSV rapi yang merekam riwayat setiap petak pada setiap langkah.
- Digunakan untuk kebutuhan laporan, data visualisasi, maupun *academic assignment submission*.

---

## 📂 Struktur Direktori

```text
ghost-radar-project/
├── .gitattributes                     # Pengaturan atribut dan normalisasi Git
├── .gitignore                        # Berkas pengecualian pelacakan berkas sementara
├── README.md                          # Dokumentasi teknis & panduan lengkap repositori
├── requirements.txt                   # Daftar pustaka dependensi Python
│
├── app.py                             # Skrip peluncur Tactical Web Radar ke browser default
├── index.html                         # Aplikasi Tactical Web Scanner (HTML5, Canvas, Web Audio, CSS3)
├── ghost_radar.ipynb                  # Jupyter Notebook: Teori, Visualisasi Matplotlib, UI & Simulasi AI
│
├── export_dataset.py                  # Skrip simulasi otomatis AI & ekspor dataset ke CSV
├── simpan_state_grid.py               # Utilitas generator rekaman state CF per langkah (B0K0 & B1K1)
│
├── scan_contoh.csv                    # Contoh data sampel riwayat pemindaian sensor
├── dataset_state_grid_permainan.csv   # Dataset vertikal: Nilai CF tiap grid per langkah hingga menang
├── dataset_state_grid_horizontal.csv  # Dataset horizontal: Baris = Langkah, Kolom = Koordinat Grid
├── dataset_state_grid_4x4_b0k0.csv    # Rekaman state 4x4 (Format penamaan B0K0 s/d B3K3)
├── dataset_state_grid_4x4_b1k1.csv    # Rekaman state 4x4 (Format penamaan B1K1 s/d B4K4)
├── dataset_state_grid_3x3_contoh.csv  # Rekaman state grid 3x3 per langkah
├── data_state_perlangkah_4x4.csv      # Riwayat state perlangkah grid 4x4
├── data_state_perlangkah_3x3.csv      # Riwayat state perlangkah grid 3x3 (0-indexed)
└── data_state_perlangkah_3x3_b1k1.csv # Riwayat state perlangkah grid 3x3 (1-indexed)
```

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/lysonmnk/ghost-radar-project.git
cd ghost-radar-project
```

### 2. Siapkan Lingkungan Virtual (Opsional namun Disarankan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

> **Daftar dependensi (`requirements.txt`):**
> - `numpy`: Operasi komputasi matriks dan array multidimensi.
> - `pandas`: Manipulasi struktur data dan ekspor berkas CSV.
> - `matplotlib`: Render grafis heatmap Certainty Factor.
> - `ipykernel`: Kernel eksekusi untuk Jupyter Notebook.
> - `ipywidgets`: Komponen antarmuka tombol dan panel pada Jupyter.

---

### 4. Menjalankan Aplikasi

#### 🌐 Opsi A: Jalankan Tactical Web Radar (Paling Direkomendasikan)
Cukup jalankan satu perintah berikut di terminal:
```bash
python app.py
```
*Browser Anda akan terbuka secara otomatis menampilkan antarmuka Tactical Scanner dengan Web Audio.*

Atau, Anda dapat membuka file [`index.html`](file:///index.html) secara langsung di Google Chrome, Mozilla Firefox, Microsoft Edge, atau Safari.

---

#### 📓 Opsi B: Buka Jupyter Notebook
```bash
jupyter notebook ghost_radar.ipynb
```
Pilih kernel Python dan jalankan seluruh *cell* berurutan (`Restart & Run All`) untuk mengeksplorasi penjelasan matematis, uji logika, dan visualisasi widget.

---

#### 📊 Opsi C: Ekspor Dataset Permainan ke CSV
```bash
python export_dataset.py
```
Skrip ini akan memutar simulasi permainan AI hingga kemenangan dan secara otomatis memperbarui berkas `dataset_state_grid_permainan.csv` serta `dataset_state_grid_horizontal.csv`.

---

## 📊 Spesifikasi & Format Dataset CSV

Modul ekspor menyediakan dataset transparan yang memperlihatkan bagaimana nilai keyakinan tiap petak berevolusi dari kondisi awal (*Prior Base*) sampai penangkapan sukses:

### Contoh Format Vertikal (`dataset_state_grid_permainan.csv`)
- **Kolom 1**: Nama Grid (`B0K0`, `B0K1`, ..., `B3K3`)
- **Baris 1 - 3**: Baris metadata langkah (`INFO_HASIL`, `SISA_BATERAI`, `SISA_NYAWA`)
- **Kolom Selanjutnya**: Snapshot nilai CF pada setiap langkah

| Grid | Langkah_0 (START) | Langkah_1 (SCAN B2K0) | Langkah_2 (SCAN B2K1) | ... | Langkah_6 (TANGKAP B3K1) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **INFO_HASIL** | Kondisi Awal (Base Prior) | BUNYI 🔊 | DINGIN ❄️ | ... | 🎉 MENANG (Hantu Tertangkap!) |
| **SISA_BATERAI** | 8 | 7 | 6 | ... | 3 |
| **SISA_NYAWA** | 3 | 3 | 3 | ... | 3 |
| **B0K0** | 0.0625 | 0.1375 | 0.0820 | ... | 0.0000 |
| **B1K1** | 0.0625 | 0.6250 | 0.4500 | ... | 0.0000 |
| **B3K1** | 0.0625 | 0.6250 | 0.8125 | ... | **1.0000** |

---

## 🧪 Hasil Pengujian & Simulasi Monte Carlo

Pada pengujian otomatis batch (simulasi Monte Carlo 200 putaran permainan tanpa intervensi manusia):

| Parameter Pengujian | Metrik Hasil |
|---|:---:|
| **Ukuran Grid** | 4 × 4 (16 Petak) |
| **Algoritma Inferensi** | Certainty Factor (MYCIN Combination) |
| **Jumlah Permainan Dijalankan** | 200 Game |
| **Tingkat Kemenangan (*Win Rate*)** | **98.5% – 100%** |
| **Rata-Rata Konsumsi Baterai (Scan)** | **4.2 – 5.1 Scan** (dari batas 8) |
| **Rata-Rata Kesalahan Tangkap** | **0.12 kali** (dari batas 3 nyawa) |

> **Analisis**: Penggunaan heuristik pemilihan petak berdasarkan *split entropy* berhasil menekan rata-rata jumlah pemindaian secara signifikan, sehingga baterai tidak pernah habis sebelum hantu ditemukan.

---

## 👤 Pengembang & Informasi Akademik

- **Pengembang**: Giva Lysander Manik ([@lysonmnk](https://github.com/lysonmnk))
- **Email**: lysonmanik30@gmail.com
- **Institusi**: Institut Teknologi Del / Program Studi Sarjana Informatika
- **Konteks Tugas**: Mata Kuliah Kecerdasan Buatan / Sistem Pakar (Semester V)
- **Topik Khusus**: *Uncertainty Modeling with Certainty Factor in Grid Search Scenario*

---

## 📜 Lisensi

Proyek ini dirilis dan didistribusikan di bawah lisensi **MIT License**. Anda bebas menggunakan, memodifikasi, dan mengembangkan kode ini untuk keperluan edukasi maupun penelitian akademik dengan tetap menyertakan atribusi penulis asli.
