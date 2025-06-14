from typing import Tuple
from ..board.board import Board
from ..board.player import Player, PlayerType
from .evaluator import PositionEvaluator
from .search import MinimaxSearch
from .progress import ProgressTracker

class AIPlayer:
    def __init__(self, board: Board, depth: int = 3):
        self.board = board
        self.depth = depth
        self.player = Player(PlayerType.WHITE)  # AI is always white
        self.evaluator = PositionEvaluator(board)
        self.progress = ProgressTracker()
    
    def make_move(self) -> Tuple[int, int]:
        """Make the best move using minimax algorithm."""
        valid_moves = self.board.get_valid_moves()
        self.progress.start(len(valid_moves))
        
        search = MinimaxSearch(
            self.board,
            lambda: self.evaluator.evaluate(),
            self.depth
        )
        
        # Override the evaluator to track progress
        def evaluator_with_progress():
            self.progress.increment_nodes()
            return self.evaluator.evaluate()
        
        search.evaluator = evaluator_with_progress
        
        # Perform the search
        score, best_move = search.search()
        
        # Print final result
        print(self.progress.finish(best_move))
        
        return best_move or (7, 7)  # Default to center if no best move found 