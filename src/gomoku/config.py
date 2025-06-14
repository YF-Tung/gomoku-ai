import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent.parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    @property
    def game_time_limit(self) -> int:
        """Get the time limit per player in seconds."""
        return self._config['game']['time_limit']

    @property
    def ai_max_depth(self) -> int:
        """Get the maximum AI search depth."""
        return self._config['ai']['max_depth']

    @property
    def ai_start_depth(self) -> int:
        """Get the starting AI search depth."""
        return self._config['ai']['start_depth']

    @property
    def ai_time_limit(self) -> float:
        """Get the AI time limit per move in seconds."""
        return self._config['ai']['time_limit']

    @property
    def ai_max_search_depth(self) -> int:
        """Get the maximum depth the AI will search."""
        return self._config['ai']['max_search_depth']

    @property
    def board_size(self) -> int:
        """Get the board size."""
        return self._config['board']['size']

    @property
    def win_length(self) -> int:
        """Get the number of pieces in a row needed to win."""
        return self._config['board']['win_length']

# Create a global config instance
config = Config() 