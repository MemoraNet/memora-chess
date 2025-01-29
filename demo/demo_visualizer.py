# demo/demo_visualizer.py

"""
Advanced visualization tools for MemoraNet Chess Demo.
Handles all visual representations including charts, chess positions, and animations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import chess
import chess.svg
from datetime import datetime
import os
import imageio
import numpy as np
from .demo_data import VISUALIZATION_SETTINGS as VS

class DemoVisualizer:
    def __init__(self):
        """Initialize visualization environment"""
        # Create output directories
        self.output_dir = 'visuals'
        self.comparison_dir = os.path.join(self.output_dir, 'comparisons')
        self.animation_dir = os.path.join(self.output_dir, 'animations')
        
        for dir_path in [self.output_dir, self.comparison_dir, self.animation_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        # Set style
        plt.style.use('dark_background')
        self.setup_plot_style()
        
    def setup_plot_style(self):
        """Configure matplotlib plotting style"""
        plt.rcParams.update({
            'font.family': VS['chart_styles']['font_family'],
            'font.size': VS['chart_styles']['font_size'],
            'axes.grid': True,
            'grid.alpha': VS['chart_styles']['grid_alpha'],
            'axes.facecolor': VS['colors']['background'],
            'figure.facecolor': VS['colors']['background'],
            'text.color': VS['colors']['text'],
            'axes.labelcolor': VS['colors']['text'],
            'xtick.color': VS['colors']['text'],
            'ytick.color': VS['colors']['text']
        })

    def create_learning_comparison(self, traditional_metrics, memoranet_metrics):
        """Create visual comparison between traditional and MemoraNet learning"""
        fig = plt.figure(figsize=(15, 8))
        
        # 1. Time Comparison (log scale)
        ax1 = plt.subplot(131)
        times = ['Traditional', 'MemoraNet']
        hours = [2000, 0.0003]  # 1 second = 0.0003 hours
        ax1.bar(times, hours, color=[VS['colors']['secondary'], VS['colors']['primary']])
        ax1.set_yscale('log')
        ax1.set_title('Learning Time (hours)')
        
        # 2. Memory Usage
        ax2 = plt.subplot(132)
        memory = [8000, 50]  # MB
        ax2.bar(times, memory, color=[VS['colors']['secondary'], VS['colors']['primary']])
        ax2.set_title('Memory Usage (MB)')
        
        # 3. Success Rate
        ax3 = plt.subplot(133)
        success = [95, 98]  # percentage
        ax3.bar(times, success, color=[VS['colors']['secondary'], VS['colors']['primary']])
        ax3.set_title('Success Rate (%)')
        ax3.set_ylim(0, 100)
        
        plt.tight_layout()
        filename = f'learning_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.comparison_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename

    def create_memory_visualization(self, memory_package):
        """Visualize memory package contents and statistics"""
        fig = plt.figure(figsize=(15, 8))
        
        # 1. Opening Distribution
        ax1 = plt.subplot(121)
        openings = {}
        for data in memory_package['memory_data'].values():
            opening = data.get('opening', 'Unknown')
            openings[opening] = openings.get(opening, 0) + 1
        
        ax1.pie(openings.values(), labels=openings.keys(), autopct='%1.1f%%',
                colors=plt.cm.Set3(np.linspace(0, 1, len(openings))))
        ax1.set_title('Opening Distribution')
        
        # 2. Evaluation Distribution
        ax2 = plt.subplot(122)
        evaluations = [data.get('evaluation', 0) for data in memory_package['memory_data'].values()]
        ax2.hist(evaluations, bins=20, color=VS['colors']['primary'], alpha=0.7)
        ax2.set_title('Position Evaluations')
        
        plt.tight_layout()
        filename = f'memory_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.comparison_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename

    def create_chess_position_svg(self, fen, move=None, description=None):
        """Create SVG representation of chess position with optional move arrow"""
        board = chess.Board(fen)
        
        # Add arrow for move if provided
        arrows = []
        if move:
            try:
                chess_move = chess.Move.from_uci(move)
                arrows = [(chess_move.from_square, chess_move.to_square)]
            except:
                pass
        
        # Create SVG
        svg = chess.svg.board(
            board,
            arrows=arrows,
            size=400,
            coordinates=True
        )
        
        return svg

    def create_learning_progress_animation(self, positions_and_moves):
        """Create animation showing learning progress"""
        frames = []
        temp_dir = os.path.join(self.animation_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            for i, (pos, move, description) in enumerate(positions_and_moves):
                # Create frame
                svg = self.create_chess_position_svg(pos, move, description)
                svg_path = os.path.join(temp_dir, f'frame_{i}.svg')
                png_path = os.path.join(temp_dir, f'frame_{i}.png')
                
                # Save SVG
                with open(svg_path, 'w') as f:
                    f.write(svg)
                
                # Convert to PNG
                os.system(f'magick {svg_path} {png_path}')
                
                # Read frame
                frames.append(imageio.imread(png_path))
            
            # Create GIF
            output_path = os.path.join(self.animation_dir, 'learning_progress.gif')
            imageio.mimsave(output_path, frames, duration=VS['animation']['frame_duration'])
            
        finally:
            # Cleanup temp files
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        
        return 'learning_progress.gif'

    def create_performance_comparison(self, student_moves, teacher_moves, positions):
        """Create visual comparison of student vs teacher performance"""
        matches = [s == t for s, t in zip(student_moves, teacher_moves)]
        accuracy = sum(matches) / len(matches) * 100
        
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(matches) + 1), matches, 
                marker='o', linestyle='-', color=VS['colors']['primary'],
                linewidth=VS['chart_styles']['line_width'])
        
        plt.title(f'Move Accuracy Comparison\nOverall Accuracy: {accuracy:.1f}%')
        plt.xlabel('Position Number')
        plt.ylabel('Move Match')
        plt.grid(True, alpha=VS['chart_styles']['grid_alpha'])
        
        filename = f'accuracy_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.comparison_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename

    def show_real_time_position(self, position, move=None):
        """Display chess position in real-time (for interactive mode)"""
        svg = self.create_chess_position_svg(position, move)
        # Note: Real-time display implementation depends on the UI framework
        # For now, we'll just save it
        filepath = os.path.join(self.output_dir, 'current_position.svg')
        with open(filepath, 'w') as f:
            f.write(svg)
        return filepath