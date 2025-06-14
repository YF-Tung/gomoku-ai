from ..board.board import Board
from ..board.player import Player, PlayerType
from ..ai.player import AIPlayer

class Game:
    def __init__(self, ai_depth: int = 2):
        self.board = Board()
        self.human_player = Player(PlayerType.BLACK)
        self.ai_player = Player(PlayerType.WHITE)
        self.ai = AIPlayer(self.board, depth=ai_depth)
    
    def play(self):
        """Main game loop."""
        print("Welcome to Gomoku!")
        print(f"You are playing as {self.human_player.symbol}")
        print("Enter moves as 'row col' (e.g., '8 8' or 'f f' for corner)")
        print("Coordinates are 1-9 and a-f (case insensitive)")
        
        while True:
            # Display board
            print("\n" + self.board.display())
            
            # Player's turn (Black)
            while True:
                try:
                    # Get input and convert to lowercase
                    row, col = input("Your move (row col): ").lower().split()
                    # Convert hex coordinates to indices
                    row_idx = self.board.parse_coordinate(row)
                    col_idx = self.board.parse_coordinate(col)
                    if self.board.make_move(row_idx, col_idx):
                        break
                    print("Invalid move! Try again.")
                except (ValueError, KeyError):
                    print("Invalid input! Enter two coordinates (1-9 or a-f) separated by space.")
            
            if self.board.check_win(row_idx, col_idx):
                print("\n" + self.board.display())
                print("Congratulations! You won!")
                break
            
            # AI's turn (White)
            ai_row, ai_col = self.ai.make_move()
            self.board.make_move(ai_row, ai_col)
            print(f"AI played: {self.board.format_coordinate(ai_row)} {self.board.format_coordinate(ai_col)}")
            
            if self.board.check_win(ai_row, ai_col):
                print("\n" + self.board.display())
                print("AI won! Better luck next time!")
                break 