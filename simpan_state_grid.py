import csv
import os

def simpan_state_grid_per_langkah(riwayat_state, path_csv="dataset_state_grid_4x4.csv", format_b1k1=False):
    """
    Menyimpan HANYA data state nilai CF per langkah ke file CSV untuk Grid 4x4.
    
    Format CSV:
    - Kolom 1         : Nama Grid (B0K0 s/d B3K3 atau B1K1 s/d B4K4)
    - Kolom 2 s/d N+1 : State nilai CF per langkah (Langkah_0 s/d Kemenangan)
    """
    total_langkah = len(riwayat_state)
    n_rows = len(riwayat_state[0])
    n_cols = len(riwayat_state[0][0])
    
    # 1. Header: Grid, Langkah_0, Langkah_1, ..., Langkah_N
    header = ["Grid"] + [f"Langkah_{i}" for i in range(total_langkah)]
    
    # 2. Baris Data: Kolom 1 = Grid, Kolom berikutnya = Nilai State
    baris_csv = []
    for r in range(n_rows):
        for c in range(n_cols):
            nama_grid = f"B{r+1}K{c+1}" if format_b1k1 else f"B{r}K{c}"
            baris = [nama_grid]
            for step_idx in range(total_langkah):
                val = riwayat_state[step_idx][r][c]
                baris.append(f"{val:+.2f}")
            baris_csv.append(baris)
            
    with open(path_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(baris_csv)
        
    print(f"✅ CSV state grid 4x4 berhasil dibuat di: {os.path.abspath(path_csv)}")
    return path_csv

if __name__ == "__main__":
    # State permainan 4x4 persis sesuai screenshot game yang dijalankan:
    # Hantu berada di B3, K1 (atau B2, K0)
    
    # Langkah 0: Awal (Base prior 1/16 = +0.06 di semua petak)
    s0 = [[0.06 for _ in range(4)] for _ in range(4)]
    
    # Langkah 1: Scan B0, K0 (Dingin)
    s1 = [
        [0.00, 0.10, 0.39, 0.39],
        [0.10, 0.10, 0.39, 0.39],
        [0.39, 0.39, 0.39, 0.39],
        [0.39, 0.39, 0.39, 0.39]
    ]
    
    # Langkah 2: Scan B0, K1 (Dingin)
    s2 = [
        [0.00, 0.00, 0.40, 0.40],
        [0.40, 0.40, 0.40, 0.40],
        [0.61, 0.61, 0.61, 0.61],
        [0.61, 0.61, 0.61, 0.61]
    ]
    
    # Langkah 3: Scan B1, K3 (Dingin)
    s3 = [
        [0.00, 0.00, 0.61, 0.61],
        [0.40, 0.40, 0.40, 0.00],
        [0.61, 0.61, 0.61, 0.61],
        [0.61, 0.61, 0.61, 0.61]
    ]
    
    # Langkah 4: Scan B2, K1 (Ada Bisikan 🔊)
    s4 = [
        [0.00, 0.00, 0.64, 0.64],
        [0.81, 0.81, 0.81, 0.00],
        [0.95, 0.00, 0.95, 0.87],
        [0.95, 0.95, 0.95, 0.95]
    ]
    
    # Langkah 5: Scan B3, K3 (Dingin) -> PERSIS SCREENSHOT ANDA
    s5 = [
        [0.00, 0.00, 0.87, 0.91],
        [0.81, 0.81, 0.81, 0.00],
        [0.98, 0.00, 0.95, 0.87],
        [0.98, 0.98, 0.96, 0.00]
    ]
    
    # Langkah 6: Tangkap B3, K1 (🎉 MENANG!)
    s6 = [
        [0.00, 0.00, 0.87, 0.91],
        [0.81, 0.81, 0.81, 0.00],
        [0.98, 0.00, 0.95, 0.87],
        [0.98, 1.00, 0.96, 0.00]
    ]
    
    riwayat_4x4 = [s0, s1, s2, s3, s4, s5, s6]
    
    # Simpan versi Kolom 1 = B0K0 s/d B3K3
    simpan_state_grid_per_langkah(riwayat_4x4, "dataset_state_grid_4x4_b0k0.csv", format_b1k1=False)
    
    # Simpan versi Kolom 1 = B1K1 s/d B4K4
    simpan_state_grid_per_langkah(riwayat_4x4, "dataset_state_grid_4x4_b1k1.csv", format_b1k1=True)
