# Flight Route Finder - Queue + BFS Implementation

## 📋 Deskripsi Proyek
Proyek ini merupakan implementasi **Queue** dan algoritma **Breadth-First Search (BFS)** menggunakan pendekatan **Object-Oriented Programming (OOP)** di Python. Program ini dirancang untuk menganalisis rute penerbangan dari dataset `routes.csv`, mencari jalur terpendek antara dua bandara, serta melakukan analisis jangkauan dan konektivitas jaringan penerbangan.

Proyek ini dibuat sebagai tugas mata kuliah **Struktur Data**.

---

## 👥 Anggota Kelompok 2

| No | Nama | NIM |
|----|------|-----|
| 1 | Favian Arkaanda | 124450021 |
| 2 | Riska Erlis Dayu Tiara | 124450022 |
| 3 | Farhanah Hadaya Fatin | 124450026 |
| 4 | M. Razan Maulana Pratama | 124450031 |
| 5 | Hani Qurrota Aini | 124450020 |
| 6 | Charrlindah | 124450037 |

---

## 🏗️ Struktur Kelas (OOP)

Program ini terdiri dari 3 kelas utama:

### 1. `DataLoader`
Kelas yang bertanggung jawab untuk:
- Membaca dan memuat data dari file `routes.csv`
- Membangun graph (adjacency list) dari data rute penerbangan
- Menyediakan metode untuk mendapatkan daftar bandara dan rute dari bandara tertentu

### 2. `Queue`
Implementasi struktur data Queue menggunakan `deque` dari modul `collections`:
- `enqueue(item)` - Menambahkan elemen ke akhir queue
- `dequeue()` - Menghapus dan mengembalikan elemen dari depan queue
- `is_empty()` - Mengecek apakah queue kosong
- `size()` - Mengembalikan jumlah elemen dalam queue
- `peek()` - Melihat elemen depan tanpa menghapus

### 3. `BFSShortestPath`
Kelas yang mengimplementasikan algoritma BFS untuk:
- `find_shortest_path(start, end)` - Mencari jalur terpendek antara dua bandara
- `find_all_paths_with_max_depth(start, end, max_depth)` - Mencari semua jalur dengan kedalaman maksimum tertentu
- `analyze_reachability_by_level(start, max_levels)` - Analisis jangkauan per level (berapa bandara yang bisa dicapai pada setiap level transit)
- `check_connectivity(airport1, airport2)` - Mengecek apakah dua bandara terhubung (langsung atau tidak langsung)

---

## 🚀 Fitur Utama

1. **Pencarian Rute Terpendek**: Menemukan jalur dengan jumlah transit paling sedikit antara dua bandara.
2. **Analisis Jangkauan per Level**: Menampilkan berapa banyak bandara yang dapat dicapai pada setiap level (0 hop, 1 hop, 2 hop, dst).
3. **Cek Konektivitas**: Memverifikasi apakah dua bandara terhubung dalam jaringan penerbangan dan menampilkan detail koneksinya.
4. **Visualisasi Output**: Tampilan hasil yang rapi dan mudah dibaca untuk keperluan presentasi dan screenshot.

---

## 📁 File dalam Repository

```
├── README.md               # Dokumentasi proyek (file ini)
├── routes.csv              # Dataset rute penerbangan
├── bfs_route_finder.py     # Kode utama implementasi OOP + Queue + BFS
└── screenshots/            # Folder untuk menyimpan hasil screenshot (jika ada)
```

---

## 🛠️ Cara Menjalankan Program

### Prasyarat
- Python 3.x terinstall di sistem Anda
- File `routes.csv` tersedia di direktori yang sama

### Langkah-langkah

1. Clone atau download repository ini ke komputer Anda.
2. Buka terminal/command prompt dan arahkan ke folder proyek:
   ```bash
   cd path/to/folder/proyek
   ```
3. Jalankan program:
   ```bash
   python bfs_route_finder.py
   ```
4. Program akan menampilkan 10 use case yang mencakup:
   - Pencarian rute terpendek (6 use case)
   - Analisis jangkauan per level (2 use case)
   - Cek konektivitas (2 use case)

---

## 📸 Use Case yang Tersedia

### A. Pencarian Rute Terpendek
1. **KZN → LED**: Rute domestik Rusia
2. **SIN → BKK**: Rute Asia Tenggara
3. **MNL → KIX**: Rute Internasional Asia
4. **CEK → NBC**: Rute dengan 1 transit via KZN
5. **ACH → MUC**: Rute Eropa via ZRH
6. **FLL → PNS**: Rute domestik AS via DFW

### B. Analisis Jangkauan per Level
7. **KZN**: Berapa bandara yang bisa dicapai pada level 0, 1, 2, 3?
8. **SIN**: Analisis jangkauan dari Bandara Changi Singapore

### C. Cek Konektivitas
9. **KZN ↔ LED**: Apakah terhubung? Langsung atau tidak?
10. **SIN ↔ MNL**: Cek konektivitas dan detail jalur

---

## 🧠 Konsep Struktur Data yang Digunakan

1. **Queue (Antrian)**: Digunakan sebagai struktur dasar untuk traversal BFS, memastikan node diproses secara FIFO (First In First Out).
2. **Graph (Adjacency List)**: Merepresentasikan jaringan penerbangan dimana bandara adalah node dan rute adalah edge.
3. **Breadth-First Search (BFS)**: Algoritma traversal graph yang menjamin pencarian jalur terpendek dalam graph tidak berbobot (unweighted).
4. **Hash Map / Dictionary**: Digunakan untuk menyimpan graph, visited nodes, dan tracking path.

---

## 📊 Contoh Output

```
--------------------------------------------------
Use Case 1: KZN → LED (Domestic Russia Route)
--------------------------------------------------
Shortest path: KZN -> LED

--------------------------------------------------
Use Case 7: Analisis Jangkauan per Level - KZN
--------------------------------------------------
Level 0 (Direct): 1 airports
Level 1 (1 hop): 15 airports
Level 2 (2 hops): 45 airports
Level 3 (3 hops): 120 airports
...

--------------------------------------------------
Use Case 9: Cek Konektivitas - KZN ↔ LED
--------------------------------------------------
Status: CONNECTED ✓
Connection Type: Direct Flight
Path: KZN -> LED
```

---

## 📝 Catatan

- Program ini mengasumsikan bahwa semua rute memiliki bobot yang sama (unweighted graph).
- Jika tidak ada jalur yang ditemukan antara dua bandara, program akan menampilkan "NO PATH FOUND".
- Dataset `routes.csv` harus berada di direktori yang sama dengan file `bfs_route_finder.py`.

---

## 🎯 Tujuan Pembelajaran

Melalui proyek ini, mahasiswa diharapkan dapat:
1. Memahami implementasi Queue dalam Python
2. Mengaplikasikan algoritma BFS untuk menyelesaikan masalah nyata
3. Menerapkan prinsip OOP dalam struktur kode
4. Menganalisis kompleksitas waktu dan ruang dari algoritma BFS
5. Bekerja sama dalam tim untuk menyelesaikan tugas struktur data

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis mata kuliah Struktur Data - Kelompok 2.

---

**Dibuat dengan ❤️ oleh Kelompok 2 Struktur Data**