from typing import Tuple, Callable
from ..board.board import Board
from .rules import GameRules

class MinimaxSearch:
    def __init__(self, board: Board, evaluator: Callable[[], int], depth: int = 3):
        self.board = board
        self.evaluator = evaluator
        self.depth = depth
        self.nodes_evaluated = 0
        self.rules = GameRules(board)
    
    def search(self) -> Tuple[float, Tuple[int, int]]:
        """Perform minimax search with alpha-beta pruning."""
        # AI is always player 2 (white)
        return self.minimax(self.depth, float('-inf'), float('inf'), True)
    
    def minimax(self, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Tuple[int, int]]:
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0:
            self.nodes_evaluated += 1
            return self.evaluator(), None
        
        valid_moves = self.rules.get_valid_moves()
        if not valid_moves:
            return 0, None
        
        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                # Save current state
                current_player = self.board.current_player
                # Make move
                self.board.make_move(*move)
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                # Undo move
                self.board.board[move[0]][move[1]] = 0
                self.board.current_player = current_player
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                # Save current state
                current_player = self.board.current_player
                # Make move
                self.board.make_move(*move)
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                # Undo move
                self.board.board[move[0]][move[1]] = 0
                self.board.current_player = current_player
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move 