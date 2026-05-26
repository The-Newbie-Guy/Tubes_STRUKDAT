"""
BFS Route Finder - Mencari rute terpendek menggunakan algoritma Breadth-First Search (BFS)
dengan implementasi Queue pada data rute penerbangan.

Dataset: routes.csv
Author: Assistant
"""

import csv
from collections import deque
from typing import Dict, List, Optional, Tuple, Set


class DataLoader:
    """Kelas untuk memuat dan memproses data dari file CSV."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.routes: List[Dict] = []
        self.graph: Dict[str, Set[str]] = {}  # Adjacency list: source -> set of destinations
        self.airports: Set[str] = set()
        
    def load_data(self) -> None:
        """Memuat data dari file CSV."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            # Read content and handle Windows line endings
            content = file.read().replace('\r\n', '\n').replace('\r', '\n')
            lines = content.split('\n')
            
            # Parse header
            header = lines[0].split(',')
            reader = csv.DictReader(lines)
            
            for row in reader:
                source = row.get(' source airport', '').strip()
                destination = row.get(' destination apirport', '').strip()
                
                # Skip invalid entries
                if not source or not destination or source == '\\N' or destination == '\\N':
                    continue
                
                # Handle equipment field - it's the last column
                equipment = row.get(' equipment', row.get('equipment', ''))
                    
                self.routes.append({
                    'airline': row.get('airline', ''),
                    'airline_id': row.get('airline ID', ''),
                    'source': source,
                    'source_id': row.get(' source airport id', ''),
                    'destination': destination,
                    'destination_id': row.get(' destination airport id', ''),
                    'stops': row.get(' stops', '0'),
                    'equipment': equipment.strip() if equipment else ''
                })
                
                # Add to airports set
                self.airports.add(source)
                self.airports.add(destination)
        
        print(f"✓ Berhasil memuat {len(self.routes)} rute dari {len(self.airports)} bandara")
    
    def build_graph(self) -> None:
        """Membangun graph adjacency list dari data rute."""
        self.graph = {airport: set() for airport in self.airports}
        
        for route in self.routes:
            source = route['source']
            destination = route['destination']
            if source in self.graph and destination in self.graph:
                self.graph[source].add(destination)
        
        print(f"✓ Graph berhasil dibangun dengan {len(self.graph)} node")
    
    def get_airport_list(self) -> List[str]:
        """Mengembalikan daftar semua bandara yang tersedia."""
        return sorted(list(self.airports))
    
    def get_routes_from_airport(self, airport: str) -> List[Dict]:
        """Mengembalikan semua rute dari sebuah bandara."""
        return [r for r in self.routes if r['source'] == airport]


class Queue:
    """Implementasi Queue sederhana untuk BFS."""
    
    def __init__(self):
        self._queue: deque = deque()
    
    def enqueue(self, item) -> None:
        """Menambahkan item ke akhir queue."""
        self._queue.append(item)
    
    def dequeue(self):
        """Mengambil dan menghapus item dari depan queue."""
        if self.is_empty():
            return None
        return self._queue.popleft()
    
    def is_empty(self) -> bool:
        """Memeriksa apakah queue kosong."""
        return len(self._queue) == 0
    
    def size(self) -> int:
        """Mengembalikan ukuran queue."""
        return len(self._queue)
    
    def peek(self):
        """Melihat item di depan queue tanpa menghapusnya."""
        if self.is_empty():
            return None
        return self._queue[0]


class BFSShortestPath:
    """Kelas untuk mencari rute terpendek menggunakan algoritma BFS."""
    
    def __init__(self, graph: Dict[str, Set[str]], data_loader: DataLoader):
        self.graph = graph
        self.data_loader = data_loader
        self.queue = Queue()
    
    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Mencari rute terpendek dari start ke end menggunakan BFS.
        
        Args:
            start: Bandara asal
            end: Bandara tujuan
            
        Returns:
            List bandara dalam rute terpendek, atau None jika tidak ada rute
        """
        if start not in self.graph or end not in self.graph:
            return None
        
        if start == end:
            return [start]
        
        # Initialize BFS
        self.queue = Queue()
        visited: Set[str] = set()
        parent: Dict[str, Optional[str]] = {start: None}
        
        # Enqueue starting node
        self.queue.enqueue(start)
        visited.add(start)
        
        # BFS traversal
        while not self.queue.is_empty():
            current = self.queue.dequeue()
            
            # Check all neighbors
            for neighbor in self.graph.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    self.queue.enqueue(neighbor)
                    
                    # Early termination if we found the destination
                    if neighbor == end:
                        return self._reconstruct_path(parent, start, end)
        
        # No path found
        return None
    
    def _reconstruct_path(self, parent: Dict[str, Optional[str]], 
                          start: str, end: str) -> List[str]:
        """Merekonstruksi jalur dari informasi parent."""
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = parent[current]
        
        path.reverse()
        return path
    
    def find_all_paths_with_max_depth(self, start: str, end: str, 
                                       max_depth: int = 5) -> List[List[str]]:
        """
        Mencari semua jalur dari start ke end dengan kedalaman maksimum.
        
        Args:
            start: Bandara asal
            end: Bandara tujuan
            max_depth: Kedalaman maksimum pencarian
            
        Returns:
            List dari semua jalur yang ditemukan
        """
        if start not in self.graph or end not in self.graph:
            return []
        
        all_paths = []
        self._dfs_find_paths(start, end, [start], set([start]), all_paths, max_depth)
        
        # Sort by length
        all_paths.sort(key=len)
        return all_paths
    
    def _dfs_find_paths(self, current: str, end: str, path: List[str], 
                        visited: Set[str], all_paths: List[List[str]], 
                        max_depth: int) -> None:
        """DFS helper untuk menemukan semua jalur."""
        if len(path) > max_depth:
            return
        
        if current == end:
            all_paths.append(path.copy())
            return
        
        for neighbor in self.graph.get(current, set()):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                self._dfs_find_paths(neighbor, end, path, visited, all_paths, max_depth)
                path.pop()
                visited.remove(neighbor)
    
    def get_flight_details(self, path: List[str]) -> List[Dict]:
        """
        Mendapatkan detail penerbangan untuk setiap segmen dalam jalur.
        
        Args:
            path: List bandara dalam jalur
            
        Returns:
            List detail penerbangan untuk setiap segmen
        """
        details = []
        
        for i in range(len(path) - 1):
            source = path[i]
            destination = path[i + 1]
            
            # Find matching route
            for route in self.data_loader.routes:
                if route['source'] == source and route['destination'] == destination:
                    details.append(route)
                    break
        
        return details


def print_path_details(path: List[str], flight_details: List[Dict], 
                       use_case_title: str) -> None:
    """Mencetak detail jalur dengan format yang rapi untuk screenshot."""
    print("\n" + "=" * 80)
    print(f"  {use_case_title}")
    print("=" * 80)
    
    if not path:
        print("❌ Tidak ada rute yang ditemukan!")
        return
    
    print(f"\n🛫 RUTE TERPENDEK DITEMUKAN!")
    print(f"\n📍 Total Bandara: {len(path)}")
    print(f"✈️  Total Transit: {len(path) - 2} (tidak termasuk asal dan tujuan)")
    
    print("\n🗺️  DETAIL PERJALANAN:")
    print("-" * 80)
    
    for i, airport in enumerate(path):
        if i == 0:
            print(f"  [{i+1}] 🟢 START: {airport}")
        elif i == len(path) - 1:
            print(f"  [{i+1}] 🔴 END:   {airport}")
        else:
            print(f"  [{i+1}] 🟡 TRANSIT: {airport}")
    
    print("\n✈️  DETAIL PENERBANGAN:")
    print("-" * 80)
    
    for i, detail in enumerate(flight_details):
        print(f"\n  Segmen {i+1}: {detail['source']} → {detail['destination']}")
        print(f"    • Maskapai: {detail['airline']} (ID: {detail['airline_id']})")
        print(f"    • Stops: {detail['stops']}")
        print(f"    • Equipment: {detail['equipment']}")
    
    print("\n" + "=" * 80)


def main():
    """Fungsi utama untuk menjalankan program."""
    print("\n" + "█" * 80)
    print("  BFS ROUTE FINDER - Pencarian Rute Terpendek dengan Queue + BFS")
    print("█" * 80)
    
    # Initialize DataLoader
    print("\n📂 MEMUAT DATA...")
    loader = DataLoader('routes.csv')
    loader.load_data()
    loader.build_graph()
    
    # Initialize BFS
    print("\n🔍 MENYIAPKAN ALGORITMA BFS...")
    bfs = BFSShortestPath(loader.graph, loader)
    
    # ============================================
    # USE CASE 1: Rute dari KZN ke LED
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 1: Mencari rute dari KZN (Kazan) ke LED (St. Petersburg)")
    print("░" * 80)
    
    start1, end1 = "KZN", "LED"
    path1 = bfs.find_shortest_path(start1, end1)
    
    if path1:
        details1 = bfs.get_flight_details(path1)
        print_path_details(path1, details1, "USE CASE 1: KZN → LED (Rute Domestik Rusia)")
    else:
        print(f"❌ Tidak ada rute dari {start1} ke {end1}")
    
    # ============================================
    # USE CASE 2: Rute dari SIN ke BKK
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 2: Mencari rute dari SIN (Singapore) ke BKK (Bangkok)")
    print("░" * 80)
    
    start2, end2 = "SIN", "BKK"
    path2 = bfs.find_shortest_path(start2, end2)
    
    if path2:
        details2 = bfs.get_flight_details(path2)
        print_path_details(path2, details2, "USE CASE 2: SIN → BKK (Rute Asia Tenggara)")
    else:
        print(f"❌ Tidak ada rute dari {start2} ke {end2}")
    
    # ============================================
    # USE CASE 3: Rute dari MNL ke KIX
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 3: Mencari rute dari MNL (Manila) ke KIX (Osaka Kansai)")
    print("░" * 80)
    
    start3, end3 = "MNL", "KIX"
    path3 = bfs.find_shortest_path(start3, end3)
    
    if path3:
        details3 = bfs.get_flight_details(path3)
        print_path_details(path3, details3, "USE CASE 3: MNL → KIX (Rute Internasional Asia)")
    else:
        print(f"❌ Tidak ada rute dari {start3} ke {end3}")
    
    # ============================================
    # USE CASE 4: Rute dengan transit (contoh rute yang membutuhkan lebih dari 1 hop)
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 4: CEK (Chelyabinsk) → NBC (Nizhnekamsk) - Dengan Transit")
    print("░" * 80)
    
    start4, end4 = "CEK", "NBC"
    path4 = bfs.find_shortest_path(start4, end4)
    
    if path4:
        details4 = bfs.get_flight_details(path4)
        print_path_details(path4, details4, "USE CASE 4: CEK → NBC (Rute dengan 1 Transit di KZN)")
    else:
        print(f"❌ Tidak ada rute dari {start4} ke {end4}")
    
    # ============================================
    # USE CASE 5: Rute Eropa dengan transit
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 5: ACH (Altenrhein) → MUC (Munich) - Dengan Transit")
    print("░" * 80)
    
    start5, end5 = "ACH", "MUC"
    path5 = bfs.find_shortest_path(start5, end5)
    
    if path5:
        details5 = bfs.get_flight_details(path5)
        print_path_details(path5, details5, "USE CASE 5: ACH → MUC (Rute Eropa dengan 1 Transit di ZRH)")
    else:
        print(f"❌ Tidak ada rute dari {start5} ke {end5}")
    
    # ============================================
    # USE CASE 6: Rute Amerika dengan transit
    # ============================================
    print("\n\n" + "░" * 80)
    print("  USE CASE 6: FLL (Fort Lauderdale) → PNS (Pensacola) - Dengan Transit")
    print("░" * 80)
    
    start6, end6 = "FLL", "PNS"
    path6 = bfs.find_shortest_path(start6, end6)
    
    if path6:
        details6 = bfs.get_flight_details(path6)
        print_path_details(path6, details6, "USE CASE 6: FLL → PNS (Rute Domestik AS dengan 1 Transit di MCO)")
    else:
        print(f"❌ Tidak ada rute dari {start6} ke {end6}")
    
    # ============================================
    # Additional Info: Show some available airports
    # ============================================
    print("\n\n" + "░" * 80)
    print("  INFORMASI TAMBAHAN: Daftar Bandara Tersedia (Sample)")
    print("░" * 80)
    
    airports = loader.get_airport_list()
    print(f"\nTotal bandara dalam dataset: {len(airports)}")
    print("\nSample bandara:")
    for i, airport in enumerate(airports[:30]):
        print(f"  • {airport}", end="")
        if (i + 1) % 5 == 0:
            print()
    
    print("\n\n" + "█" * 80)
    print("  PROGRAM SELESAI - Silakan screenshot output di atas")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
