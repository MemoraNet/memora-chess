import time
import json
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.position_memory = {}
        self.game_sequences = []
        self.move_history = []
        
    def get_move_from_memory(self, position):
        return self.position_memory.get(position)
    
    def get_stats(self):
        return {
            'name': self.name,
            'total_positions': len(self.position_memory),
            'total_sequences': len(self.game_sequences),
            'total_moves': len(self.move_history)
        }

class TeacherAgent(BaseAgent):
    def __init__(self, name, engine):
        super().__init__(name)
        self.engine = engine
        self.teaching_history = []
        
    def calculate_best_move(self, position):
        return self.engine.get_best_move()
    
    def record_move(self, position, move):
        self.position_memory[position] = move
        self.move_history.append({
            'position': position,
            'move': move,
            'timestamp': time.time()
        })
        
    def teach(self, student, position):
        move = self.calculate_best_move(position)
        self.record_move(position, move)
        student.learn(position, move)
        
        self.teaching_history.append({
            'student': student.name,
            'position': position,
            'move': move,
            'timestamp': time.time()
        })
        return move
    
    def get_teaching_stats(self):
        return {
            **self.get_stats(),
            'students_taught': len(set(h['student'] for h in self.teaching_history)),
            'total_lessons': len(self.teaching_history),
            'last_teaching': self.teaching_history[-1] if self.teaching_history else None
        }

class StudentAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.learned_moves = 0
        self.learning_history = []
        self.opening_knowledge = {}  # Açılış bilgisi için
        
    def learn(self, position, move):
        self.position_memory[position] = move
        self.learned_moves += 1
        
        learning_event = {
            'position': position,
            'move': move,
            'timestamp': time.time(),
            'move_number': self.learned_moves
        }
        self.learning_history.append(learning_event)
        self.move_history.append(learning_event)
        
    # 🟢 YENİ METOD
    def load_memory_package(self, package):
        """Hafıza paketini yükle"""
        if isinstance(package, dict):
            # Direkt dictionary olarak geldi
            memory_data = package['memory_data']
        else:
            # Dosyadan okuma
            try:
                with open(package, 'r') as f:
                    data = json.load(f)
                    memory_data = data['memory_data']
            except Exception as e:
                print(f"Hafıza paketi yüklenirken hata: {e}")
                return False
        
        # Hafızayı işle
        for key, data in memory_data.items():
            position = data['position']
            self.opening_knowledge[position] = {
                "move": data['move'],
                "sequence": data.get('opening', 'Unknown'),
                "weight": data.get('evaluation', 0.5)
            }
            # Position memory'ye de ekle
            self.position_memory[position] = data['move']
            self.learned_moves += 1
        
        print(f"Hafıza paketi yüklendi:")
        print(f"- Toplam pozisyon: {len(self.opening_knowledge)}")
        print(f"- Açılışlar: {set(data['sequence'] for data in self.opening_knowledge.values())}")
        return True
        
    def get_move(self, position):
        """Pozisyon için hamle seç"""
        # Önce opening_knowledge'a bak
        if position in self.opening_knowledge:
            return self.opening_knowledge[position]["move"]
        # Sonra position_memory'ye bak
        return self.position_memory.get(position)
        
    def get_learning_stats(self):
        return {
            **self.get_stats(),
            'total_learned_moves': self.learned_moves,
            'unique_positions': len(self.position_memory),
            'learning_progress': f"{self.learned_moves}/5 moves",
            'success_rate': f"{(self.learned_moves/5)*100}%",
            'last_learned': self.learning_history[-1] if self.learning_history else None
        }