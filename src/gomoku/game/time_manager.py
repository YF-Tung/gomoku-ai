import time
from typing import Dict
from ..board.player import PlayerType

class TimeManager:
    """Manages time tracking for both players in a game, like a chess clock."""
    
    def __init__(self, time_limit: int = 300):  # 300 seconds = 5 minutes
        self.time_limit = time_limit
        self.time_remaining: Dict[PlayerType, int] = {
            PlayerType.BLACK: time_limit,
            PlayerType.WHITE: time_limit
        }
        self.last_move_time = time.time()
        self.current_player = PlayerType.BLACK  # Black starts
    
    def switch_player(self, new_player: PlayerType):
        """Switch the active player and update time for the previous player."""
        if self.current_player != new_player:
            # Update time for the player who just finished their turn
            current_time = time.time()
            elapsed = current_time - self.last_move_time
            self.time_remaining[self.current_player] = max(0, self.time_remaining[self.current_player] - int(elapsed))
            self.last_move_time = current_time
            self.current_player = new_player
    
    def get_time_remaining(self, player_type: PlayerType) -> int:
        """Get remaining time for a player in seconds."""
        if player_type == self.current_player:
            # For current player, calculate time including current turn
            current_time = time.time()
            elapsed = current_time - self.last_move_time
            return max(0, self.time_remaining[player_type] - int(elapsed))
        else:
            # For other player, return stored time
            return self.time_remaining[player_type]
    
    def get_time_state(self) -> Dict[str, int]:
        """Get current time state for both players."""
        return {
            'black': self.get_time_remaining(PlayerType.BLACK),
            'white': self.get_time_remaining(PlayerType.WHITE)
        }
    
    def reset(self):
        """Reset time tracking to initial state."""
        self.time_remaining = {
            PlayerType.BLACK: self.time_limit,
            PlayerType.WHITE: self.time_limit
        }
        self.last_move_time = time.time()
        self.current_player = PlayerType.BLACK 