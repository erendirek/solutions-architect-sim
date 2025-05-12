"""
Core game module that manages the main game loop and state.
"""
from typing import Dict, List, Optional, Tuple, Any
import pygame

from core.config import GameConfig
from core.state import GameState, GameMode
from core.event_handler import EventHandler
from core.level_manager import LevelManager
from core.time_manager import TimeManager
from ui.ui_manager import UIManager
from ui.main_menu import MainMenu
from ui.aws_theme import AWSColors


class Game:
    """Main game class that manages the game loop and state."""
    
    def __init__(self, config: GameConfig) -> None:
        """
        Initialize the game with configuration.
        
        Args:
            config: Game configuration object
        """
        self.config = config
        self.screen = pygame.display.set_mode(
            (config.window.width, config.window.height)
        )
        pygame.display.set_caption(config.window.title)
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Initialize game state
        self.state = GameState()
        
        # Initialize managers
        self.event_handler = EventHandler(self)
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self)
        self.time_manager = TimeManager(self)
        
        # Initialize main menu
        self.main_menu = MainMenu(self)
        self.show_main_menu = True
        
        # Initialize completion screen
        self.completion_screen = None
        self.show_completion_screen = False
        
    def run(self) -> None:
        """Run the main game loop."""
        self.running = True
        
        while self.running:
            # Handle events
            self.event_handler.process_events()
            
            # Update game state
            self.update()
            
            # Render the game
            self.render()
            
            # Cap the frame rate
            self.clock.tick(self.config.window.fps)
    
    def update(self) -> None:
        """Update the game state."""
        if self.show_main_menu:
            # Update main menu
            self.main_menu.update()
            
            # Check if main menu is closed
            if not self.main_menu.active:
                self.show_main_menu = False
        elif self.show_completion_screen and self.completion_screen:
            # Update completion screen
            self.completion_screen.update()
            
            # Check if completion screen is closed
            if not self.completion_screen.active:
                self.show_completion_screen = False
                self.completion_screen = None
        else:
            # Update the current level
            self.level_manager.update()
            
            # Update time manager
            self.time_manager.update()
            
            # Update UI components
            self.ui_manager.update()
    
    def render(self) -> None:
        """Render the game to the screen."""
        # Clear the screen
        self.screen.fill((25, 35, 50))  # Daha koyu arka plan - AWSColors.SQUID_INK
        
        if self.show_main_menu:
            # Render main menu
            self.main_menu.render(self.screen)
        else:
            # Render the current level
            self.level_manager.render(self.screen)
            
            # Render UI components
            self.ui_manager.render(self.screen)
            
            # Render completion screen on top if active
            if self.show_completion_screen and self.completion_screen:
                self.completion_screen.render(self.screen)
        
        # Show FPS if debug is enabled
        if self.config.debug.show_fps:
            fps = int(self.clock.get_fps())
            font = pygame.font.SysFont("Arial", 18)
            fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
            self.screen.blit(fps_text, (10, 10))
        
        # Update the display
        pygame.display.flip()
    
    def show_menu(self) -> None:
        """Show the main menu."""
        self.show_main_menu = True
        self.main_menu.active = True
        self.show_completion_screen = False
        self.completion_screen = None
        
        # Refresh main menu button states to ensure completed levels are properly shown
        if hasattr(self.main_menu, 'level_buttons'):
            for i, button in enumerate(self.main_menu.level_buttons):
                level_id = i + 1
                is_unlocked = level_id in self.state.unlocked_levels
                is_completed = level_id in self.state.completed_levels
                is_selected = level_id == self.main_menu.selected_level
                
                # Update button state
                button.disabled = not is_unlocked
                
                # Set button style based on status
                if is_selected:
                    button.bg_color = AWSColors.SMILE_ORANGE
                    button.hover_color = (230, 138, 0)  # Darker orange
                elif is_completed:
                    button.bg_color = AWSColors.SUCCESS
                    button.hover_color = (48, 155, 68)  # Darker green
                elif is_unlocked:
                    button.bg_color = AWSColors.BUTTON_SECONDARY
                    button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
                else:
                    button.bg_color = AWSColors.BUTTON_DISABLED
                    button.hover_color = AWSColors.BUTTON_DISABLED
    
    def show_level_completion(self, score: int, rank: str, level_id: int) -> None:
        """
        Show the level completion screen.
        
        Args:
            score: Score achieved in the level
            rank: Rank achieved (Bronze, Silver, Gold)
            level_id: ID of the completed level
        """
        from ui.completion_screen import CompletionScreen
        self.completion_screen = CompletionScreen(self, score, rank, level_id)
        self.show_completion_screen = True
    
    def quit(self) -> None:
        """Quit the game."""
        self.running = False