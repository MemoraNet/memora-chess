import chess
import chess.polyglot
import os
import struct

def create_test_opening_book():
    """Test için popüler açılışları içeren küçük bir kitaplık oluştur"""
    print("Test açılış kitaplığı oluşturuluyor...")
    
    # books klasörünü oluştur
    if not os.path.exists('books'):
        os.makedirs('books')
    
    board = chess.Board()
    entries = []
    
    # 1. Ruy Lopez
    entries.append((board.fen(), "e2e4", 1000))  # e4
    board.push_uci("e2e4")
    entries.append((board.fen(), "e7e5", 1000))  # e5
    board.push_uci("e7e5")
    entries.append((board.fen(), "g1f3", 1000))  # Nf3
    board.push_uci("g1f3")
    entries.append((board.fen(), "b8c6", 1000))  # Nc6
    board.push_uci("b8c6")
    entries.append((board.fen(), "f1b5", 1000))  # Bb5
    
    # Tahtayı sıfırla
    board.reset()
    
    # 2. Italian Game
    entries.append((board.fen(), "e2e4", 900))  # e4
    board.push_uci("e2e4")
    entries.append((board.fen(), "e7e5", 900))  # e5
    board.push_uci("e7e5")
    entries.append((board.fen(), "g1f3", 900))  # Nf3
    board.push_uci("g1f3")
    entries.append((board.fen(), "b8c6", 900))  # Nc6
    board.push_uci("b8c6")
    entries.append((board.fen(), "f1c4", 900))  # Bc4
    
    # Kitaplığı kaydet
    book_path = 'books/test_openings.bin'
    save_to_binary(entries, book_path)
    
    print(f"Test kitaplığı oluşturuldu: {book_path}")
    print(f"Toplam pozisyon sayısı: {len(entries)}")
    return book_path

def move_to_int(move_uci):
    """UCI formatındaki hamleyi integer'a çevir"""
    from_square = chess.parse_square(move_uci[:2])
    to_square = chess.parse_square(move_uci[2:4])
    promotion = 0
    if len(move_uci) > 4:
        promotion = "pnbrqk".index(move_uci[4].lower()) + 1
    return from_square | (to_square << 6) | (promotion << 12)

def save_to_binary(entries, filepath):
    """Pozisyonları binary formatta kaydet"""
    with open(filepath, 'wb') as f:
        for fen, move_uci, weight in entries:
            board = chess.Board(fen)
            key = chess.polyglot.zobrist_hash(board)
            move_int = move_to_int(move_uci)
            entry_data = struct.pack('>QHHI', key, move_int, weight, 0)
            f.write(entry_data)

if __name__ == "__main__":
    create_test_opening_book()