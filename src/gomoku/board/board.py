import numpy as np
from typing import Tuple, Optional
from .player import Player, PlayerType
from .win_checker import WinChecker

class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = Player(PlayerType.BLACK)  # Human starts as black
        self.move_history = []
        # Hex mapping for coordinates (1-9, a-f)
        self.hex_map = {str(i): i-1 for i in range(1, 10)}  # 1-9
        self.hex_map.update({c: i+9 for i, c in enumerate('abcdef')})  # a-f
        self.reverse_hex_map = {v: k for k, v in self.hex_map.items()}
        self.win_checker = WinChecker(size)
    
    def parse_coordinate(self, coord: str) -> int:
        """Convert hex coordinate to 0-based index."""
        return self.hex_map[coord.lower()]
    
    def format_coordinate(self, index: int) -> str:
        """Convert 0-based index to hex coordinate."""
        return self.reverse_hex_map[index]
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move on the board. Returns True if move is valid."""
        if not self.is_valid_move(row, col):
            return False
            
        # Record the move with current player
        self.board[row][col] = self.current_player.type.value
        self.move_history.append((row, col, self.current_player))
        
        # Switch player after recording the move
        self.current_player = self.current_player.get_opponent()
        return True
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid."""
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == 0)
    
    def get_piece_at(self, row: int, col: int) -> Optional[Player]:
        """Get the player at the given position, or None if empty."""
        value = self.board[row][col]
        if value == 0:
            return None
        return Player(PlayerType(value))
    
    def check_win(self, row: int, col: int) -> bool:
        """Check if the last move resulted in a win."""
        player = self.get_piece_at(row, col)
        if not player:
            return False
        return self.win_checker.check_win(self.board.tolist(), row, col, player.type.value)
    
    def get_valid_moves(self) -> list[Tuple[int, int]]:
        """Get all valid moves on the board."""
        return [(i, j) for i in range(self.size) for j in range(self.size) 
                if self.is_valid_move(i, j)]
    
    def display(self) -> str:
        """Return a string representation of the board."""
        result = []
        
        # Add column headers (1-9, a-f)
        header = '   ' + ' '.join(f'{self.format_coordinate(i)}' for i in range(self.size))
        result.append(header)
        
        # Add rows with row numbers (1-9, a-f)
        for i in range(self.size):
            row = [f'{self.format_coordinate(i):2}']  # Row number
            for j in range(self.size):
                piece = self.get_piece_at(i, j)
                symbol = piece.symbol if piece else '·'
                row.append(symbol)
            result.append(' '.join(row))
        
        return '\n'.join(result) 