# tests/test_memory_extraction.py

def test_memory_extraction():
    print("Stockfish hafızası çekiliyor...")
    
    extractor = StockfishMemoryExtractor()
    memory_data = extractor.extract_openings(max_positions=100)
    
    package = MemoryPackage()
    package.add_memories(memory_data)
    
    # Paketi kaydet
    package.save("stockfish_openings_v1")
    
    print("\nHafıza Paketi Oluşturuldu:")
    print(f"Toplam Pozisyon: {package.metadata['total_positions']}")
    print(f"Ortalama Güven: {package.metadata['average_confidence']:.2f}")
    
    # Örnek bir pozisyonu göster
    sample_position = list(memory_data.keys())[0]
    print("\nÖrnek Pozisyon:")
    print(f"FEN: {sample_position}")
    print(f"Hamle: {memory_data[sample_position]['move']}")
    print(f"Güven: {memory_data[sample_position]['confidence']:.2f}")

if __name__ == "__main__":
    test_memory_extraction()