"""
HUD (Heads-Up Display) UI component.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame


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
        self.title_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 16)
    
    def update(self) -> None:
        """Update the HUD state."""
        # No dynamic updates needed for now
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the HUD.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw HUD background
        pygame.draw.rect(surface, (220, 220, 220), self.rect)
        pygame.draw.line(surface, (180, 180, 180), (0, self.rect.top), (self.rect.right, self.rect.top), 2)
        
        # Draw level information
        if self.game.level_manager.current_level:
            level = self.game.level_manager.current_level
            
            # Draw level title
            title_text = self.title_font.render(
                f"Level {level.level_id}: {level.title}",
                True,
                (0, 0, 0)
            )
            surface.blit(title_text, (20, self.rect.top + 10))
            
            # Draw score
            score_text = self.info_font.render(
                f"Score: {self.game.state.score}",
                True,
                (0, 0, 0)
            )
            surface.blit(score_text, (20, self.rect.top + 35))
            
            # Draw budget information
            from tests.cost_estimator import CostEstimator
            
            estimated_cost = CostEstimator.estimate_monthly_cost(
                self.game.state.placed_services,
                self.game.state.connections,
                level.level_id
            )
            
            budget_text = self.info_font.render(
                f"Budget: ${estimated_cost:.2f} / ${level.budget:.2f}",
                True,
                (0, 0, 0) if estimated_cost <= level.budget else (200, 0, 0)
            )
            surface.blit(budget_text, (200, self.rect.top + 35))
            
            # Draw latency information
            from tests.performance_test import PerformanceTest
            
            estimated_latency = PerformanceTest.estimate_latency(
                self.game.state.placed_services,
                self.game.state.connections,
                level.level_id
            )
            
            latency_text = self.info_font.render(
                f"Latency: {estimated_latency:.2f}ms / {level.max_latency:.2f}ms",
                True,
                (0, 0, 0) if estimated_latency <= level.max_latency else (200, 0, 0)
            )
            surface.blit(latency_text, (400, self.rect.top + 35))
            
            # Draw time remaining if in time trial mode
            if self.game.state.time_remaining is not None:
                minutes = self.game.state.time_remaining // 60
                seconds = self.game.state.time_remaining % 60
                
                time_text = self.info_font.render(
                    f"Time: {minutes:02d}:{seconds:02d}",
                    True,
                    (0, 0, 0) if self.game.state.time_remaining > 30 else (200, 0, 0)
                )
                surface.blit(time_text, (600, self.rect.top + 35))