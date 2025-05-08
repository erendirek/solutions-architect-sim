#!/usr/bin/env python3
"""
Solutions Architect Simulator - Main Entry Point

This module initializes and runs the Solutions Architect Simulator game.
"""
import sys
from typing import List, Optional

import pygame

from core.game import Game
from core.config import GameConfig


def main() -> None:
    """Initialize and run the Solutions Architect Simulator game."""
    # Initialize pygame
    pygame.init()
    
    # Load game configuration
    config = GameConfig.load_from_file("config/game_config.json")
    
    # Create and run the game
    game = Game(config)
    game.run()
    
    # Clean up pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()