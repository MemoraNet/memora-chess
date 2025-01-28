# src/chess_agents.py (yeni dosya adı)

import time
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Temel Agent sınıfı"""
    def __init__(self, name):
        self.name = name
        self.position_memory = {}
        self.game_sequences = []
        self.move_history = []  # Hamle geçmişi

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
    """Öğretmen Agent - Stockfish tabanlı"""
    def __init__(self, name, engine):
        super().__init__(name)
        self.engine = engine  # Stockfish engine
        self.teaching_history = []  # Öğretme geçmişi
        
    def calculate_best_move(self, position):
        """Stockfish kullanarak en iyi hamleyi hesapla"""
        return self.engine.get_best_move()
    
    def record_move(self, position, move):
        """Hamleyi kaydet"""
        self.position_memory[position] = move
        self.move_history.append({
            'position': position,
            'move': move,
            'timestamp': time.time()
        })

    def teach(self, student, position):
        """Öğrenciye hamle öğret"""
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
    """Öğrenci Agent"""
    def __init__(self, name):
        super().__init__(name)
        self.learned_moves = 0
        self.learning_history = []  # Öğrenme geçmişi
        
    def learn(self, position, move):
        """Öğretmenden hamle öğren"""
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

    def get_learning_stats(self):
        return {
            **self.get_stats(),
            'total_learned_moves': self.learned_moves,
            'unique_positions': len(self.position_memory),
            'learning_progress': f"{self.learned_moves}/5 moves",
            'success_rate': f"{(self.learned_moves/5)*100}%",
            'last_learned': self.learning_history[-1] if self.learning_history else None
        }