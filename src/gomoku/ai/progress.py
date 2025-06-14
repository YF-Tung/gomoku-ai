import time
from typing import Tuple, Optional

class ProgressTracker:
    def __init__(self):
        self.start_time = 0
        self.nodes_evaluated = 0
        self.current_move = 0
        self.total_moves = 0
        self.current_depth = 0
        self.best_move: Optional[Tuple[int, int]] = None
        self.best_score = float('-inf')
    
    def start(self, total_moves: int):
        """Start tracking progress."""
        self.start_time = time.time()
        self.nodes_evaluated = 0
        self.current_move = 0
        self.total_moves = total_moves
        self.current_depth = 0
        self.best_move = None
        self.best_score = float('-inf')
        print("\nAI is thinking...")
    
    def update(self, move: int, depth: int, best_move: Tuple[int, int], score: float):
        """Update progress information."""
        self.current_move = move
        self.current_depth = depth
        self.best_move = best_move
        self.best_score = score
    
    def increment_nodes(self):
        """Increment the node counter."""
        self.nodes_evaluated += 1
    
    def get_progress_message(self) -> str:
        """Get the current progress message."""
        elapsed = time.time() - self.start_time
        return (f"Move {self.current_move}/{self.total_moves} "
                f"(Depth {self.current_depth}) "
                f"Best: {self.best_move} Score: {self.best_score:.0f} "
                f"Nodes: {self.nodes_evaluated} Time: {elapsed:.1f}s")
    
    def finish(self, best_move: Tuple[int, int]) -> str:
        """Get the final result message."""
        elapsed = time.time() - self.start_time
        return (f"AI found move: {best_move} "
                f"Nodes evaluated: {self.nodes_evaluated} "
                f"Time: {elapsed:.1f}s") 