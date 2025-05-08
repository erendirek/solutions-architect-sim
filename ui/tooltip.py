"""
Tooltip UI component.
"""
from typing import List, Tuple

import pygame


class Tooltip:
    """Tooltip UI component for displaying additional information."""
    
    def __init__(
        self,
        position: Tuple[int, int],
        content: List[str],
        bg_color: Tuple[int, int, int] = (255, 255, 220),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        border_color: Tuple[int, int, int] = (100, 100, 100),
        padding: int = 10,
        max_width: int = 300
    ) -> None:
        """
        Initialize a tooltip.
        
        Args:
            position: Position (x, y) to show the tooltip at
            content: List of text lines to display
            bg_color: Background color (RGB)
            text_color: Text color (RGB)
            border_color: Border color (RGB)
            padding: Padding around the content
            max_width: Maximum width of the tooltip
        """
        self.position = position
        self.content = content
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.padding = padding
        self.max_width = max_width
        
        # Create font
        self.font = pygame.font.SysFont("Arial", 14)
        
        # Create text surfaces
        self.text_surfaces = [
            self.font.render(line, True, text_color) for line in content
        ]
        
        # Calculate tooltip dimensions
        width = min(
            max(surface.get_width() for surface in self.text_surfaces) + padding * 2,
            max_width
        )
        height = sum(surface.get_height() for surface in self.text_surfaces) + padding * 2
        
        # Create tooltip rectangle
        self.rect = pygame.Rect(position[0], position[1], width, height)
        
        # Adjust position to keep tooltip on screen
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if self.rect.right > screen_width:
            self.rect.right = screen_width - 5
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height - 5
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the tooltip.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw tooltip background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 1)
        
        # Draw text
        y = self.rect.top + self.padding
        for text_surface in self.text_surfaces:
            x = self.rect.left + self.padding
            surface.blit(text_surface, (x, y))
            y += text_surface.get_height()