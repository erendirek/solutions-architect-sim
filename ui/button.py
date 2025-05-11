"""
Button UI component.
"""
from typing import Callable, Optional, Tuple

import pygame

from ui.aws_theme import AWSColors, AWSStyling


class Button:
    """Interactive button UI component."""
    
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Callable[[], None],
        bg_color: Optional[Tuple[int, int, int]] = None,
        hover_color: Optional[Tuple[int, int, int]] = None,
        text_color: Optional[Tuple[int, int, int]] = None,
        style: str = "primary",
        disabled: bool = False
    ) -> None:
        """
        Initialize a button.
        
        Args:
            rect: Rectangle defining the button's position and size
            text: Text to display on the button
            callback: Function to call when the button is clicked
            bg_color: Background color (RGB), overrides style if provided
            hover_color: Background color when hovered (RGB), overrides style if provided
            text_color: Text color (RGB), overrides style if provided
            style: Button style ("primary", "secondary", "danger", "success")
            disabled: Whether the button is disabled
        """
        self.rect = rect
        self.text = text
        self.callback = callback
        self.style = style
        self.disabled = disabled
        self.is_hovered = False
        
        # Set colors based on style
        if bg_color is not None:
            self.bg_color = bg_color
        elif style == "primary":
            self.bg_color = AWSColors.BUTTON_PRIMARY
        elif style == "secondary":
            self.bg_color = AWSColors.BUTTON_SECONDARY
        elif style == "danger":
            self.bg_color = AWSColors.ERROR
        elif style == "success":
            self.bg_color = AWSColors.SUCCESS
        else:
            self.bg_color = AWSColors.BUTTON_PRIMARY
            
        if hover_color is not None:
            self.hover_color = hover_color
        elif style == "primary":
            self.hover_color = AWSColors.BUTTON_PRIMARY_HOVER
        elif style == "secondary":
            self.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
        elif style == "danger":
            self.hover_color = (184, 46, 46)  # Darker red
        elif style == "success":
            self.hover_color = (48, 155, 68)  # Darker green
        else:
            self.hover_color = AWSColors.BUTTON_PRIMARY_HOVER
            
        if text_color is not None:
            self.text_color = text_color
        else:
            self.text_color = AWSColors.WHITE
            
        # Override colors if disabled
        if disabled:
            self.bg_color = AWSColors.BUTTON_DISABLED
            self.hover_color = AWSColors.BUTTON_DISABLED
            self.text_color = AWSColors.DARK_GRAY
        
        # Create font
        self.font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_NORMAL)
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the button.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw button background with rounded corners
        color = self.hover_color if self.is_hovered and not self.disabled else self.bg_color
        
        # Draw rounded rectangle
        border_radius = min(AWSStyling.BORDER_RADIUS_MEDIUM, self.rect.height // 2)
        pygame.draw.rect(surface, color, self.rect, border_radius=border_radius)
        
        # Draw border with slightly thicker line for better visibility
        border_color = AWSColors.DARK_GRAY if not self.disabled else AWSColors.MEDIUM_GRAY
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=border_radius)
        
        # Update text surface if text has changed
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
    
    def on_click(self) -> None:
        """Handle button click."""
        if self.callback and not self.disabled:
            self.callback()