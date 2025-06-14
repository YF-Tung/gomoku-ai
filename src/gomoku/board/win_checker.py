from typing import Tuple
from .player import Player

class WinChecker:
    """Handles win detection logic for Gomoku."""
    
    def __init__(self, board_size: int):
        self.size = board_size
        self.directions = [(1,0), (0,1), (1,1), (1,-1)]  # horizontal, vertical, diagonal
    
    def check_win(self, board: list[list[int]], row: int, col: int, player_value: int) -> bool:
        """Check if the last move resulted in a win.
        
        Args:
            board: The game board as a 2D list
            row: Row of the last move
            col: Column of the last move
            player_value: Value representing the player (1 for black, 2 for white)
            
        Returns:
            bool: True if the move resulted in a win
        """
        for dr, dc in self.directions:
            count = 1
            # Check forward direction
            for i in range(1, 5):
                r, c = row + dr*i, col + dc*i
                if 0 <= r < self.size and 0 <= c < self.size:
                    if board[r][c] == player_value:
                        count += 1
                    else:
                        break
                else:
                    break
            # Check backward direction
            for i in range(1, 5):
                r, c = row - dr*i, col - dc*i
                if 0 <= r < self.size and 0 <= c < self.size:
                    if board[r][c] == player_value:
                        count += 1
                    else:
                        break
                else:
                    break
            if count >= 5:
                return True
        return False 