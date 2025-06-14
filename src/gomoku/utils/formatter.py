from typing import List
from ..board.board import Board
from .coordinate import CoordinateConverter

class BoardFormatter:
    """Handles formatting of the board for display."""
    
    def __init__(self, board: Board):
        self.board = board
        self.coord_converter = CoordinateConverter()
    
    def format_board(self) -> str:
        """Return a string representation of the board."""
        result = []
        
        # Add column headers (1-9, a-f)
        header = '   ' + ' '.join(f'{self.coord_converter.to_coordinate(i)}' 
                                for i in range(self.board.size))
        result.append(header)
        
        # Add rows with row numbers (1-9, a-f)
        for i in range(self.board.size):
            row = [f'{self.coord_converter.to_coordinate(i):2}']  # Row number
            for j in range(self.board.size):
                piece = self.board.get_piece_at(i, j)
                symbol = piece.symbol if piece else '·'
                row.append(symbol)
            result.append(' '.join(row))
        
        return '\n'.join(result)
    
    def format_move(self, row: int, col: int) -> str:
        """Format a move as a coordinate pair."""
        return f"{self.coord_converter.to_coordinate(row)} {self.coord_converter.to_coordinate(col)}" 