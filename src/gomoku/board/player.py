from enum import Enum
from typing import Tuple

class PlayerType(Enum):
    BLACK = 1
    WHITE = 2

class Player:
    def __init__(self, player_type: PlayerType):
        self.type = player_type
        self.symbol = '●' if player_type == PlayerType.BLACK else '○'
    
    def get_opponent(self) -> 'Player':
        return Player(PlayerType.WHITE if self.type == PlayerType.BLACK else PlayerType.BLACK)
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.type == other.type 