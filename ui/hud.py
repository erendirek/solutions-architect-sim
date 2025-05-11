"""
HUD (Heads-Up Display) UI component.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame

from ui.aws_theme import AWSColors, AWSStyling


class HUD:
    """HUD UI component for displaying game information."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the HUD.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.rect = pygame.Rect(
            0,
            game.config.window.height - game.config.ui.hud_height,
            game.config.window.width,
            game.config.ui.hud_height
        )
        
        # Create fonts
        self.title_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_MEDIUM, bold=True)
        self.info_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_NORMAL)
        self.icon_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_SMALL)
        
        # Create metric icons
        self.score_icon = "🏆"
        self.budget_icon = "💰"
        self.latency_icon = "⚡"
        self.time_icon = "⏱️"
    
    def update(self) -> None:
        """Update the HUD state."""
        # Update time remaining in time trial mode
        from core.state import GameMode
        if self.game.state.mode == GameMode.TIME_TRIAL and self.game.state.time_remaining is not None:
            # Check if time has run out
            if self.game.state.time_remaining <= 0 and not self.game.time_manager.time_out:
                self.game.time_manager.time_out = True
                self.game.time_manager._handle_time_out()
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the HUD.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw HUD background with gradient effect
        self._draw_gradient_background(surface)
        
        # Draw level information
        if self.game.level_manager.current_level:
            level = self.game.level_manager.current_level
            
            # Draw level title
            title_text = self.title_font.render(
                f"Level {level.level_id}: {level.title}",
                True,
                AWSColors.WHITE
            )
            title_shadow = self.title_font.render(
                f"Level {level.level_id}: {level.title}",
                True,
                AWSColors.SQUID_INK
            )
            
            # Draw shadow effect
            surface.blit(title_shadow, (22, self.rect.top + 12))
            surface.blit(title_text, (20, self.rect.top + 10))
            
            # Get metrics
            from tests.cost_estimator import CostEstimator
            from tests.performance_test import PerformanceTest
            
            estimated_cost = CostEstimator.estimate_monthly_cost(
                self.game.state.placed_services,
                self.game.state.connections,
                level.level_id
            )
            
            estimated_latency = PerformanceTest.estimate_latency(
                self.game.state.placed_services,
                self.game.state.connections,
                level.level_id
            )
            
            # Create metric cards
            self._draw_metric_card(
                surface, 
                self.score_icon,
                "Score", 
                f"{self.game.state.score}", 
                20, 
                self.rect.top + 45,
                AWSColors.RIND
            )
            
            budget_color = AWSColors.SUCCESS if estimated_cost <= level.budget else AWSColors.ERROR
            self._draw_metric_card(
                surface, 
                self.budget_icon,
                "Budget", 
                f"${estimated_cost:.2f} / ${level.budget:.2f}", 
                200, 
                self.rect.top + 45,
                budget_color
            )
            
            latency_color = AWSColors.SUCCESS if estimated_latency <= level.max_latency else AWSColors.ERROR
            self._draw_metric_card(
                surface, 
                self.latency_icon,
                "Latency", 
                f"{estimated_latency:.2f}ms / {level.max_latency:.2f}ms", 
                400, 
                self.rect.top + 45,
                latency_color
            )
            
            # Draw time remaining if in time trial mode
            from core.state import GameMode
            if self.game.state.mode == GameMode.TIME_TRIAL and self.game.state.time_remaining is not None:
                minutes = int(self.game.state.time_remaining // 60)
                seconds = int(self.game.state.time_remaining % 60)
                
                time_color = AWSColors.SUCCESS if self.game.state.time_remaining > 30 else AWSColors.ERROR
                self._draw_metric_card(
                    surface, 
                    self.time_icon,
                    "Time", 
                    f"{minutes:02d}:{seconds:02d}", 
                    600, 
                    self.rect.top + 45,
                    time_color
                )
    
    def _draw_gradient_background(self, surface: pygame.Surface) -> None:
        """Draw a gradient background for the HUD."""
        # Create a surface for the gradient
        gradient = pygame.Surface((self.rect.width, self.rect.height))
        
        # Define gradient colors
        top_color = AWSColors.SQUID_INK
        bottom_color = (top_color[0] + 15, top_color[1] + 15, top_color[2] + 15)
        
        # Draw gradient
        for y in range(self.rect.height):
            # Calculate color for this line
            ratio = y / self.rect.height
            color = (
                int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
                int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
                int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            )
            pygame.draw.line(gradient, color, (0, y), (self.rect.width, y))
        
        # Draw the gradient surface
        surface.blit(gradient, self.rect)
        
        # Draw top border
        pygame.draw.line(
            surface, 
            AWSColors.SMILE_ORANGE, 
            (0, self.rect.top), 
            (self.rect.right, self.rect.top), 
            2
        )
    
    def _draw_metric_card(
        self, 
        surface: pygame.Surface, 
        icon: str,
        label: str, 
        value: str, 
        x: int, 
        y: int,
        value_color: Tuple[int, int, int]
    ) -> None:
        """Draw a metric card with icon, label and value."""
        # Draw icon
        icon_text = self.icon_font.render(icon, True, AWSColors.WHITE)
        surface.blit(icon_text, (x, y))
        
        # Draw label
        label_text = self.info_font.render(label, True, AWSColors.MEDIUM_GRAY)
        surface.blit(label_text, (x + 25, y))
        
        # Draw value
        value_text = self.info_font.render(value, True, value_color)
        surface.blit(value_text, (x + 25, y + 20))