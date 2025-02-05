import chess
import time
from typing import Dict, List
import json
from src.memory_extractor import StockfishMemoryExtractor
from src.memory_tokenizer import MemoryTokenizer
from src.chess_agents import StudentAgent
from demo.demo_visualizer import DemoVisualizer
from demo.demo_data import CHESS_OPENINGS, INTERACTIVE_SETTINGS

class InteractiveMemoryDemo:
    def __init__(self):
        """Initialize demo components"""
        print("\nInitializing MemoraNet Chess Memory Transfer Demo...")
        self.visualizer = DemoVisualizer()
        self.extractor = StockfishMemoryExtractor()
        self.tokenizer = MemoryTokenizer()
        self.student = StudentAgent("MemoraNet Student")
        
    def run_demo(self):
        """Run the complete demo process"""
        try:
            self._show_welcome_message()
            
            # 1. Memory Extraction
            memory_package = self._extract_memories()
            if not memory_package:
                print("Memory extraction failed!")
                return
                
            # 2. Memory Tokenization
            tokenized_package = self._tokenize_memories(memory_package)
            if not tokenized_package:
                print("Tokenization failed!")
                return
                
            # 3. Learning
            success = self._demonstrate_learning(tokenized_package)
            if not success:
                print("Learning failed!")
                return
                
            # 4. Interactive Testing
            self._interactive_testing()
            
        except KeyboardInterrupt:
            print("\nDemo stopped by user.")
        except Exception as e:
            print(f"\nError occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._cleanup()

    def _show_welcome_message(self):
        """Show welcome message and demo information"""
        print("\n=== MemoraNet Chess Memory Transfer Demo ===")
        print("This demo demonstrates how Stockfish's chess knowledge")
        print("can be tokenized and transferred to a new agent.")
        print("\nFeatures:")
        print("- Stockfish memory extraction")
        print("- Memory tokenization")
        print("- Rapid learning")
        print("- Interactive testing")
        input("\nPress ENTER to start...")

    def _extract_memories(self) -> Dict:
        """Extract memories from Stockfish"""
        print("\n1. Extracting Stockfish Memory")
        print("--------------------------------")
        
        positions = int(input("Number of positions to analyze (recommended: 20): ") or 20)
        depth = int(input("Analysis depth (recommended: 15): ") or 15)
        
        print("\nStarting Stockfish analysis...")
        start_time = time.time()
        
        memory_package = self.extractor.create_memory_package(
            num_games=2,
            positions_per_game=positions,
            depth=depth
        )
        
        duration = time.time() - start_time
        print(f"\nMemory extraction completed!")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total positions: {memory_package['metadata']['total_positions']}")
        
        self._show_sample_position(memory_package)
        
        return memory_package

    def _tokenize_memories(self, memory_package: Dict) -> Dict:
        """Tokenize extracted memories"""
        print("\n2. Memory Tokenization")
        print("----------------------")
        
        print("Starting memory tokenization...")
        start_time = time.time()
        
        tokenized_package = self.tokenizer.tokenize_stockfish_memory(memory_package)
        
        duration = time.time() - start_time
        print(f"\nTokenization completed!")
        print(f"Duration: {duration:.2f} seconds")
        
        self._show_sample_tokens(tokenized_package)
        
        return tokenized_package

    def _demonstrate_learning(self, tokenized_package: Dict) -> bool:
        """Demonstrate the learning process"""
        print("\n3. Rapid Learning")
        print("----------------")
        
        print("Starting learning process...")
        self.student.learn_from_tokenized_memory(tokenized_package)
        
        stats = self.student.get_learning_stats()
        print("\nLearning Statistics:")
        print(f"Positions learned: {stats['total_learned_moves']}")
        print(f"Unique patterns: {stats['unique_patterns']}")
        print(f"Average confidence: {stats['average_confidence']}%")
        print(f"Learning progress: {stats['learning_progress']}")
        
        return True

    def _interactive_testing(self):
        """Interactive testing phase"""
        print("\n4. Interactive Testing")
        print("----------------")
        print("Test options:")
        print("1. Test prepared positions")
        print("2. Test with custom FEN")
        print("3. Play a game")
        
        choice = input("\nSelect option (1-3): ")
        
        if choice == '1':
            self._test_prepared_positions()
        elif choice == '2':
            self._test_custom_positions()
        elif choice == '3':
            self._play_game()
        else:
            print("Invalid selection!")

    def _test_opening(self, opening_name: str):
        """Test a specific opening"""
        print(f"\nTesting {opening_name}...")
        self.student.reset_game()
        board = chess.Board()
        
        while not board.is_game_over():
            print(f"\nCurrent position:")
            print(board)
            
            move = self.student.get_move(board.fen())
            if move:
                self.student.make_move(board.fen(), move)
                confidence = self.student.confidence_scores.get(board.fen(), 0)
                
                print(f"Selected move: {move}")
                print(f"Confidence score: {confidence:.1f}%")
                print(f"Opening: {self.student.current_opening}")
                
                try:
                    chess_move = chess.Move.from_uci(move)
                    if chess_move in board.legal_moves:
                        board.push(chess_move)
                        print("\nPosition after move:")
                        print(board)
                    else:
                        print("Warning: Selected move is not legal!")
                        break
                except Exception as e:
                    print(f"Error making move: {e}")
                    break
            else:
                print("Warning: No move found for this position!")
                break

    def _test_prepared_positions(self):
        """Test with prepared positions"""
        for opening in ["Ruy Lopez", "Sicilian Defense", "French Defense"]:
            self._test_opening(opening)

    def _test_custom_positions(self):
        """Test with custom FEN positions"""
        while True:
            fen = input("\nEnter FEN position (or 'q' to quit): ")
            if fen.lower() == 'q':
                break
                
            board = chess.Board(fen)
            move = self.student.get_move(fen)
            
            if move:
                self.student.make_move(fen, move)
                confidence = self.student.confidence_scores.get(fen, 0)
                
                print(f"\nSelected move: {move}")
                print(f"Confidence score: {confidence:.1f}%")
                print(f"Opening: {self.student.current_opening}")
                
                try:
                    chess_move = chess.Move.from_uci(move)
                    if chess_move in board.legal_moves:
                        board.push(chess_move)
                        print("\nPosition after move:")
                        print(board)
                    else:
                        print("Warning: Selected move is not legal!")
                except Exception as e:
                    print(f"Error making move: {e}")
            else:
                print("Warning: No move found for this position!")

    def _play_game(self):
        """Play a game against the student"""
        board = chess.Board()
        self.student.reset_game()
        
        while not board.is_game_over():
            print(f"\n{board}")
            
            if board.turn == chess.WHITE:
                # Human move
                move = input("Enter your move (UCI format, e.g., e2e4): ")
                if move in [str(m) for m in board.legal_moves]:
                    board.push_san(move)
                    self.student.make_move(board.fen(), move)
                else:
                    print("Invalid move!")
                    continue
            else:
                # Student move
                move = self.student.get_move(board.fen())
                if move:
                    self.student.make_move(board.fen(), move)
                    confidence = self.student.confidence_scores.get(board.fen(), 0)
                    
                    print(f"Student's move: {move}")
                    print(f"Confidence score: {confidence:.1f}%")
                    print(f"Opening: {self.student.current_opening}")
                    
                    chess_move = chess.Move.from_uci(move)
                    if chess_move in board.legal_moves:
                        board.push(chess_move)
                    else:
                        print("Warning: Student selected invalid move!")
                        break
                else:
                    print("Student couldn't find a move!")
                    break

    def _show_sample_position(self, memory_package: Dict):
        """Show a sample position from memory package"""
        sample_key = list(memory_package['memories'].keys())[0]
        sample = memory_package['memories'][sample_key]
        
        print("\nSample Position Analysis:")
        print(f"FEN: {sample['position']}")
        print(f"Best move: {sample['best_move']}")
        print(f"Evaluation: {sample['evaluation']}")

    def _show_sample_tokens(self, tokenized_package: Dict):
        """Show sample tokenized data"""
        sample_key = list(tokenized_package['tokenized_memories'].keys())[0]
        sample = tokenized_package['tokenized_memories'][sample_key]
        
        print("\nSample Token Structure:")
        print(f"Position tokens: {sample['position_tokens'][:10]}...")
        print(f"Move tokens: {sample['move_tokens']}")
        print(f"Evaluation token: {sample['evaluation_token']}")

    def _cleanup(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'extractor'):
                try:
                    self.extractor.engine.quit()
                except chess.engine.EngineTerminatedError:
                    pass
                except Exception as e:
                    print(f"Engine cleanup warning: {e}")
        except Exception as e:
            print(f"Cleanup error: {e}")

def run_demo():
    """Main entry point"""
    demo = InteractiveMemoryDemo()
    demo.run_demo()

if __name__ == "__main__":
    run_demo()