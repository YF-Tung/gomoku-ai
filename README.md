# Gomoku AI

A Gomoku (Five in a Row) game with an AI opponent, implemented in Python.

## Features

- Play Gomoku against an AI opponent
- Hex-based coordinate system (1-9, a-f)
- Minimax algorithm with alpha-beta pruning for AI moves
- Clean, modern command-line interface

## Requirements

- Python 3.6+
- NumPy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gomoku-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game with default settings:
```bash
python main.py
```

Run with custom AI search depth (higher = stronger but slower):
```bash
python main.py --depth 3
```

## How to Play

1. You play as Black (●), the AI plays as White (○)
2. Enter moves using hex coordinates (1-9, a-f)
3. Example moves:
   - `8 8` for center
   - `f f` for corner
   - `7 7` for near center

## Project Structure

```
src/gomoku/
├── ai/           # AI implementation
├── board/        # Board and game rules
└── game/         # Game flow and UI
```

## License

MIT License 