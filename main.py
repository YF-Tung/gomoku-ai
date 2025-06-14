#!/usr/bin/env python3

import argparse
from src.gomoku.game.game import Game
from src.gomoku.config import config

def main():
    parser = argparse.ArgumentParser(description='Play Gomoku against an AI')
    parser.add_argument('--depth', type=int, default=config.ai_max_depth,
                      help=f'AI search depth (default: {config.ai_max_depth}, higher = stronger but slower)')
    args = parser.parse_args()
    
    # Override config with command line argument if provided
    if args.depth != config.ai_max_depth:
        config._config['ai']['max_depth'] = args.depth
    
    game = Game()
    game.play()

if __name__ == "__main__":
    main()