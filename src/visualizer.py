# src/visualizer.py

import chess
import chess.svg
import matplotlib.pyplot as plt
import os
import imageio
import time
from datetime import datetime

class ChessVisualizer:
    def __init__(self, output_dir='chess_visuals'):
        self.board = chess.Board()
        self.output_dir = output_dir
        # Ana klasörü oluştur
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Temp klasörü oluştur
        self.temp_dir = os.path.join(output_dir, 'temp')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def save_position(self, position, move=None, filename=None, description=None):
        """Pozisyonu SVG olarak kaydet"""
        self.board.set_fen(position)
        
        # Hamleyi vurgula
        arrows = []
        if move:
            try:
                chess_move = chess.Move.from_uci(move)
                arrows = [(chess_move.from_square, chess_move.to_square)]
            except:
                pass
        
        # SVG oluştur
        svg_content = chess.svg.board(
            self.board,
            arrows=arrows,
            size=400
        )
        
        if filename is None:
            filename = f"position_{len(os.listdir(self.output_dir))}.svg"
        
        # Tam dosya yolunu oluştur
        if os.path.dirname(filename):
            filepath = filename  # Eğer filename zaten tam yol içeriyorsa
        else:
            filepath = os.path.join(self.output_dir, filename)
            
        # Klasörün var olduğundan emin ol
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(svg_content)
        return filepath
    
    def create_learning_animation(self, positions, moves, descriptions=None):
        """Tüm hamleleri animasyonlu GIF olarak kaydet"""
        images = []
        
        for i, (pos, move) in enumerate(zip(positions, moves)):
            description = descriptions[i] if descriptions else f"Move {i+1}: {move}"
            temp_path = os.path.join(self.temp_dir, f"temp_{i}.svg")
            
            # Her kareyi kaydet
            self.save_position(pos, move, temp_path, description)
            
            # SVG'yi PNG'ye çevir
            png_path = os.path.join(self.temp_dir, f"frame_{i}.png")
            os.system(f"magick {temp_path} {png_path}")
            
            try:
                images.append(imageio.imread(png_path))
            except Exception as e:
                print(f"Frame {i} oluşturulurken hata: {e}")
                continue
        
        if images:
            # Animasyonu kaydet
            output_path = os.path.join(self.output_dir, 'game_animation.gif')
            imageio.mimsave(output_path, images, duration=1)
        
        # Temp dosyaları temizle
        for file in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, file))
            except Exception as e:
                print(f"Temp dosya silinirken hata: {e}")
        
        return output_path

# LearningVisualizer sınıfı aynı kalacak
class LearningVisualizer:
    def __init__(self, output_dir='learning_visuals'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def plot_learning_progress(self, student):
        """Temel öğrenme ilerlemesi grafiği"""
        plt.figure(figsize=(10, 6))
        moves = range(1, student.learned_moves + 1)
        success_rates = [i/5*100 for i in moves]
        
        plt.plot(moves, success_rates, marker='o', color='blue', linewidth=2)
        plt.title(f"{student.name}'s Learning Progress")
        plt.xlabel("Moves Learned")
        plt.ylabel("Success Rate (%)")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        filepath = os.path.join(self.output_dir, 'learning_progress.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    
    def plot_detailed_metrics(self, student):
        """Detaylı öğrenme metrikleri görselleştirmesi"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Öğrenme hızı grafiği
        times = [h['timestamp'] for h in student.learning_history]
        relative_times = [(t - times[0]) for t in times]
        moves = range(1, len(times) + 1)
        
        ax1.plot(relative_times, moves, marker='o', color='green', linewidth=2)
        ax1.set_title('Learning Speed')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Moves Learned')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Başarı oranı grafiği
        success_rates = [i/5*100 for i in moves]
        ax2.plot(moves, success_rates, marker='o', color='blue', linewidth=2)
        ax2.set_title('Success Rate Progress')
        ax2.set_xlabel('Move Number')
        ax2.set_ylabel('Success Rate (%)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, 'detailed_metrics.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath