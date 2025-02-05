import time
import json
from abc import ABC, abstractmethod
import chess
import numpy as np
from typing import Dict, List, Optional, Tuple

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.position_memory = {}
        self.game_sequences = []
        self.move_history = []
        
    def get_move_from_memory(self, position: str) -> Optional[str]:
        """Get a move from memory for a given position"""
        return self.position_memory.get(position)
    
    def get_stats(self) -> Dict:
        """Get basic agent statistics"""
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
        
    def calculate_best_move(self, position: str) -> Optional[str]:
        """Calculate best move using the engine"""
        try:
            board = chess.Board(position)
            result = self.engine.play(board, chess.engine.Limit(depth=20))
            return result.move.uci() if result.move else None
        except Exception as e:
            print(f"Error calculating best move: {e}")
            return None
        
    def record_move(self, position: str, move: str):
        """Record a move in memory"""
        self.position_memory[position] = move
        self.move_history.append({
            'position': position,
            'move': move,
            'timestamp': time.time()
        })

    def teach(self, student, position: str) -> Optional[str]:
        """Teach a move to a student"""
        move = self.calculate_best_move(position)
        if move:
            self.record_move(position, move)
            student.learn(position, move)
            
            self.teaching_history.append({
                'student': student.name,
                'position': position,
                'move': move,
                'timestamp': time.time()
            })
            
        return move
    
    def get_teaching_stats(self) -> Dict:
        """Get detailed teaching statistics"""
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
        self.position_evaluations = {}
        self.confidence_scores = {}
        self.pattern_memory = {}
        self.position_history = {}
        self.draw_threshold = 3
        self.current_opening = "Unknown"
        self.opening_knowledge = {
            "Ruy Lopez": [
                ("e2e4", "e7e5"),
                ("g1f3", "b8c6"),
                ("f1b5", None)
            ],
            "Sicilian Defense": [
                ("e2e4", "c7c5"),
                ("g1f3", "d7d6"),
                ("d2d4", None)
            ],
            "French Defense": [
                ("e2e4", "e7e6"),
                ("d2d4", "d7d5"),
                ("e4e5", None)
            ]
        }

    def reset_game(self):
        """Reset game state"""
        self.move_history = []
        self.position_history = {}
        self.current_opening = "Unknown"

    def learn_from_tokenized_memory(self, tokenized_package: Dict):
        """Learn from tokenized memory package"""
        print(f"\n{self.name} starting to learn...")
        start_time = time.time()
        
        success_count = 0
        for key, tokens in tokenized_package["tokenized_memories"].items():
            try:
                position = tokens["metadata"]["original_position"]
                move_tokens = tokens["move_tokens"]
                move = self._decode_move(move_tokens)
                
                self.position_memory[position] = move
                self.position_evaluations[position] = self._decode_evaluation(tokens["evaluation_token"])
                self._learn_position_pattern(tokens["position_tokens"], move_tokens, tokens["evaluation_token"])
                self.confidence_scores[position] = self._calculate_confidence(position, move)
                
                self.learning_history.append({
                    'position': position,
                    'move': move,
                    'confidence': self.confidence_scores[position],
                    'timestamp': time.time()
                })
                
                success_count += 1
                self.learned_moves += 1
                
            except Exception as e:
                print(f"Error learning position {key}: {e}")
                continue
        
        end_time = time.time()
        print(f"\nLearning completed!")
        print(f"Successfully learned positions: {success_count}/{len(tokenized_package['tokenized_memories'])}")
        print(f"Learning duration: {end_time - start_time:.2f} seconds")
        
        return end_time - start_time

    def get_move(self, position: str) -> Optional[str]:
        """Get best move for the position"""
        if self.is_draw_by_repetition(position):
            return None
            
        board = chess.Board(position)
        
        if position == chess.STARTING_FEN:
            self.reset_game()
        
        # 1. Check opening book
        opening_move = self._get_opening_move(position)
        if opening_move:
            self.make_move(position, opening_move)
            return opening_move
            
        # 2. Check learned memory
        memory_move = self._get_memory_move(position)
        if memory_move:
            self.make_move(position, memory_move)
            return memory_move
            
        # 3. Calculate best move
        best_move = self._calculate_best_move(board)
        if best_move:
            move_str = best_move.uci()
            self.make_move(position, move_str)
            return move_str
        
        # 4. Fallback to first legal move
        legal_moves = list(board.legal_moves)
        if legal_moves:
            move_str = legal_moves[0].uci()
            self.make_move(position, move_str)
            return move_str
        
        return None

    def make_move(self, position: str, move: str):
        """Record a move being made"""
        if move:
            self.move_history.append(move)

    def is_draw_by_repetition(self, position: str) -> bool:
        """Check for draw by repetition"""
        if position in self.position_history:
            self.position_history[position] += 1
            if self.position_history[position] >= self.draw_threshold:
                print("Draw by repetition detected!")
                return True
        else:
            self.position_history[position] = 1
        return False

    def _get_opening_move(self, position: str) -> Optional[str]:
        """Get move from opening knowledge"""
        board = chess.Board(position)
        move_count = len(board.move_stack)
        
        for opening_name, moves in self.opening_knowledge.items():
            if move_count < len(moves):
                expected_move = moves[move_count][board.turn]
                if expected_move:
                    try:
                        move = chess.Move.from_uci(expected_move)
                        if move in board.legal_moves:
                            self.current_opening = opening_name
                            return expected_move
                    except:
                        continue
        return None

    def _get_memory_move(self, position: str) -> Optional[str]:
        """Get move from learned memory"""
        if position in self.position_memory:
            move = self.position_memory[position]
            try:
                board = chess.Board(position)
                chess_move = chess.Move.from_uci(move)
                if chess_move in board.legal_moves:
                    return move
            except:
                pass
        return None

    def _calculate_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Calculate best move using position evaluation"""
        best_move = None
        best_score = float('-inf')
        
        for move in board.legal_moves:
            board.push(move)
            score = -self._evaluate_position(board)
            board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def _evaluate_position(self, board: chess.Board) -> float:
        """Evaluate chess position"""
        if board.is_checkmate():
            return float('inf') if board.turn else float('-inf')
            
        score = 0
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Material evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == board.turn:
                    score += value
                else:
                    score -= value
                    
        # Center control bonus
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        for square in center_squares:
            if board.piece_at(square):
                if board.piece_at(square).color == board.turn:
                    score += 30
                else:
                    score -= 30
        
        return score

    def _calculate_confidence(self, position: str, move: str) -> float:
        """Calculate confidence score"""
        board = chess.Board(position)
        
        # Pattern match score
        pattern_confidence = self._get_pattern_confidence(position)
        
        # Legal move bonus
        try:
            chess_move = chess.Move.from_uci(move)
            legal_bonus = 30.0 if chess_move in board.legal_moves else 0.0
        except:
            legal_bonus = 0.0
        
        return min(pattern_confidence + legal_bonus, 100.0)

    def _get_pattern_confidence(self, position: str) -> float:
        """Calculate confidence based on pattern recognition"""
        board = chess.Board(position)
        pattern = self._create_position_vector(board)
        pattern_key = tuple(pattern)
        
        if pattern_key in self.pattern_memory:
            pattern_data = self.pattern_memory[pattern_key]
            return min(pattern_data['count'] / 3, 1.0) * 40  # Max 40 points from pattern recognition
        return 0.0

    def _create_position_vector(self, board: chess.Board) -> List[float]:
        """Create a numerical vector representing the position"""
        vector = []
        
        # Piece placement features
        for piece_type in chess.PIECE_TYPES:
            for color in [chess.WHITE, chess.BLACK]:
                mask = board.pieces_mask(piece_type, color)
                for i in range(64):
                    vector.append(float((mask >> i) & 1))
        
        # Additional features
        vector.extend([
            float(board.turn),
            float(board.has_kingside_castling_rights(chess.WHITE)),
            float(board.has_queenside_castling_rights(chess.WHITE)),
            float(board.has_kingside_castling_rights(chess.BLACK)),
            float(board.has_queenside_castling_rights(chess.BLACK))
        ])
        
        return vector

    def _decode_move(self, move_tokens: List[float]) -> str:
        """Decode move tokens to UCI format"""
        from_square = int(round(move_tokens[0] * 63))
        to_square = int(round(move_tokens[1] * 63))
        return chess.Move(from_square, to_square).uci()

    def _decode_evaluation(self, eval_tokens: List[float]) -> float:
        """Decode evaluation tokens to score"""
        return float(np.arctanh(eval_tokens[0]))

    def _learn_position_pattern(self, position_tokens: List[float], 
                              move_tokens: List[float],
                              eval_tokens: List[float]):
        """Learn a position pattern"""
        pattern_key = tuple(position_tokens)
        
        if pattern_key not in self.pattern_memory:
            self.pattern_memory[pattern_key] = {
                'moves': [],
                'evaluations': [],
                'count': 0
            }
        
        self.pattern_memory[pattern_key]['moves'].append(move_tokens)
        self.pattern_memory[pattern_key]['evaluations'].append(eval_tokens)
        self.pattern_memory[pattern_key]['count'] += 1

    def get_learning_stats(self) -> Dict:
        """Get detailed learning statistics"""
        confidence_values = [
            score for score in self.confidence_scores.values()
            if score is not None
        ]
        
        avg_confidence = (
            sum(confidence_values) / len(confidence_values)
            if confidence_values else 0.0
        )
        
        return {
            'total_learned_moves': self.learned_moves,
            'unique_positions': len(self.position_memory),
            'unique_patterns': len(self.pattern_memory),
            'average_confidence': f"{avg_confidence:.2f}",
            'positions_with_confidence': len(confidence_values),
            'learning_progress': f"{self.learned_moves} moves learned",
            'last_learned': self.learning_history[-1] if self.learning_history else None
        }