import chess
import chess.polyglot
import json
import time
import os
import struct

class StockfishMemoryExtractor:
    def __init__(self, opening_book_path="books/test_openings.bin"):
        self.board = chess.Board()
        self.book_path = opening_book_path
        print(f"Açılış kitaplığı yolu: {opening_book_path}")
        
    def extract_openings(self, max_positions=1000):
        """Açılış kitaplığından pozisyonları çek"""
        print("Hafıza çıkarma işlemi başlıyor...")
        memory_data = {}
        
        # Tüm sekansları bir listede toplayalım
        all_sequences = [
            {
                "name": "Ruy Lopez",
                "moves": [
                    ("e2e4", 1000),
                    ("e7e5", 1000),
                    ("g1f3", 1000),
                    ("b8c6", 1000),
                    ("f1b5", 1000)
                ]
            },
            {
                "name": "Italian Game",
                "moves": [
                    ("e2e4", 900),
                    ("e7e5", 900),
                    ("g1f3", 900),
                    ("b8c6", 900),
                    ("f1c4", 900)
                ]
            }
        ]
        
        # Her sekansı işle
        for sequence in all_sequences:
            self.board.reset()
            sequence_name = sequence["name"]
            print(f"\nİşleniyor: {sequence_name}")
            current_sequence = []

            for move_uci, weight in sequence["moves"]:
                position_fen = self.board.fen()
                move_key = f"{position_fen}_{sequence_name}"  # Benzersiz anahtar

                memory_data[position_fen] = {
                    "move": move_uci,
                    "weight": weight,
                    "sequence": sequence_name,
                    "position": position_fen,
                    "timestamp": time.time()
                }
                print(f"Pozisyon eklendi: {move_uci} ({sequence_name})")
                
                try:
                    self.board.push_uci(move_uci)
                    current_sequence.append(move_uci)
                except Exception as e:
                    print(f"Hata: {move_uci} hamlesi yapılamadı - {e}")
                    break
        
        print(f"\nToplam {len(memory_data)} pozisyon çıkarıldı")
        return memory_data

class MemoryPackage:
    def __init__(self, source_name="Stockfish", memory_type="chess_openings"):
        self.metadata = {
            "source": source_name,
            "type": memory_type,
            "created_at": time.time(),
            "ram_required": "50MB",
            "version": "1.0",
            "total_positions": 0,
            "average_weight": 0.0,
            "sequences": {
                "Ruy Lopez": 0,
                "Italian Game": 0
            }
        }
        self.memory_data = {}
        
    def add_memories(self, memory_data):
        """Hafıza paketine yeni veriler ekle"""
        self.memory_data.update(memory_data)
        self._update_metadata()
        
    def save(self, filename):
        """Paketi .agentmem dosyası olarak kaydet"""
        if not filename.endswith('.agentmem'):
            filename += '.agentmem'
            
        package = {
            "metadata": self.metadata,
            "memory_data": self.memory_data
        }
        
        try:
            with open(filename, "w") as f:
                json.dump(package, f, indent=2)
            print(f"Hafıza paketi kaydedildi: {filename}")
        except Exception as e:
            print(f"Kayıt sırasında hata: {e}")
            raise
            
    def _update_metadata(self):
        """Metadata bilgilerini güncelle"""
        self.metadata["total_positions"] = len(self.memory_data)
    
        # Ağırlık ortalamasını hesapla
        weights = [m["weight"] for m in self.memory_data.values()]
        self.metadata["average_weight"] = sum(weights) / len(weights) if weights else 0
    
        # Sekans sayılarını güncelle
        self.metadata["sequences"] = {
            "Ruy Lopez": sum(1 for m in self.memory_data.values() if m["sequence"] == "Ruy Lopez"),
            "Italian Game": sum(1 for m in self.memory_data.values() if m["sequence"] == "Italian Game")
    }
        
    def get_stats(self):
        """Detaylı istatistikler"""
        return {
            "total_positions": self.metadata["total_positions"],
            "average_weight": self.metadata["average_weight"],
            "sequences": self.metadata["sequences"],
            "memory_size": len(json.dumps(self.memory_data)),
            "creation_date": time.ctime(self.metadata["created_at"])
        }

def test_extraction():
    """Hafıza çıkarma işlemini test et"""
    print("\n=== Hafıza Çıkarma Testi ===")
    
    # Extractor oluştur
    extractor = StockfishMemoryExtractor()
    
    # Verileri çek
    memory_data = extractor.extract_openings()
    
    # Memory package oluştur
    package = MemoryPackage(source_name="TestBook", memory_type="basic_openings")
    package.add_memories(memory_data)
    
    # Paketi kaydet
    package.save("test_memory_package")
    
    # Detaylı istatistikleri göster
    print("\n=== Hafıza Paketi İstatistikleri ===")
    stats = package.get_stats()
    print(f"Toplam Pozisyon: {stats['total_positions']}")
    print(f"Ortalama Ağırlık: {stats['average_weight']:.2f}")
    print("\nSekans Dağılımı:")
    for name, count in stats['sequences'].items():
        print(f"- {name}: {count} pozisyon")
    
    print("\n=== Kaydedilen Pozisyonlar ===")
    for pos, data in memory_data.items():
        print(f"\n{data['sequence']} - {data['move']}:")
        print(f"FEN: {pos}")
        print(f"Ağırlık: {data['weight']}")

if __name__ == "__main__":
    test_extraction()