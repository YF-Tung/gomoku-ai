from typing import Dict

class CoordinateConverter:
    """Handles conversion between hex coordinates (1-9, a-f) and 0-based indices."""
    
    def __init__(self):
        # Initialize hex mapping for coordinates (1-9, a-f)
        self.hex_map: Dict[str, int] = {str(i): i-1 for i in range(1, 10)}  # 1-9
        self.hex_map.update({c: i+9 for i, c in enumerate('abcdef')})  # a-f
        self.reverse_hex_map: Dict[int, str] = {v: k for k, v in self.hex_map.items()}
    
    def to_index(self, coord: str) -> int:
        """Convert hex coordinate to 0-based index."""
        return self.hex_map[coord.lower()]
    
    def to_coordinate(self, index: int) -> str:
        """Convert 0-based index to hex coordinate."""
        return self.reverse_hex_map[index]
    
    def is_valid_coordinate(self, coord: str) -> bool:
        """Check if a coordinate string is valid."""
        return coord.lower() in self.hex_map 