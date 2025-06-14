from typing import Optional, Tuple
import time
from ..board.board import Board
from ..board.player import Player, PlayerType
from ..ai.player import AIPlayer
from ..utils.formatter import BoardFormatter

class Game:
    def __init__(self, ai_depth: int = 3, time_limit: int = 300):  # 300 seconds = 5 minutes
        self.board = Board()
        self.human_player = Player(PlayerType.BLACK)
        self.ai_player = Player(PlayerType.WHITE)
        self.ai = AIPlayer(self.board, depth=ai_depth)
        self.current_player = self.human_player
        self.game_over = False
        self.winner = None
        self.time_limit = time_limit
        self.time_remaining = {
            PlayerType.BLACK: time_limit,
            PlayerType.WHITE: time_limit
        }
        self.last_move_time = time.time()
        self.formatter = BoardFormatter(self.board)
    
    def get_time_remaining(self, player_type: PlayerType) -> int:
        """Get remaining time for a player in seconds."""
        if self.game_over:
            return self.time_remaining[player_type]
            
        current_time = time.time()
        elapsed = current_time - self.last_move_time
        self.time_remaining[player_type] = max(0, self.time_remaining[player_type] - int(elapsed))
        self.last_move_time = current_time
        return self.time_remaining[player_type]
    
    def make_move(self, row: int, col: int) -> Tuple[bool, Optional[str]]:
        """Make a move and return (success, error_message)."""
        if self.game_over:
            return False, "Game is already over"
            
        if self.current_player != self.human_player:
            return False, "Not your turn"
            
        if not self.board.is_valid_move(row, col):
            return False, "Invalid move"
            
        # Update time for black player
        self.get_time_remaining(PlayerType.BLACK)
        
        # Make the move
        if not self.board.make_move(row, col):
            return False, "Invalid move"
        
        # Check for win
        if self.board.check_win(row, col):
            self.game_over = True
            self.winner = self.human_player
            return True, None
            
        # Switch to AI
        self.current_player = self.ai_player
        
        # AI makes move
        ai_row, ai_col = self.ai.make_move()
        self.board.make_move(ai_row, ai_col)
        
        # Update time for white player
        self.get_time_remaining(PlayerType.WHITE)
        
        # Check for AI win
        if self.board.check_win(ai_row, ai_col):
            self.game_over = True
            self.winner = self.ai_player
            return True, None
            
        # Switch back to player
        self.current_player = self.human_player
        
        return True, None
    
    def get_game_state(self) -> dict:
        """Get current game state for web interface."""
        return {
            'board': self.board.board.tolist(),  # Convert numpy array to list
            'current_player': self.current_player.type.value,
            'game_over': self.game_over,
            'winner': self.winner.type.value if self.winner else None,
            'time_remaining': {
                'black': self.get_time_remaining(PlayerType.BLACK),
                'white': self.get_time_remaining(PlayerType.WHITE)
            }
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
            ai_row, ai_col = self.ai.make_move()
            self.board.make_move(ai_row, ai_col)
            print(f"AI played: {self.formatter.format_move(ai_row, ai_col)}")
            
            if self.game_over:
                print("\n" + self.formatter.format_board())
                print(f"AI won! Better luck next time!" if self.winner == self.ai_player else "Congratulations! You won!")
                break 