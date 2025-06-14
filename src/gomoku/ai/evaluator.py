from typing import Tuple
from ..board.board import Board

class PositionEvaluator:
    def __init__(self, board: Board):
        self.board = board
    
    def evaluate(self) -> int:
        """Evaluate the current board position."""
        score = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]  # horizontal, vertical, diagonal
        
        # Evaluate for both players
        for player in [1, 2]:
            multiplier = 1 if player == 2 else -1  # AI is player 2
            
            for i in range(self.board.size):
                for j in range(self.board.size):
                    if self.board.board[i][j] == player:
                        # Check each direction
                        for dr, dc in directions:
                            # Count consecutive pieces
                            count = 1
                            blocked = 0
                            
                            # Check forward
                            for k in range(1, 5):
                                r, c = i + dr*k, j + dc*k
                                if 0 <= r < self.board.size and 0 <= c < self.board.size:
                                    if self.board.board[r][c] == player:
                                        count += 1
                                    elif self.board.board[r][c] != 0:
                                        blocked += 1
                                        break
                                    else:
                                        break
                                else:
                                    blocked += 1
                                    break
                            
                            # Check backward
                            for k in range(1, 5):
                                r, c = i - dr*k, j - dc*k
                                if 0 <= r < self.board.size and 0 <= c < self.board.size:
                                    if self.board.board[r][c] == player:
                                        count += 1
                                    elif self.board.board[r][c] != 0:
                                        blocked += 1
                                        break
                                    else:
                                        break
                                else:
                                    blocked += 1
                                    break
                            
                            # Score based on consecutive pieces and blocked ends
                            if count >= 5:
                                score += 100000 * multiplier  # Win
                            elif count == 4:
                                if blocked == 0:
                                    score += 10000 * multiplier  # Open four
                                elif blocked == 1:
                                    score += 1000 * multiplier  # Blocked four
                            elif count == 3:
                                if blocked == 0:
                                    score += 1000 * multiplier  # Open three
                                elif blocked == 1:
                                    score += 100 * multiplier  # Blocked three
                            elif count == 2:
                                if blocked == 0:
                                    score += 100 * multiplier  # Open two
                                elif blocked == 1:
                                    score += 10 * multiplier  # Blocked two
        
        return score 