from typing import Tuple
import time
from ..board.board import Board
from ..board.player import Player, PlayerType
from .evaluator import PositionEvaluator
from .search import MinimaxSearch
from .progress import ProgressTracker

class AIPlayer:
    def __init__(self, board: Board, depth: int = 3, time_limit: float = 10.0):
        self.board = board
        self.depth = depth
        self.time_limit = time_limit  # Time limit in seconds
        self.player = Player(PlayerType.WHITE)  # AI is always white
        self.evaluator = PositionEvaluator(board)
        self.progress = ProgressTracker()
        self.first_move_made = False
    
    def _get_first_move(self) -> Tuple[int, int]:
        """Get the optimal first move for white."""
        last_row, last_col, _ = self.board.move_history[-1]
        adjacent_moves = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in adjacent_moves:
            new_row, new_col = last_row + dr, last_col + dc
            if self.board.is_valid_move(new_row, new_col):
                return new_row, new_col
        return 7, 7  # Fallback to center
    
    def _search_with_time_limit(self, start_depth: int = 2) -> Tuple[float, Tuple[int, int]]:
        """Perform iterative deepening search with time limit."""
        best_score = float('-inf')
        best_move = None
        current_depth = start_depth
        start_time = time.time()
        max_depth = 3  # Cap the maximum search depth
        
        print(f"\nStarting AI search at depth {current_depth}...")
        
        while time.time() - start_time < self.time_limit and current_depth <= max_depth:
            print(f"\nTrying depth {current_depth}...")
            search = MinimaxSearch(
                self.board,
                lambda: self.evaluator.evaluate(),
                current_depth
            )
            
            # Override the evaluator to track progress
            def evaluator_with_progress():
                self.progress.increment_nodes()
                return self.evaluator.evaluate()
            
            search.evaluator = evaluator_with_progress
            
            try:
                score, move = search.search()
                if move:  # Only update if we found a valid move
                    best_score = score
                    best_move = move
                    print(f"✓ Depth {current_depth} completed:")
                    print(f"  - Best move: {move}")
                    print(f"  - Score: {score}")
                    print(f"  - Time used: {time.time() - start_time:.2f}s")
                    
                    if current_depth == max_depth:
                        print(f"\nReached maximum depth {max_depth}, stopping search.")
                        break
                        
                    # Check if we have time for next depth
                    time_left = self.time_limit - (time.time() - start_time)
                    if time_left < 2.0:  # Less than 2 seconds left
                        print(f"\nNot enough time ({time_left:.2f}s) for depth {current_depth + 1}, stopping search.")
                        break
                    print(f"\nTime remaining: {time_left:.2f}s, attempting depth {current_depth + 1}...")
            except TimeoutError:
                print(f"× Timeout at depth {current_depth}")
                break
                
            current_depth += 1
            
        if best_move:
            print(f"\nFinal decision:")
            print(f"- Best move: {best_move}")
            print(f"- Score: {best_score}")
            print(f"- Search depth: {current_depth - 1}")
            print(f"- Total time: {time.time() - start_time:.2f}s")
        else:
            print("\nWARNING: No valid move found!")
            
        return best_score, best_move
    
    def make_move(self) -> Tuple[int, int]:
        """Make the best move using minimax algorithm."""
        print("\nAI is thinking...")
        if not self.first_move_made and len(self.board.move_history) == 1:
            print("Making first move (adjacent to black)...")
            self.first_move_made = True
            return self._get_first_move()
            
        valid_moves = self.board.get_valid_moves()
        print(f"Found {len(valid_moves)} valid moves to evaluate")
        self.progress.start(len(valid_moves))
        
        # Start with depth 2 for faster initial response
        print("Starting search at depth 2...")
        score, best_move = self._search_with_time_limit(start_depth=2)
        
        if best_move:
            print(f"AI chose move: {best_move} with score: {score}")
        else:
            print("WARNING: No best move found, using center as fallback")
            best_move = (7, 7)
        
        # Print final result
        print(self.progress.finish(best_move))
        
        return best_move 