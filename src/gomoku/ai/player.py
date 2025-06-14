from typing import Tuple
import time
import random
from ..board.board import Board
from ..board.player import Player, PlayerType
from .evaluator import PositionEvaluator
from .search import MinimaxSearch
from .progress import ProgressTracker
from src.gomoku.config import config

class AIPlayer:
    def __init__(self, board: Board, depth: int = 3, time_limit: float = 10.0):
        self.board = board
        self.depth = depth
        self.time_limit = time_limit  # Time limit in seconds
        self.player = Player(PlayerType.WHITE)  # AI is always white
        self.evaluator = PositionEvaluator(board)
        self.progress = ProgressTracker()
        self.first_move_made = False
        self.last_score = None  # Store the last evaluation score
    
    def _get_first_move(self) -> Tuple[int, int]:
        """Get the optimal first move for white."""
        last_row, last_col, _ = self.board.move_history[-1]
        adjacent_moves = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in adjacent_moves:
            new_row, new_col = last_row + dr, last_col + dc
            if self.board.is_valid_move(new_row, new_col):
                self.last_score = None  # No score for first move
                return new_row, new_col
        self.last_score = None  # No score for first move
        return 7, 7  # Fallback to center
    
    def _search_with_time_limit(self, start_depth: int = 2) -> Tuple[float, Tuple[int, int]]:
        """Perform iterative deepening search with time limit and early cutoff."""
        best_score = float('-inf')
        best_move = None
        current_depth = start_depth
        start_time = time.time()
        max_depth = self.depth  # Use the configured depth
        win_threshold = config.win_score_threshold
        lose_threshold = config.lose_score_threshold
        
        print(f"\nStarting AI search at depth {current_depth}...")
        
        # First try to get at least one move at minimum depth
        try:
            search = MinimaxSearch(
                self.board,
                lambda: self.evaluator.evaluate(),
                current_depth
            )
            
            def evaluator_with_progress():
                self.progress.increment_nodes()
                return self.evaluator.evaluate()
            
            search.evaluator = evaluator_with_progress
            
            score, move = search.search()
            if move:
                best_score = score
                best_move = move
                print(f"✓ Initial depth {current_depth} completed:")
                print(f"  - Best move: {move}")
                print(f"  - Score: {score}")
                print(f"  - Time used: {time.time() - start_time:.2f}s")
                # Early cutoff if score is decisive
                if best_score >= win_threshold or best_score <= lose_threshold:
                    print(f"Early cutoff: Decisive score ({best_score}) found at depth {current_depth}.")
                    return best_score, best_move
        except Exception as e:
            print(f"× Error at initial depth {current_depth}: {str(e)}")
            valid_moves = self.board.get_valid_moves()
            if valid_moves:
                best_move = valid_moves[0]
                print(f"Using fallback move: {best_move}")
            return 0, best_move
        
        # Now try deeper searches if we have time
        while time.time() - start_time < self.time_limit and current_depth < max_depth:
            current_depth += 1
            print(f"\nTrying depth {current_depth}...")
            
            try:
                search = MinimaxSearch(
                    self.board,
                    lambda: self.evaluator.evaluate(),
                    current_depth
                )
                search.evaluator = evaluator_with_progress
                
                score, move = search.search()
                if move:
                    best_score = score
                    best_move = move
                    print(f"✓ Depth {current_depth} completed:")
                    print(f"  - Best move: {move}")
                    print(f"  - Score: {score}")
                    print(f"  - Time used: {time.time() - start_time:.2f}s")
                    # Early cutoff if score is decisive
                    if best_score >= win_threshold or best_score <= lose_threshold:
                        print(f"Early cutoff: Decisive score ({best_score}) found at depth {current_depth}.")
                        break
                    time_left = self.time_limit - (time.time() - start_time)
                    if time_left < 2.0:
                        print(f"\nNot enough time ({time_left:.2f}s) for depth {current_depth + 1}, stopping search.")
                        break
                    print(f"\nTime remaining: {time_left:.2f}s, attempting depth {current_depth + 1}...")
            except Exception as e:
                print(f"× Error at depth {current_depth}: {str(e)}")
                break
        
        if best_move:
            print(f"\nFinal decision:")
            print(f"- Best move: {best_move}")
            print(f"- Score: {best_score}")
            print(f"- Search depth: {current_depth}")
            print(f"- Total time: {time.time() - start_time:.2f}s")
        else:
            print("\nWARNING: No valid move found!")
            best_move = (7, 7)
        
        return best_score, best_move
    
    def get_move(self) -> Tuple[int, int]:
        """Get the next move for the AI player."""
        print("\nAI is thinking...")
        self.progress = ProgressTracker()
        
        # Special handling for first white move (must be within one space of black's first move)
        if len(self.board.move_history) == 1:
            print("First white move - applying one-space rule")
            last_row, last_col, _ = self.board.move_history[0]
            valid_moves = []
            
            # Check all 8 surrounding positions
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:  # Skip the center (black's move)
                        continue
                    new_row, new_col = last_row + dr, last_col + dc
                    if self.board.is_valid_move(new_row, new_col):
                        valid_moves.append((new_row, new_col))
            
            if valid_moves:
                # Choose a random valid move from the surrounding positions
                move = random.choice(valid_moves)
                print(f"Selected first white move: {move}")
                return move
            else:
                print("No valid surrounding moves found, falling back to normal move selection")
        
        # Normal move selection for other moves
        score, move = self._search_with_time_limit()
        return move 