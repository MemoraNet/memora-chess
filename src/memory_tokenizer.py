import chess
import numpy as np
from typing import Dict, List, Any
import json
import time

class MemoryTokenizer:
    def __init__(self):
        """Initialize the memory tokenizer with piece values and token types"""
        self.piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0
        }
        
        self.TOKEN_TYPES = {
            'POSITION': 1,
            'EVALUATION': 2,
            'MOVE': 3,
            'PV': 4,  # Principal Variation
            'ALTERNATIVE': 5
        }

    def tokenize_stockfish_memory(self, memory_package: Dict) -> Dict:
        """Tokenize a Stockfish memory package"""
        tokenized_package = {
            "metadata": memory_package["metadata"],
            "tokenized_memories": {}
        }

        for key, memory in memory_package["memories"].items():
            tokenized_package["tokenized_memories"][key] = {
                "position_tokens": self._tokenize_position(memory["position"]),
                "evaluation_token": self._tokenize_evaluation(memory["evaluation"]),
                "move_tokens": self._tokenize_move(memory["best_move"]),
                "pv_tokens": self._tokenize_principal_variation(
                    memory.get("principal_variation", [])
                ),
                "alternative_tokens": self._tokenize_alternatives(
                    memory.get("alternative_moves", [])
                ),
                "metadata": {
                    "original_position": memory["position"],
                    "depth": memory.get("depth", 0),
                    "timestamp": memory.get("timestamp", time.time())
                }
            }

        return tokenized_package

    def _tokenize_position(self, fen: str) -> List[float]:
        """Tokenize a chess position from FEN string"""
        board = chess.Board(fen)
        tokens = []
        
        # Piece-centric encoding for each piece type and color
        for piece_type in chess.PIECE_TYPES:
            for color in [chess.WHITE, chess.BLACK]:
                mask = board.pieces_mask(piece_type, color)
                for i in range(64):
                    tokens.append(float((mask >> i) & 1))
        
        # Additional position features
        tokens.extend([
            float(board.turn),
            float(board.has_kingside_castling_rights(chess.WHITE)),
            float(board.has_queenside_castling_rights(chess.WHITE)),
            float(board.has_kingside_castling_rights(chess.BLACK)),
            float(board.has_queenside_castling_rights(chess.BLACK)),
            float(board.is_check()),
            float(len(list(board.legal_moves)))  # Number of legal moves
        ])
        
        return tokens
    
    def _tokenize_evaluation(self, eval_score: float) -> List[float]:
        """Tokenize evaluation score"""
        # Normalize evaluation to [-1, 1] range using tanh
        normalized_eval = np.tanh(eval_score)
        
        # Create evaluation features
        return [
            normalized_eval,
            float(abs(eval_score) > 3),  # Significant advantage
            float(abs(eval_score) > 5),  # Winning position
            float(abs(eval_score) > 10)  # Near mate
        ]

    def _tokenize_move(self, move_uci: str) -> List[float]:
        """Tokenize a chess move in UCI format"""
        move = chess.Move.from_uci(move_uci)
        
        # Normalize square coordinates to [0, 1]
        from_square = move.from_square / 63.0
        to_square = move.to_square / 63.0
        
        # Special move type flags
        is_capture = float('x' in move_uci)
        is_promotion = float(move.promotion is not None)
        is_castle = float(move_uci in ['e1g1', 'e1c1', 'e8g8', 'e8c8'])
        
        return [from_square, to_square, is_capture, is_promotion, is_castle]

    def _tokenize_principal_variation(self, pv: List[str]) -> List[List[float]]:
        """Tokenize principal variation (sequence of best moves)"""
        return [self._tokenize_move(move) for move in pv]

    def _tokenize_alternatives(self, alternatives: List[Dict]) -> List[Dict]:
        """Tokenize alternative moves with their evaluations"""
        return [{
            "move": self._tokenize_move(alt["move"]),
            "evaluation": self._tokenize_evaluation(alt["evaluation"])
        } for alt in alternatives]

    def detokenize_package(self, tokenized_package: Dict) -> Dict:
        """Convert tokenized package back to original format"""
        original_package = {
            "metadata": tokenized_package["metadata"],
            "memories": {}
        }

        for key, tokens in tokenized_package["tokenized_memories"].items():
            original_package["memories"][key] = {
                "position": tokens["metadata"]["original_position"],
                "best_move": self._detokenize_move(tokens["move_tokens"]),
                "evaluation": self._detokenize_evaluation(tokens["evaluation_token"]),
                "depth": tokens["metadata"]["depth"],
                "timestamp": tokens["metadata"]["timestamp"]
            }

        return original_package

    def _detokenize_move(self, move_tokens: List[float]) -> str:
        """Convert move tokens back to UCI format"""
        from_square = int(round(move_tokens[0] * 63))
        to_square = int(round(move_tokens[1] * 63))
        return chess.Move(from_square, to_square).uci()

    def _detokenize_evaluation(self, eval_tokens: List[float]) -> float:
        """Convert evaluation tokens back to centipawn score"""
        return float(np.arctanh(eval_tokens[0]))

    def save_tokenized_package(self, package: Dict, filename: str):
        """Save tokenized package to file"""
        if not filename.endswith('.tokens'):
            filename += '.tokens'
        
        with open(filename, 'w') as f:
            json.dump(package, f, indent=2)

    def load_tokenized_package(self, filename: str) -> Dict:
        """Load tokenized package from file"""
        with open(filename, 'r') as f:
            return json.load(f)

def test_tokenizer():
    """Test tokenizer functionality"""
    tokenizer = MemoryTokenizer()
    
    # Test position
    test_position = chess.STARTING_FEN
    position_tokens = tokenizer._tokenize_position(test_position)
    print(f"Position tokens (first 10): {position_tokens[:10]}")
    
    # Test move
    test_move = "e2e4"
    move_tokens = tokenizer._tokenize_move(test_move)
    print(f"Move tokens: {move_tokens}")
    
    # Test evaluation
    test_eval = 0.5
    eval_tokens = tokenizer._tokenize_evaluation(test_eval)
    print(f"Evaluation tokens: {eval_tokens}")

if __name__ == "__main__":
    test_tokenizer()