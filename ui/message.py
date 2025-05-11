"""
Message UI component.
"""
from typing import Optional, Tuple

import pygame

from ui.aws_theme import AWSColors, AWSStyling


class Message:
    """Message UI component for displaying temporary messages."""
    
    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        font: Optional[pygame.font.Font] = None,
        color: Tuple[int, int, int] = AWSColors.WHITE,
        bg_color: Tuple[int, int, int] = AWSColors.SQUID_INK,
        duration: int = 3000  # milliseconds
    ) -> None:
        """
        Initialize a message.
        
        Args:
            text: Message text
            position: Position (x, y) of the message center
            font: Font to use for the message text
            color: Text color (RGB)
            bg_color: Background color (RGB)
            duration: Duration to display the message in milliseconds
        """
        self.text = text
        self.position = position
        self.color = color
        self.bg_color = bg_color
        self.duration = duration
        self.creation_time = pygame.time.get_ticks()
        self.alpha = 255  # Full opacity
        
        # Create font if not provided
        if font is None:
            self.font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_MEDIUM)
        else:
            self.font = font
        
        # Create text surface
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=position)
        
        # Create background rectangle
        padding = AWSStyling.PADDING_MEDIUM
        self.bg_rect = pygame.Rect(
            self.text_rect.left - padding,
            self.text_rect.top - padding,
            self.text_rect.width + padding * 2,
            self.text_rect.height + padding * 2
        )
        
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the message.
        
        Args:
            surface: Pygame surface to render on
        """
        # Calculate time elapsed since creation
        elapsed = pygame.time.get_ticks() - self.creation_time
        
        # Fade out during the last second
        if elapsed > self.duration - 1000:
            self.alpha = max(0, int(255 * (1 - (elapsed - (self.duration - 1000)) / 1000)))
        
        # Create a surface with alpha channel for the background
        bg_surface = pygame.Surface((self.bg_rect.width, self.bg_rect.height), pygame.SRCALPHA)
        bg_color_with_alpha = (*self.bg_color, self.alpha)
        pygame.draw.rect(
            bg_surface, 
            bg_color_with_alpha, 
            bg_surface.get_rect(),
            border_radius=AWSStyling.BORDER_RADIUS_MEDIUM
        )
        
        # Draw orange border
        border_color = (*AWSColors.SMILE_ORANGE, self.alpha)
        pygame.draw.rect(
            bg_surface, 
            border_color, 
            bg_surface.get_rect(),
            width=2,
            border_radius=AWSStyling.BORDER_RADIUS_MEDIUM
        )
        
        # Blit background
        surface.blit(bg_surface, self.bg_rect)
        
        # Create a surface with alpha channel for the text
        text_surface_alpha = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)
        text_surface_alpha.fill((0, 0, 0, 0))  # Transparent
        text_surface_alpha.blit(self.text_surface, (0, 0))
        text_surface_alpha.set_alpha(self.alpha)
        
        # Blit text
        surface.blit(text_surface_alpha, self.text_rect)