import time
from typing import Dict
from ..board.player import PlayerType

class TimeManager:
    """Manages time tracking for both players in a game."""
    
    def __init__(self, time_limit: int = 300):  # 300 seconds = 5 minutes
        self.time_limit = time_limit
        self.time_remaining: Dict[PlayerType, int] = {
            PlayerType.BLACK: time_limit,
            PlayerType.WHITE: time_limit
        }
        self.last_move_time = time.time()
    
    def get_time_remaining(self, player_type: PlayerType) -> int:
        """Get remaining time for a player in seconds."""
        current_time = time.time()
        elapsed = current_time - self.last_move_time
        self.time_remaining[player_type] = max(0, self.time_remaining[player_type] - int(elapsed))
        self.last_move_time = current_time
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