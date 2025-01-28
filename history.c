
/*
def test_agent_memory():

    env = ChessEnvironment()
    
    # İki agent oluştur
    teacher = ChessAgent("Teacher", skill_level=15)
    student = ChessAgent("Student", skill_level=1)
    
    # Öğretmen agent'a bir hamle öğret
    position = env.get_board_state()
    best_move = env.get_best_move()
    teacher.store_memory(position, best_move, 0.5)
    
    # Hafızayı öğrenciye aktar
    teacher.transfer_memories_to(student)
    
    # Öğrenci aynı pozisyonda aynı hamleyi yapıyor mu kontrol et
    student_move = student.get_move_from_memory(position)
    print(f"Öğretmen hamlesi: {best_move}")
    print(f"Öğrenci hamlesi: {student_move}")
    print(f"Öğrenme başarılı: {best_move == student_move}")

def test_sequence_learning():
    print("\n=== Sequence Learning Test ===")
    env = ChessEnvironment()
    
    # Agentları oluştur
    teacher = ChessAgent("Teacher", skill_level=15)
    student = ChessAgent("Student", skill_level=1)
    
    # Oyun sekansı için listeleri hazırla
    positions = []
    moves = []
    evaluations = []
    
    # 5 hamlelik bir sekans oluştur
    for _ in range(5):
        position = env.get_board_state()
        best_move = env.get_best_move()
        evaluation = 0.5  # Basit bir değerlendirme skoru
        
        # Hamleyi kaydet
        positions.append(position)
        moves.append(best_move)
        evaluations.append(evaluation)
        
        # Hamleyi yap
        env.make_move(best_move)
    
    # Öğretmen sekansı öğrensin
    teacher.learn_from_game(positions, moves, evaluations)
    
    # Öğrenciye transfer et
    teacher.transfer_memories_to(student)
    
    # Sonuçları göster
    print(f"\nÖğretmen istatistikleri:")
    print(teacher.get_sequence_stats())
    
    print(f"\nÖğrenci istatistikleri:")
    print(student.get_sequence_stats())
    
    # Test et
    for pos, expected_move in zip(positions, moves):
        student_move = student.get_move_from_memory(pos)
        print(f"\nPozisyon: {pos[:50]}...")
        print(f"Beklenen hamle: {expected_move}")
        print(f"Öğrenci hamlesi: {student_move}")
        print(f"Doğru mu: {expected_move == student_move}")



    # Sonuçları göster
    print("\nÖğretmen istatistikleri:")
    print(teacher.get_stats())
    
    print("\nÖğrenci istatistikleri:")
    print(student.get_learning_stats())
    
    # Öğrenilen hamleleri test et
    print("\nHamle testleri:")
    for pos, expected_move in zip(positions, moves):
        student_move = student.get_move_from_memory(pos)
        print(f"Pozisyon için öğrenilen hamle doğru mu: {student_move == expected_move}")

        source venv/bin/activate
*/