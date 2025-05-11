"""
Time management module for the Solutions Architect Simulator.
"""
from typing import Any, Optional

import pygame

from core.state import GameMode


class TimeManager:
    """Manages time-related functionality in the game."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the time manager.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.last_update_time = 0
        self.time_out = False
    
    def update(self) -> None:
        """Update time-related game state."""
        # Only update time in TIME_TRIAL mode
        from core.state import GameMode
        if self.game.state.mode != GameMode.TIME_TRIAL:
            return
            
        # Skip if time has already run out
        if self.time_out:
            return
            
        # Get current time
        current_time = pygame.time.get_ticks()
        
        # Initialize last_update_time if this is the first update
        if self.last_update_time == 0:
            self.last_update_time = current_time
            return
        
        # Calculate elapsed time in seconds since last update
        elapsed_seconds = (current_time - self.last_update_time) / 1000
        self.last_update_time = current_time
        
        # Update time remaining
        if self.game.state.time_remaining is not None:
            self.game.state.time_remaining -= elapsed_seconds
            
            # Check if time has run out
            if self.game.state.time_remaining <= 0:
                self.game.state.time_remaining = 0
                self.time_out = True
                self._handle_time_out()
    
    def reset(self) -> None:
        """Reset the time manager state."""
        self.last_update_time = 0
        self.time_out = False
    
    def _handle_time_out(self) -> None:
        """Handle time running out in time trial mode."""
        # Show time out message
        self.game.ui_manager.show_message("Time's up! You didn't complete the level in time.")
        
        # Double the score if the level was completed in time trial mode
        if self.game.state.score > 0:
            self.game.state.score *= 2
            
            # Mark level as completed with the doubled score
            level_id = self.game.state.current_level_id
            self.game.state.complete_level(level_id, self.game.state.score)
            
            # Get rank
            rank = self.game.state.get_rank_for_score(self.game.state.score)
            
            # Show completion screen
            self.game.show_level_completion(self.game.state.score, rank, level_id)
        else:
            # Return to main menu after a delay if level wasn't completed
            pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 seconds delay
            
            # The event will be handled in the event handler