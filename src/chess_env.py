# src/chess_env.py

import chess
import chess.engine
import os

class ChessEnvironment:
    def __init__(self, stockfish_path=None):
        """
        Satranç ortamını başlat
        stockfish_path: Stockfish engine'in yolu
        """
        self.board = chess.Board()
        
        # Stockfish yolunu belirle
        if stockfish_path is None:
            # Mac için varsayılan Homebrew kurulum yolu
            stockfish_path = "/opt/homebrew/bin/stockfish"
        
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print("Stockfish engine başarıyla başlatıldı!")
        except Exception as e:
            print(f"Stockfish engine başlatılamadı: {e}")
            raise

    def get_board_state(self):
        """Mevcut tahta durumunu FEN formatında döndür"""
        return self.board.fen()

    def make_move(self, move_uci):
        """UCI formatında verilen hamleyi yap"""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        except:
            return False

    def get_legal_moves(self):
        """Tüm yasal hamleleri listele"""
        return [move.uci() for move in self.board.legal_moves]

    def get_best_move(self, time_limit=1.0):
        """Stockfish'in önerdiği en iyi hamleyi al"""
        result = self.engine.play(self.board, chess.engine.Limit(time=time_limit))
        return result.move.uci() if result.move else None

    def __del__(self):
        """Engine'i temiz bir şekilde kapat"""
        if hasattr(self, 'engine'):
            self.engine.quit()