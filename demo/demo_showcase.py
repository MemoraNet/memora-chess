# demo/demo_showcase.py

"""
Main demonstration script for MemoraNet Chess.
Shows the complete workflow of memory extraction, transfer, and validation.
"""

import time
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

# Import local modules
from src.chess_env import ChessEnvironment
from src.chess_agents import TeacherAgent, StudentAgent
from .demo_visualizer import DemoVisualizer
from .demo_data import (
    CHESS_OPENINGS,
    LEARNING_METRICS,
    TEST_SCENARIOS,
    VISUALIZATION_SETTINGS as VS
)

class MemoraNetDemo:
    def __init__(self):
        """Initialize demo environment"""
        self.env = ChessEnvironment()
        self.visualizer = DemoVisualizer()
        
        # Print welcome message
        print("\n=== MemoraNet Demo - AI Memory Transfer System ===")
        print("Demonstrating rapid knowledge transfer in chess AI")
        
    def run_demo(self):
        """Execute main demo sequence"""
        try:
            # 1. Memory Extraction
            print("\n1. Extracting Stockfish Memory...")
            memory_package = self.extract_stockfish_memory()
            
            # 2. Traditional Learning Simulation
            print("\n2. Simulating Traditional Learning Process...")
            self.simulate_traditional_learning()
            
            # 3. MemoraNet Quick Learning
            print("\n3. Demonstrating MemoraNet Quick Learning...")
            student = self.demonstrate_quick_learning(memory_package)
            
            # 4. Performance Testing
            print("\n4. Running Performance Tests...")
            self.run_performance_tests(student, memory_package)
            
            # 5. Visual Comparisons
            print("\n5. Creating Visual Comparisons...")
            self.create_visualizations(memory_package)
            
            # 6. Summary
            self.show_final_summary()
            
        except Exception as e:
            print(f"\nError during demo execution: {e}")
            raise
        
    def extract_stockfish_memory(self) -> Dict:
        """Extract and package Stockfish's chess knowledge"""
        print("Processing Stockfish experience...")
        start_time = time.time()
        
        # Process openings into memory package
        memory_data = {}
        for opening_name, moves in CHESS_OPENINGS.items():
            print(f"Processing {opening_name}...")
            for position_data in moves:
                key = f"{position_data['position']}_{opening_name}"
                memory_data[key] = {
                    "position": position_data['position'],
                    "move": position_data['move'],
                    "evaluation": position_data['evaluation'],
                    "opening": opening_name,
                    "description": position_data['description']
                }
        
        # Create memory package
        memory_package = {
            "metadata": {
                "source": "Stockfish",
                "creation_date": datetime.now().isoformat(),
                "total_positions": len(memory_data),
                "openings_included": list(CHESS_OPENINGS.keys()),
                "metrics": LEARNING_METRICS['traditional']
            },
            "memory_data": memory_data
        }
        
        end_time = time.time()
        print(f"Memory extraction completed in {end_time - start_time:.2f} seconds")
        print(f"Total positions extracted: {len(memory_data)}")
        
        return memory_package
        
    def simulate_traditional_learning(self):
        """Simulate traditional AI learning process"""
        print("Traditional learning process started...")
        metrics = LEARNING_METRICS['traditional']
        
        # Simulate learning progress
        for i in range(5):
            time.sleep(0.5)  # For demonstration
            progress = (i + 1) * 20
            hours = (i + 1) * 400
            print(f"Learning progress: {progress}%")
            print(f"Time elapsed: {hours} hours")
            
        # Show traditional metrics
        print("\nTraditional Learning Metrics:")
        for key, value in metrics.items():
            print(f"- {key}: {value}")
            
    def demonstrate_quick_learning(self, memory_package: Dict):
        """Demonstrate MemoraNet's rapid learning capability"""
        print("Starting MemoraNet quick learning...")
        
        start_time = time.time()
        student = StudentAgent("Quick Learner")
        
        # Load memory package
        print("Loading memory package...")
        student.load_memory_package(memory_package)
        
        end_time = time.time()
        transfer_time = end_time - start_time
        
        # Show quick learning metrics
        print(f"\nQuick Learning Metrics:")
        print(f"- Transfer time: {transfer_time:.2f} seconds")
        print(f"- Positions learned: {len(memory_package['memory_data'])}")
        print(f"- Memory usage: {LEARNING_METRICS['memoranet']['memory_usage']}")
        
        return student
        
    def run_performance_tests(self, student: StudentAgent, memory_package: Dict):
        """Test student agent's performance"""
        print("\nRunning performance tests...")
        
        for scenario in TEST_SCENARIOS:
            print(f"\nTest Scenario: {scenario['name']}")
            correct = 0
            total = len(scenario['positions'])
            
            for pos in scenario['positions']:
                student_move = student.get_move(pos)
                expected_move = next(
                    (data['move'] for data in memory_package['memory_data'].values() 
                     if data['position'] == pos),
                    None
                )
                
                is_correct = student_move == expected_move
                correct += int(is_correct)
                
                print(f"Position: {pos[:30]}...")
                print(f"Student move: {student_move}")
                print(f"Expected move: {expected_move}")
                print(f"Result: {'✓' if is_correct else '✗'}")
                
            success_rate = (correct / total) * 100
            print(f"\nScenario success rate: {success_rate:.1f}%")
            
    def create_visualizations(self, memory_package: Dict):
        """Create visual representations of the demo results"""
        print("Creating visualizations...")
        
        # Learning comparison visualization
        comparison_file = self.visualizer.create_learning_comparison(
            LEARNING_METRICS['traditional'],
            LEARNING_METRICS['memoranet']
        )
        
        # Memory analysis visualization
        analysis_file = self.visualizer.create_memory_visualization(memory_package)
        
        # Learning progress animation
        positions_and_moves = [
            (data['position'], data['move'], data['description']) 
            for data in memory_package['memory_data'].values()
        ]
        animation_file = self.visualizer.create_learning_progress_animation(
            positions_and_moves[:5]  # First 5 moves for demo
        )
        
        print("\nVisualizations completed:")
        print(f"- Comparison chart: {comparison_file}")
        print(f"- Memory analysis: {analysis_file}")
        print(f"- Learning animation: {animation_file}")
        
    def show_final_summary(self):
        """Display final demo summary"""
        print("\n=== Demo Summary ===")
        print("Traditional Learning:")
        print(f"- Time: {LEARNING_METRICS['traditional']['time_required']}")
        print(f"- Success Rate: {LEARNING_METRICS['traditional']['success_rate']}")
        
        print("\nMemoraNet Learning:")
        print(f"- Time: {LEARNING_METRICS['memoranet']['time_required']}")
        print(f"- Success Rate: {LEARNING_METRICS['memoranet']['success_rate']}")
        
        print("\nDemo completed! Visualizations available in 'visuals/' directory.")

def run_demo():
    """Main entry point for running the demo"""
    print("\nMemoraNet Demo - AI Memory Transfer System")
    print("==========================================")
    
    demo = MemoraNetDemo()
    demo.run_demo()

if __name__ == "__main__":
    run_demo()