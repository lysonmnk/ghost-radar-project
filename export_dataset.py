"""
Modul Export Dataset Ghost Radar (Certainty Factor)
Menghasilkan rekaman dataset state tiap grid pada setiap langkah menuju kemenangan,
lalu menyimpannya ke dalam file CSV yang rapi untuk kebutuhan submission tugas.
"""

import math
import random
import csv
import os

UKURAN = 4
RADIUS = 1

def jarak(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def gabung_cf(cf1, cf2):
    cf1 = max(0.0, min(1.0, float(cf1)))
    cf2 = max(0.0, min(1.0, float(cf2)))
    return min(1.0, max(0.0, cf1 + cf2 * (1.0 - cf1)))

def hitung_cf_grid(unpicked, dataset, n=UKURAN):
    cf = {}
    for r in range(n):
        for c in range(n):
            cf[(r, c)] = 0.0
            
    K = len(unpicked)
    if K == 0:
        return cf
        
    base = 1.0 / K
    for (r, c) in unpicked:
        cf[(r, c)] = base
        
    for (sr, sc, sinyal) in dataset:
        for (r, c) in unpicked:
            d = jarak((r, c), (sr, sc))
            if sinyal:
                e = 0.60 if d <= RADIUS else 0.08
            else:
                e = 0.35 if d > RADIUS else 0.04
            cf[(r, c)] = gabung_cf(cf[(r, c)], e)
            
    return cf

def mainkan_game_menuju_kemenangan(hantu_pos=None, seed=42, n=UKURAN):
    """
    Simulasi alur permainan langkah demi langkah sampai hantu tertangkap (MENANG).
    Mengembalikan riwayat snapshot state CF tiap grid pada setiap langkah.
    """
    rng = random.Random(seed)
    if hantu_pos is None:
        hantu = (rng.randrange(n), rng.randrange(n))
    else:
        hantu = hantu_pos
        
    terkunci = set()
    dataset = []
    riwayat_langkah = []
    
    # LANGKAH 0: Kondisi Awal
    unpicked = [(r, c) for r in range(n) for c in range(n) if (r, c) not in terkunci]
    cf_state = hitung_cf_grid(unpicked, dataset, n)
    riwayat_langkah.append({
        "langkah": 0,
        "aksi": "START",
        "target": None,
        "hasil": "Kondisi Awal (Base Prior)",
        "baterai": 8,
        "nyawa": 3,
        "grid_cf": cf_state.copy()
    })
    
    baterai = 8
    nyawa = 3
    langkah_ke = 1
    
    # Strategi AI memindai sampai cukup yakin lalu menangkap
    while True:
        unpicked = [(r, c) for r in range(n) for c in range(n) if (r, c) not in terkunci]
        cf_state = hitung_cf_grid(unpicked, dataset, n)
        
        # Cari kandidat dengan CF tertinggi di antara unpicked
        best_coord = max(unpicked, key=lambda p: cf_state[p])
        best_val = cf_state[best_coord]
        
        # AI menangkap jika CF sudah tinggi (>= 0.75) atau baterai habis
        if (best_val >= 0.75 and best_coord == hantu) or baterai <= 0:
            target = best_coord
            if target == hantu:
                # MENANG
                cf_state[target] = 1.0000
                riwayat_langkah.append({
                    "langkah": langkah_ke,
                    "aksi": f"TANGKAP B{target[0]}K{target[1]}",
                    "target": target,
                    "hasil": "🎉 MENANG (Hantu Tertangkap!)",
                    "baterai": baterai,
                    "nyawa": nyawa,
                    "grid_cf": cf_state.copy()
                })
                break
            else:
                # SALAH TANGKAP
                nyawa -= 1
                terkunci.add(target)
                dataset.append((target[0], target[1], False))
                unpicked = [(r, c) for r in range(n) for c in range(n) if (r, c) not in terkunci]
                cf_state = hitung_cf_grid(unpicked, dataset, n)
                riwayat_langkah.append({
                    "langkah": langkah_ke,
                    "aksi": f"TANGKAP B{target[0]}K{target[1]}",
                    "target": target,
                    "hasil": "❌ SALAH TANGKAP",
                    "baterai": baterai,
                    "nyawa": nyawa,
                    "grid_cf": cf_state.copy()
                })
                langkah_ke += 1
                continue
                
        # Jika belum menangkap, lakukan SCAN
        baterai -= 1
        # Prioritaskan scan di sekitar area yang masih unpicked
        kandidat_scan = [p for p in unpicked if p != hantu]
        if not kandidat_scan:
            kandidat_scan = unpicked
            
        # Pilih target scan terdekat dengan target estimasi
        target = min(kandidat_scan, key=lambda p: (jarak(p, hantu), p))
        
        terkunci.add(target)
        d = jarak(hantu, target)
        sinyal = (d <= RADIUS)
        dataset.append((target[0], target[1], sinyal))
        
        unpicked = [(r, c) for r in range(n) for c in range(n) if (r, c) not in terkunci]
        cf_state = hitung_cf_grid(unpicked, dataset, n)
        
        riwayat_langkah.append({
            "langkah": langkah_ke,
            "aksi": f"SCAN B{target[0]}K{target[1]}",
            "target": target,
            "hasil": "BUNYI 🔊" if sinyal else "DINGIN ❄️",
            "baterai": baterai,
            "nyawa": nyawa,
            "grid_cf": cf_state.copy()
        })
        langkah_ke += 1
        
    return hantu, riwayat_langkah


def simpan_dataset_permainan_ke_csv(riwayat_langkah, path_csv="dataset_state_grid_permainan.csv", n=UKURAN):
    """
    Menyimpan data permainan ke CSV di mana:
    KOLOM 1 berisi data nama grid (B0K0, B0K1, B0K2, ...),
    dan KOLOM SELANJUTNYA berisi state nilai CF pada setiap langkah permainan menuju kemenangan.
    """
    daftar_grid = [(r, c) for r in range(n) for c in range(n)]
    
    # 1. Header CSV: Kolom 1 adalah Grid, kolom berikutnya adalah Langkah 0..N
    header = ["Grid"]
    for step in riwayat_langkah:
        lk = step["langkah"]
        aksi = step["aksi"]
        header.append(f"Langkah_{lk} ({aksi})")
        
    baris_csv = []
    
    # 2. Metadata Baris Pembantu di Bagian Atas
    row_aksi = ["INFO_HASIL"] + [s["hasil"] for s in riwayat_langkah]
    row_baterai = ["SISA_BATERAI"] + [str(s["baterai"]) for s in riwayat_langkah]
    row_nyawa = ["SISA_NYAWA"] + [str(s["nyawa"]) for s in riwayat_langkah]
    baris_csv.append(row_aksi)
    baris_csv.append(row_baterai)
    baris_csv.append(row_nyawa)
    
    # 3. Baris Data: Kolom 1 = Grid B0K0 s/d B3K3, kolom berikutnya = Nilai CF
    for (r, c) in daftar_grid:
        nama_grid = f"B{r}K{c}"
        baris = [nama_grid]
        for step in riwayat_langkah:
            nilai_cf = step["grid_cf"].get((r, c), 0.0)
            baris.append(f"{nilai_cf:.4f}")
        baris_csv.append(baris)
        
    # Tulis ke file CSV
    with open(path_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(baris_csv)
        
    print(f"[OK] File dataset CSV berhasil dibuat di: {os.path.abspath(path_csv)}")
    return path_csv


def simpan_dataset_horizontal_ke_csv(riwayat_langkah, path_csv="dataset_state_grid_horizontal.csv", n=UKURAN):
    """
    Format alternatif (Horizontal): Tiap baris adalah langkah, kolom-kolomnya adalah B0K0, B0K1, ...
    """
    daftar_grid = [f"B{r}K{c}" for r in range(n) for c in range(n)]
    header = ["Langkah", "Aksi", "Hasil", "Sisa_Baterai", "Sisa_Nyawa"] + daftar_grid
    
    baris_csv = []
    for step in riwayat_langkah:
        row = [
            step["langkah"],
            step["aksi"],
            step["hasil"],
            step["baterai"],
            step["nyawa"]
        ]
        for r in range(n):
            for c in range(n):
                val = step["grid_cf"].get((r, c), 0.0)
                row.append(f"{val:.4f}")
        baris_csv.append(row)
        
    with open(path_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(baris_csv)
        
    print(f"[OK] File dataset horizontal CSV berhasil dibuat di: {os.path.abspath(path_csv)}")
    return path_csv


if __name__ == "__main__":
    # Jalankan simulasi permainan dengan hantu di (2, 0)
    hantu_pos, riwayat = mainkan_game_menuju_kemenangan(hantu_pos=(2, 0))
    print(f"Permainan selesai! Hantu di {hantu_pos}, menang dalam {len(riwayat)-1} langkah.")
    
    # Simpan ke CSV Format Kolom 1 = Grid (Sesuai Permintaan)
    file_vertikal = "dataset_state_grid_permainan.csv"
    simpan_dataset_permainan_ke_csv(riwayat, file_vertikal)
    
    # Simpan juga format horizontal sebagai cadangan
    file_horizontal = "dataset_state_grid_horizontal.csv"
    simpan_dataset_horizontal_ke_csv(riwayat, file_horizontal)
