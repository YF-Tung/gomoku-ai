#!/usr/bin/env python3

import argparse
from src.gomoku.game.game import Game

def main():
    parser = argparse.ArgumentParser(description='Play Gomoku against an AI')
    parser.add_argument('--depth', type=int, default=2,
                      help='AI search depth (default: 2, higher = stronger but slower)')
    args = parser.parse_args()
    
    game = Game(ai_depth=args.depth)
    game.play()

if __name__ == "__main__":
    main()