import chess
import chess.engine
import json
import time
import os
from typing import Dict, List, Optional, Tuple

class StockfishMemoryExtractor:
    def __init__(self, engine_path: str = "/opt/homebrew/bin/stockfish"):
        """Initialize Stockfish memory extractor"""
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            self.board = chess.Board()
            print("Stockfish engine initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize Stockfish engine: {e}")
            raise

    def extract_position_knowledge(self, position: str, depth: int = 20) -> Optional[Dict]:
        """Extract Stockfish's knowledge about a specific position"""
        try:
            self.board.set_fen(position)
            
            # Analyze position with multiple variations
            result = self.engine.analyse(
                self.board,
                chess.engine.Limit(depth=depth, time=0.5),
                multipv=3  # Get top 3 moves
            )
            
            if not result:
                print(f"No analysis result for position: {position}")
                return None
                
            main_line = result[0]
            if not main_line.get("pv"):
                print(f"No PV found for position: {position}")
                return None
                
            best_move = main_line["pv"][0]
            
            return {
                "position": position,
                "best_move": best_move.uci(),
                "evaluation": self._parse_evaluation(main_line),
                "depth": main_line.get("depth", 0),
                "principal_variation": [move.uci() for move in main_line["pv"][:5]],
                "alternative_moves": [
                    {
                        "move": line["pv"][0].uci(),
                        "evaluation": self._parse_evaluation(line)
                    }
                    for line in result[1:] if line.get("pv")
                ],
                "timestamp": time.time()
            }
            
        except Exception as e:
            print(f"Analysis error for position {position}: {e}")
            return None

    def _parse_evaluation(self, line: Dict) -> float:
        """Parse Stockfish evaluation score"""
        if "score" in line:
            score = line["score"]
            if score.is_mate():
                return 10000 if score.mate() > 0 else -10000
            else:
                return score.relative.score() / 100.0
        return 0.0

    def create_memory_package(self, num_games: int = 5, 
                            positions_per_game: int = 20,
                            depth: int = 20) -> Optional[Dict]:
        """Create a complete memory package from multiple games"""
        try:
            memory_package = {
                "metadata": {
                    "source": "Stockfish",
                    "creation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "engine_depth": depth,
                    "total_positions": 0,
                    "total_games": num_games
                },
                "memories": {}
            }
            
            for game_id in range(num_games):
                print(f"\nExtracting game {game_id + 1}/{num_games}...")
                self.board.reset()
                
                for move_number in range(positions_per_game):
                    position = self.board.fen()
                    
                    # Extract knowledge for current position
                    memory = self.extract_position_knowledge(position, depth)
                    if memory:
                        key = f"game_{game_id}_pos_{move_number}"
                        memory_package["memories"][key] = memory
                        
                        # Make the best move
                        try:
                            best_move = chess.Move.from_uci(memory["best_move"])
                            if best_move in self.board.legal_moves:
                                self.board.push(best_move)
                            else:
                                print(f"Invalid move generated: {best_move}")
                                break
                        except Exception as e:
                            print(f"Error making move: {e}")
                            break
                            
                        if self.board.is_game_over():
                            break
                    else:
                        print(f"Failed to analyze position: {position}")
                        break
                
            memory_package["metadata"]["total_positions"] = len(memory_package["memories"])
            return memory_package
            
        except Exception as e:
            print(f"Error creating memory package: {e}")
            return None

    def save_memory_package(self, package: Dict, filename: str):
        """Save memory package to file"""
        if not filename.endswith('.stockfish'):
            filename += '.stockfish'
            
        with open(filename, 'w') as f:
            json.dump(package, f, indent=2)

    def load_memory_package(self, filename: str) -> Dict:
        """Load memory package from file"""
        with open(filename, 'r') as f:
            return json.load(f)

    def __del__(self):
        """Cleanup engine properly"""
        try:
            if hasattr(self, 'engine') and self.engine:
                try:
                    self.engine.quit()
                except chess.engine.EngineTerminatedError:
                    pass  # Ignore if already terminated
                except Exception as e:
                    print(f"Warning: Engine cleanup error: {e}")
                finally:
                    self.engine = None
        except Exception as e:
            print(f"Cleanup error: {e}")

def test_extraction():
    """Test memory extraction functionality"""
    extractor = StockfishMemoryExtractor()
    
    # Create test package
    package = extractor.create_memory_package(
        num_games=2,
        positions_per_game=10,
        depth=15
    )
    
    if package:
        # Save package
        extractor.save_memory_package(package, "test_stockfish_memory")
        
        # Print statistics
        print("\nMemory Package Statistics:")
        print(f"Total positions: {package['metadata']['total_positions']}")
        print(f"Engine depth: {package['metadata']['engine_depth']}")
        
        # Show sample position
        sample_key = list(package['memories'].keys())[0]
        sample_memory = package['memories'][sample_key]
        print("\nSample Position Analysis:")
        print(f"Position: {sample_memory['position']}")
        print(f"Best move: {sample_memory['best_move']}")
        print(f"Evaluation: {sample_memory['evaluation']}")
        print(f"Principal variation: {sample_memory['principal_variation']}")

if __name__ == "__main__":
    test_extraction()