"""
Button UI component.
"""
from typing import Callable, Optional, Tuple

import pygame


class Button:
    """Interactive button UI component."""
    
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Callable[[], None],
        bg_color: Tuple[int, int, int] = (100, 100, 240),
        hover_color: Tuple[int, int, int] = (130, 130, 255),
        text_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> None:
        """
        Initialize a button.
        
        Args:
            rect: Rectangle defining the button's position and size
            text: Text to display on the button
            callback: Function to call when the button is clicked
            bg_color: Background color (RGB)
            hover_color: Background color when hovered (RGB)
            text_color: Text color (RGB)
        """
        self.rect = rect
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
        # Create font
        self.font = pygame.font.SysFont("Arial", 16)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the button.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw button background
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (50, 50, 50), self.rect, 2)  # Border
        
        # Update text surface if text has changed
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
    
    def on_click(self) -> None:
        """Handle button click."""
        if self.callback:
            self.callback()