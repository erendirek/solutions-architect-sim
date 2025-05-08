"""
Message box UI component.
"""
from typing import Callable, Optional, Tuple

import pygame


class MessageBox:
    """Message box UI component for displaying messages to the user."""
    
    def __init__(
        self,
        message: str,
        rect: pygame.Rect,
        bg_color: Tuple[int, int, int] = (240, 240, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        border_color: Tuple[int, int, int] = (100, 100, 200),
        timeout: Optional[int] = 180  # 3 seconds at 60 FPS
    ) -> None:
        """
        Initialize a message box.
        
        Args:
            message: Message to display
            rect: Rectangle defining the message box's position and size
            bg_color: Background color (RGB)
            text_color: Text color (RGB)
            border_color: Border color (RGB)
            timeout: Frames until the message box disappears (None for no timeout)
        """
        self.message = message
        self.rect = rect
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.timeout = timeout
        self.active = True
        
        # Create font
        self.font = pygame.font.SysFont("Arial", 16)
        
        # Wrap text to fit in the message box
        self.wrapped_text = self._wrap_text(message, rect.width - 20)
    
    def _wrap_text(self, text: str, max_width: int) -> list:
        """
        Wrap text to fit within a given width.
        
        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            
        Returns:
            List of wrapped text lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # If the word is too long for a single line, force it
                    lines.append(word)
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def update(self) -> None:
        """Update the message box state."""
        if self.timeout is not None:
            self.timeout -= 1
            if self.timeout <= 0:
                self.active = False
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the message box.
        
        Args:
            surface: Pygame surface to render on
        """
        if not self.active:
            return
            
        # Draw message box background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw text
        y = self.rect.top + 20
        for line in self.wrapped_text:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(centerx=self.rect.centerx, top=y)
            surface.blit(text_surface, text_rect)
            y += text_surface.get_height() + 5
        
        # Draw close button or "Click to continue" text
        if self.timeout is None:
            close_text = self.font.render("Click to continue", True, self.text_color)
            close_rect = close_text.get_rect(
                centerx=self.rect.centerx,
                bottom=self.rect.bottom - 15
            )
            surface.blit(close_text, close_rect)
    
    def on_click(self) -> None:
        """Handle click on the message box."""
        self.active = False