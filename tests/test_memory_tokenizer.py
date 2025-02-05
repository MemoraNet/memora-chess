# tests/test_memory_tokenizer.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.memory_tokenizer import MemoryTokenizer
from src.chess_env import ChessEnvironment
from demo.demo_data import CHESS_OPENINGS

def test_basic_tokenization():
    """Temel tokenization işlevlerini test et"""
    print("\n=== Basic Tokenization Test ===")
    tokenizer = MemoryTokenizer()
    
    # Test pozisyonu
    test_position = {
        'position': "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        'move': "e7e5",
        'evaluation': 0.5,
        'opening': "Ruy Lopez"
    }
    
    # Tokenize et
    tokens = tokenizer._tokenize_position(test_position['position'])
    print(f"Position tokens: {tokens[:10]}...")
    
    move_tokens = tokenizer._tokenize_move(test_position['move'])
    print(f"Move tokens: {move_tokens}")
    
    sequence_token = tokenizer._tokenize_sequence(test_position['opening'])
    print(f"Sequence token: {sequence_token}")

def test_package_tokenization():
    """Tam paket tokenization sürecini test et"""
    print("\n=== Package Tokenization Test ===")
    tokenizer = MemoryTokenizer()
    
    # Test paketi oluştur
    test_package = {
        "metadata": {
            "source": "Test",
            "type": "basic_openings"
        },
        "memory_data": {}
    }
    
    # CHESS_OPENINGS'den test verisi al
    for opening_name, positions in CHESS_OPENINGS.items():
        for pos_data in positions[:2]:  # Her açılıştan 2 pozisyon
            key = f"{pos_data['position']}_{opening_name}"
            test_package["memory_data"][key] = {
                "position": pos_data['position'],
                "move": pos_data['move'],
                "evaluation": pos_data['evaluation'],
                "opening": opening_name
            }
    
    # Paketi tokenize et
    tokenized = tokenizer.tokenize_package(test_package)
    print(f"\nTokenized package contains {len(tokenized['tokenized_memories'])} positions")
    
    # Örnek bir tokenized pozisyonu göster
    sample_key = list(tokenized['tokenized_memories'].keys())[0]
    print("\nSample tokenized position:")
    print(json.dumps(tokenized['tokenized_memories'][sample_key], indent=2))

def test_detokenization():
    """Detokenization sürecini test et"""
    print("\n=== Detokenization Test ===")
    tokenizer = MemoryTokenizer()
    
    # Test verisi
    test_position = CHESS_OPENINGS["Ruy Lopez"][0]
    
    # Tokenize et
    tokenized = tokenizer.tokenize_package({
        "metadata": {"source": "Test"},
        "memory_data": {"test_pos": test_position}
    })
    
    # Detokenize et
    original = tokenizer.detokenize_package(tokenized)
    
    # Karşılaştır
    print("\nOriginal vs Detokenized:")
    print(f"Original move: {test_position['move']}")
    print(f"Detokenized move: {original['memory_data']['test_pos']['move']}")
    
    assert test_position['move'] == original['memory_data']['test_pos']['move'], \
        "Detokenization failed: moves don't match"
    print("Detokenization successful!")

def test_memory_efficiency():
    """Hafıza verimliliğini test et"""
    print("\n=== Memory Efficiency Test ===")
    tokenizer = MemoryTokenizer()
    
    # Büyük test paketi oluştur
    large_package = {
        "metadata": {"source": "Test"},
        "memory_data": {}
    }
    
    # 1000 pozisyon ekle
    for i in range(1000):
        pos_data = CHESS_OPENINGS["Ruy Lopez"][0]  # Örnek pozisyon
        large_package["memory_data"][f"pos_{i}"] = pos_data
    
    # Tokenization öncesi ve sonrası boyutu ölç
    import sys
    original_size = sys.getsizeof(str(large_package))
    
    tokenized = tokenizer.tokenize_package(large_package)
    tokenized_size = sys.getsizeof(str(tokenized))
    
    print(f"Original size: {original_size:,} bytes")
    print(f"Tokenized size: {tokenized_size:,} bytes")
    print(f"Compression ratio: {tokenized_size/original_size:.2%}")

def main():
    """Tüm testleri çalıştır"""
    try:
        test_basic_tokenization()
        test_package_tokenization()
        test_detokenization()
        test_memory_efficiency()
        
    except Exception as e:
        print(f"Test error: {e}")
        raise

if __name__ == "__main__":
    main()