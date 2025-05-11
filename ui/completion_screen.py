"""
Level completion screen UI component.
"""
from typing import Any, Callable, Dict, List, Optional, Tuple

import pygame

from ui.aws_theme import AWSColors, AWSStyling
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
        self.title_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_XXLARGE, bold=True)
        self.heading_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_XLARGE, bold=True)
        self.text_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_LARGE)
        self.info_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_MEDIUM)
        
        # Calculate layout
        self.window_width = self.game.config.window.width
        self.window_height = self.game.config.window.height
        
        # Create buttons
        self._create_buttons()
        
        # Determine if next level is available
        self.next_level_available = (level_id < 10) and (level_id + 1 in self.game.state.unlocked_levels)
        
        # Animation state
        self.animation_progress = 0.0  # 0.0 to 1.0
        self.animation_speed = 0.05  # Progress per frame
        self.particles = []
        self._create_particles()
    
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
            callback=self._on_menu_click,
            style="secondary"
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
            callback=self._on_next_click,
            style="primary"
        )
        self.buttons.append(next_button)
        self.next_button = next_button
    
    def _create_particles(self) -> None:
        """Create celebration particles."""
        import random
        
        # Create particles based on rank
        particle_count = 50
        if self.rank == "Gold":
            particle_count = 100
            colors = [AWSColors.RIND, AWSColors.SMILE_ORANGE]
        elif self.rank == "Silver":
            colors = [(192, 192, 192), (150, 150, 150)]
        else:  # Bronze
            colors = [(205, 127, 50), (160, 100, 40)]
        
        # Create particles
        for _ in range(particle_count):
            self.particles.append({
                "x": self.window_width // 2,
                "y": self.window_height // 2,
                "vx": random.uniform(-5, 5),
                "vy": random.uniform(-8, -2),
                "radius": random.uniform(2, 6),
                "color": random.choice(colors),
                "life": random.uniform(0.5, 1.0)  # Life percentage (1.0 = full life)
            })
    
    def update(self) -> None:
        """Update the completion screen state."""
        # Update animation progress
        if self.animation_progress < 1.0:
            self.animation_progress += self.animation_speed
            if self.animation_progress > 1.0:
                self.animation_progress = 1.0
        
        # Update next level button state
        if not self.next_level_available:
            self.next_button.disabled = True
        
        # Update particles
        import random
        for particle in self.particles:
            # Apply gravity
            particle["vy"] += 0.1
            
            # Update position
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            
            # Update life
            particle["life"] -= 0.005
            
            # Respawn dead particles
            if particle["life"] <= 0:
                particle["x"] = self.window_width // 2
                particle["y"] = self.window_height // 2
                particle["vx"] = random.uniform(-5, 5)
                particle["vy"] = random.uniform(-8, -2)
                particle["life"] = random.uniform(0.5, 1.0)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the completion screen.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw background overlay with animation
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        alpha = int(180 * self.animation_progress)
        overlay.fill((0, 0, 0, alpha))  # Semi-transparent black
        surface.blit(overlay, (0, 0))
        
        # Draw completion panel with animation
        panel_width = 600
        panel_height = 400
        panel_rect = pygame.Rect(
            (self.window_width - panel_width) // 2,
            (self.window_height - panel_height) // 2 - int(50 * (1 - self.animation_progress)),
            panel_width,
            panel_height
        )
        
        # Draw panel background with gradient
        self._draw_gradient_panel(surface, panel_rect)
        
        # Draw particles
        for particle in self.particles:
            # Skip if not visible yet
            if self.animation_progress < 0.8:
                continue
                
            # Calculate alpha based on life
            alpha = int(255 * particle["life"])
            color_with_alpha = (*particle["color"], alpha)
            
            # Draw particle
            pygame.draw.circle(
                surface,
                color_with_alpha,
                (int(particle["x"]), int(particle["y"])),
                int(particle["radius"])
            )
        
        # Skip the rest if animation is not far enough
        if self.animation_progress < 0.3:
            return
        
        # Draw completion title with animation
        title_alpha = int(min(255, 255 * (self.animation_progress - 0.3) / 0.2))
        self._render_text_with_alpha(
            surface,
            "Level Complete!",
            self.title_font,
            AWSColors.SMILE_ORANGE,
            self.window_width // 2,
            panel_rect.top + 40,
            title_alpha
        )
        
        # Skip the rest if animation is not far enough
        if self.animation_progress < 0.5:
            return
        
        # Draw level info with animation
        level_alpha = int(min(255, 255 * (self.animation_progress - 0.5) / 0.2))
        self._render_text_with_alpha(
            surface,
            f"Level {self.level_id}",
            self.heading_font,
            AWSColors.WHITE,
            self.window_width // 2,
            panel_rect.top + 100,
            level_alpha
        )
        
        # Draw score with animation
        score_alpha = int(min(255, 255 * (self.animation_progress - 0.6) / 0.2))
        self._render_text_with_alpha(
            surface,
            f"Score: {self.score}",
            self.text_font,
            AWSColors.WHITE,
            self.window_width // 2,
            panel_rect.top + 150,
            score_alpha
        )
        
        # Draw rank with color based on rank and animation
        rank_alpha = int(min(255, 255 * (self.animation_progress - 0.7) / 0.2))
        rank_color = AWSColors.WHITE
        if self.rank == "Gold":
            rank_color = AWSColors.RIND
        elif self.rank == "Silver":
            rank_color = (192, 192, 192)  # Silver color
        elif self.rank == "Bronze":
            rank_color = (205, 127, 50)  # Bronze color
            
        self._render_text_with_alpha(
            surface,
            f"{self.rank} Architect",
            self.heading_font,
            rank_color,
            self.window_width // 2,
            panel_rect.top + 200,
            rank_alpha
        )
        
        # Draw congratulatory message with animation
        message_alpha = int(min(255, 255 * (self.animation_progress - 0.8) / 0.2))
        if self.rank == "Gold":
            message = "Outstanding work! You've achieved the highest rank!"
        elif self.rank == "Silver":
            message = "Great job! Can you optimize further for Gold?"
        else:
            message = "Good start! Try optimizing your solution for a higher rank."
            
        self._render_text_with_alpha(
            surface,
            message,
            self.info_font,
            AWSColors.WHITE,
            self.window_width // 2,
            panel_rect.top + 250,
            message_alpha
        )
        
        # Draw buttons with animation
        if self.animation_progress > 0.9:
            for button in self.buttons:
                button.render(surface)
    
    def _draw_gradient_panel(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Draw a gradient panel.
        
        Args:
            surface: Pygame surface to render on
            rect: Rectangle defining the panel position and size
        """
        # Create a surface for the gradient
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Define gradient colors
        top_color = AWSColors.SQUID_INK
        bottom_color = (top_color[0] + 20, top_color[1] + 20, top_color[2] + 20)
        
        # Draw gradient
        for y in range(rect.height):
            # Calculate color for this line
            ratio = y / rect.height
            color = (
                int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
                int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
                int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio),
                int(220 * self.animation_progress)  # Alpha based on animation
            )
            pygame.draw.line(panel, color, (0, y), (rect.width, y))
        
        # Draw the panel
        surface.blit(panel, rect)
        
        # Draw border
        border_alpha = int(255 * self.animation_progress)
        border_color = (*AWSColors.SMILE_ORANGE, border_alpha)
        pygame.draw.rect(
            surface, 
            border_color, 
            rect, 
            2, 
            border_radius=AWSStyling.BORDER_RADIUS_LARGE
        )
    
    def _render_text_with_alpha(
        self,
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        color: Tuple[int, int, int],
        x: int,
        y: int,
        alpha: int
    ) -> None:
        """
        Render text with alpha transparency.
        
        Args:
            surface: Pygame surface to render on
            text: Text to render
            font: Font to use
            color: Text color (RGB)
            x: X position (center)
            y: Y position (top)
            alpha: Alpha value (0-255)
        """
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(centerx=x, top=y)
        surface.blit(text_surface, text_rect)
    
    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Only handle events if animation is complete
        if self.animation_progress < 1.0:
            return False
            
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