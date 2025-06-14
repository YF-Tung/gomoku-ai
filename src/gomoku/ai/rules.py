from typing import List, Tuple
from ..board.board import Board

class GameRules:
    def __init__(self, board: Board):
        self.board = board
        self.first_move_played = False
        self.first_white_move_played = False
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Get valid moves based on game rules and current state."""
        # If it's the first move and we're black, play center
        if not self.first_move_played and self.board.current_player == 1:
            self.first_move_played = True
            return [(7, 7)]
        
        # If it's the first move and we're white, play near center
        if not self.first_white_move_played and self.board.current_player == 2:
            self.first_white_move_played = True
            # Only return moves that are empty
            valid_moves = []
            for move in [(7, 8), (8, 8)]:
                if self.board.board[move[0]][move[1]] == 0:
                    valid_moves.append(move)
            return valid_moves
        
        # For other moves, constrain the search area
        return self._get_constrained_moves()
    
    def _get_constrained_moves(self) -> List[Tuple[int, int]]:
        """Get moves within the constrained area around existing pieces."""
        # Find the bounds of current moves
        min_row = max_row = min_col = max_col = None
        
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != 0:
                    if min_row is None:
                        min_row = max_row = i
                        min_col = max_col = j
                    else:
                        min_row = min(min_row, i)
                        max_row = max(max_row, i)
                        min_col = min(min_col, j)
                        max_col = max(max_col, j)
        
        # If no moves yet, return all empty moves
        if min_row is None:
            return [(i, j) for i in range(self.board.size) 
                   for j in range(self.board.size)
                   if self.board.board[i][j] == 0]
        
        # Expand the bounds by 2 in each direction
        min_row = max(0, min_row - 2)
        max_row = min(self.board.size - 1, max_row + 2)
        min_col = max(0, min_col - 2)
        max_col = min(self.board.size - 1, max_col + 2)
        
        # Return only empty moves within the expanded bounds
        return [(i, j) for i in range(min_row, max_row + 1)
                for j in range(min_col, max_col + 1)
                if self.board.board[i][j] == 0] 