"""
Level completion screen UI component.
"""
from typing import Any, Callable, Dict, List, Optional, Tuple

import pygame

from ui.button import Button


class CompletionScreen:
    """Level completion screen UI component."""
    
    def __init__(self, game: Any, score: int, rank: str, level_id: int) -> None:
        """
        Initialize the completion screen.
        
        Args:
            game: Reference to the main game object
            score: Score achieved in the level
            rank: Rank achieved (Bronze, Silver, Gold)
            level_id: ID of the completed level
        """
        self.game = game
        self.score = score
        self.rank = rank
        self.level_id = level_id
        self.active = True
        
        # Create fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 24)
        self.info_font = pygame.font.SysFont("Arial", 20)
        
        # Calculate layout
        self.window_width = self.game.config.window.width
        self.window_height = self.game.config.window.height
        
        # Create buttons
        self._create_buttons()
        
        # Determine if next level is available
        self.next_level_available = (level_id < 10) and (level_id + 1 in self.game.state.unlocked_levels)
    
    def _create_buttons(self) -> None:
        """Create UI buttons for the completion screen."""
        self.buttons = []
        
        # Main menu button
        menu_button = Button(
            rect=pygame.Rect(
                self.window_width // 2 - 200,
                self.window_height - 120,
                180,
                50
            ),
            text="Main Menu",
            callback=self._on_menu_click
        )
        self.buttons.append(menu_button)
        
        # Next level button (if available)
        next_button = Button(
            rect=pygame.Rect(
                self.window_width // 2 + 20,
                self.window_height - 120,
                180,
                50
            ),
            text="Next Level",
            callback=self._on_next_click
        )
        self.buttons.append(next_button)
        self.next_button = next_button
    
    def update(self) -> None:
        """Update the completion screen state."""
        # Update next level button state
        if not self.next_level_available:
            self.next_button.bg_color = (150, 150, 150)  # Gray for disabled
        else:
            self.next_button.bg_color = (100, 100, 240)  # Blue for enabled
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the completion screen.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw background overlay
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        surface.blit(overlay, (0, 0))
        
        # Draw completion panel
        panel_width = 600
        panel_height = 400
        panel_rect = pygame.Rect(
            (self.window_width - panel_width) // 2,
            (self.window_height - panel_height) // 2,
            panel_width,
            panel_height
        )
        pygame.draw.rect(surface, (240, 240, 240), panel_rect)
        pygame.draw.rect(surface, (100, 100, 100), panel_rect, 2)
        
        # Draw completion title
        title_text = self.title_font.render("Level Complete!", True, (0, 0, 0))
        title_rect = title_text.get_rect(centerx=self.window_width // 2, top=panel_rect.top + 30)
        surface.blit(title_text, title_rect)
        
        # Draw level info
        level_text = self.heading_font.render(f"Level {self.level_id}", True, (0, 0, 0))
        level_rect = level_text.get_rect(centerx=self.window_width // 2, top=title_rect.bottom + 30)
        surface.blit(level_text, level_rect)
        
        # Draw score
        score_text = self.text_font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(centerx=self.window_width // 2, top=level_rect.bottom + 30)
        surface.blit(score_text, score_rect)
        
        # Draw rank with color based on rank
        rank_color = (0, 0, 0)
        if self.rank == "Gold":
            rank_color = (212, 175, 55)  # Gold color
        elif self.rank == "Silver":
            rank_color = (192, 192, 192)  # Silver color
        elif self.rank == "Bronze":
            rank_color = (205, 127, 50)  # Bronze color
            
        rank_text = self.heading_font.render(f"{self.rank} Architect", True, rank_color)
        rank_rect = rank_text.get_rect(centerx=self.window_width // 2, top=score_rect.bottom + 20)
        surface.blit(rank_text, rank_rect)
        
        # Draw congratulatory message
        if self.rank == "Gold":
            message = "Outstanding work! You've achieved the highest rank!"
        elif self.rank == "Silver":
            message = "Great job! Can you optimize further for Gold?"
        else:
            message = "Good start! Try optimizing your solution for a higher rank."
            
        message_text = self.info_font.render(message, True, (0, 0, 0))
        message_rect = message_text.get_rect(centerx=self.window_width // 2, top=rank_rect.bottom + 20)
        surface.blit(message_text, message_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.render(surface)
    
    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Check button clicks
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                if button == self.next_button and not self.next_level_available:
                    # Skip disabled next button
                    continue
                button.on_click()
                return True
        
        return False
    
    def handle_mouse_up(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button up events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # No specific handling for mouse up events
        return False
    
    def handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """
        Handle mouse motion events.
        
        Args:
            event: Pygame mouse motion event
        """
        # Update button hover states
        for button in self.buttons:
            button.is_hovered = button.rect.collidepoint(event.pos)
    
    def _on_menu_click(self) -> None:
        """Handle click on the main menu button."""
        self.active = False
        self.game.show_menu()
    
    def _on_next_click(self) -> None:
        """Handle click on the next level button."""
        if self.next_level_available:
            self.active = False
            self.game.level_manager.load_level(self.level_id + 1)