# tests/test_env.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.chess_env import ChessEnvironment
from src.chess_agents import TeacherAgent, StudentAgent
from src.visualizer import ChessVisualizer, LearningVisualizer

def test_basic_functionality():
    """Temel satranç ortamı fonksiyonlarını test et"""
    print("\nStockfish Test:")
    env = ChessEnvironment()
    
    # Başlangıç durumunu al
    initial_state = env.get_board_state()
    print(f"Başlangıç durumu: {initial_state}")
    
    # Yasal hamleleri al
    legal_moves = env.get_legal_moves()
    print(f"Yasal hamleler: {legal_moves}")
    
    # Stockfish'in önerdiği hamleyi al
    best_move = env.get_best_move()
    print(f"En iyi hamle: {best_move}")
    
    # Hamleyi yap
    if best_move:
        success = env.make_move(best_move)
        print(f"Hamle yapıldı: {success}")
        print(f"Yeni durum: {env.get_board_state()}")

def test_teaching_process():
    """Öğretme ve öğrenme sürecini test et"""
    print("\n=== Teaching Process Test ===")
    env = ChessEnvironment()
    
    # Görselleştiricileri oluştur
    chess_vis = ChessVisualizer()
    learning_vis = LearningVisualizer()
    
    teacher = TeacherAgent("Stockfish Teacher", env)
    student = StudentAgent("Beginner Student")
    
    positions = []
    moves = []
    descriptions = []
    
    for move_number in range(5):
        current_position = env.get_board_state()
        positions.append(current_position)
        
        print(f"\nHamle {move_number + 1}:")
        move = teacher.teach(student, current_position)
        moves.append(move)
        descriptions.append(f"Move {move_number + 1}: {move}")
        
        # Her hamleyi görselleştir
        chess_vis.save_position(current_position, move, f"move_{move_number+1}.svg")
        
        # Hamleyi yap
        env.make_move(move)
        
        # İstatistikleri göster
        print("\nÖğretmen Detaylı İstatistikler:")
        print(teacher.get_teaching_stats())
        
        print("\nÖğrenci Detaylı İstatistikler:")
        print(student.get_learning_stats())
        
        learning_vis.plot_learning_progress(student)
    
    # Oyun animasyonunu oluştur
    chess_vis.create_learning_animation(positions, moves, descriptions)
    
    print("\nGörselleştirmeler oluşturuldu:")
    print("- Satranç hamleleri: chess_visuals/")
    print("- Öğrenme grafikleri: learning_visuals/")
    print("- Animasyon: chess_visuals/game_animation.gif")
    
    # Final test
    print("\nFinal Hamle Testleri:")
    success_count = 0
    for pos, expected_move in zip(positions, moves):
        student_move = student.get_move_from_memory(pos)
        is_correct = student_move == expected_move
        success_count += 1 if is_correct else 0
        print(f"Pozisyon için öğrenilen hamle doğru mu: {is_correct}")
    
    print(f"\nToplam Başarı Oranı: {(success_count/len(positions))*100}%")

def test_memory_usage():
    """Hafıza kullanımını test et"""
    print("\n=== Hafıza Kullanım Testi ===")
    
    # Öğrenci agent oluştur
    student = StudentAgent("Memory Student")
    
    # Hafıza paketini yükle
    success = student.load_memory_package("test_memory_package.agentmem")
    if not success:
        print("Hafıza paketi yüklenemedi!")
        return
        
    # Test pozisyonları
    test_positions = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Başlangıç
        "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",  # e4 e5
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"  # ...Nc6
    ]
    
    print("\nTest Hamleleri:")
    for pos in test_positions:
        move = student.get_move(pos)
        print(f"Pozisyon: {pos[:30]}...")
        print(f"Seçilen hamle: {move}")
        print("---")

def main():
    """Tüm testleri çalıştır"""
    try:
        # Temel fonksiyonalite testi
        test_basic_functionality()
        
        # Öğretme/öğrenme süreci testi
        test_teaching_process()
        
        # Hafıza kullanım testi
        test_memory_usage()
        
    except Exception as e:
        print(f"Test sırasında hata oluştu: {e}")
        raise

if __name__ == "__main__":
    main()