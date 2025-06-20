from typing import Optional, Tuple
import time
from ..board.board import Board
from ..board.player import Player, PlayerType
from ..ai.player import AIPlayer
from ..utils.formatter import BoardFormatter
from .time_manager import TimeManager
from src.gomoku.config import config


class Game:
    def __init__(self):
        """Initialize a new game with settings from config."""
        self.board = Board()
        self.human_player = Player(PlayerType.BLACK)
        self.ai_player = Player(PlayerType.WHITE)
        self.current_player = self.human_player
        self.game_over = False
        self.winner = None
        
        # Initialize AI with config values
        self.ai = AIPlayer(
            self.board,
            depth=config.ai_max_depth,
            time_limit=config.ai_time_limit
        )
        
        # Initialize time manager with config value
        self.time_manager = TimeManager(config.game_time_limit)
        
        self.formatter = BoardFormatter(self.board)
    
    def get_time_remaining(self, player: Player) -> int:
        """Get remaining time for a player in seconds."""
        if self.game_over:
            return self.time_manager.time_remaining[player.type]
        return self.time_manager.get_time_remaining(player.type)
    
    def make_move(self, row: int, col: int) -> Tuple[bool, Optional[str]]:
        """Make a move at the specified position."""
        if self.game_over:
            return False, "Game is already over"
        
        if not self.board.is_valid_move(row, col):
            return False, "Invalid move"
        
        # Make human player's move
        success = self.board.make_move(row, col)
        if not success:
            return False, "Invalid move"
        
        # Check if human player won
        if self.board.check_win(row, col):
            self.game_over = True
            self.winner = self.human_player
            return True, None
        
        # Make AI's move
        ai_row, ai_col = self.ai.get_move()
        success = self.board.make_move(ai_row, ai_col)
        if not success:
            return False, "AI made an invalid move"
        
        # Check if AI won
        if self.board.check_win(ai_row, ai_col):
            self.game_over = True
            self.winner = self.ai_player
            return True, None
        
        return True, None
    
    def get_game_state(self) -> dict:
        """Get current game state for web interface."""
        # Get the last moves for display
        last_move = None
        if self.board.move_history:
            last_row, last_col, player = self.board.move_history[-1]
            last_move = [last_row, last_col]  # Send as list for frontend
        
        return {
            'board': self.board.board.tolist(),  # Convert numpy array to list
            'current_player': self.current_player.type.value,
            'game_over': self.game_over,
            'winner': self.winner.type.value if self.winner else None,
            'time_remaining': self.time_manager.get_time_state(),
            'last_move': last_move
        }
    
    def play(self):
        """Main game loop."""
        print("Welcome to Gomoku!")
        print(f"You are playing as {self.human_player.symbol}")
        print("Enter moves as 'row col' (e.g., '8 8' or 'f f' for corner)")
        print("Coordinates are 1-9 and a-f (case insensitive)")
        
        while True:
            # Display board
            print("\n" + self.formatter.format_board())
            
            # Player's turn (Black)
            while True:
                try:
                    # Get input and convert to lowercase
                    row, col = input("Your move (row col): ").lower().split()
                    # Convert hex coordinates to indices
                    row_idx = self.board.parse_coordinate(row)
                    col_idx = self.board.parse_coordinate(col)
                    success, error = self.make_move(row_idx, col_idx)
                    if success:
                        break
                    print(error)
                except (ValueError, KeyError):
                    print("Invalid input! Enter two coordinates (1-9 or a-f) separated by space.")
            
            if self.game_over:
                print("\n" + self.formatter.format_board())
                print(f"Congratulations! You won!" if self.winner == self.human_player else "AI won! Better luck next time!")
                break
            
            # AI's turn (White)
            ai_row, ai_col = self.ai.get_move()
            self.board.make_move(ai_row, ai_col)
            print(f"AI played: {self.formatter.format_move(ai_row, ai_col)}")
            
            if self.game_over:
                print("\n" + self.formatter.format_board())
                print(f"AI won! Better luck next time!" if self.winner == self.ai_player else "Congratulations! You won!")
                break 