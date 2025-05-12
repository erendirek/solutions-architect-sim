"""
Level 2: Static Portfolio Site with CloudFront.
"""
from typing import Any, Dict, List, Optional, Set, Tuple

import pygame

from levels.base_level import BaseLevel
from services.service_registry import ServiceRegistry


class Level2(BaseLevel):
    """Level 2: Static Portfolio Site with CloudFront."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize Level 2.
        
        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        
        # Load level data from levels.json
        if not self.load_level_data(2):
            # Fallback to hardcoded values if loading fails
            self.level_id = 2
            self.title = "Static Portfolio Site"
            self.description = (
                "Build a static portfolio website with global content delivery for fast access worldwide."
            )
            self.objective = (
                "Create an architecture using S3 for static content hosting and CloudFront "
                "for global content delivery."
            )
            
            # Level requirements
            self.required_services = {
                "s3", "cloudfront"
            }
            self.optional_services = {
                "waf", "lambda"
            }
            self.available_services = {
                "s3", "cloudfront", "waf", "lambda", "route53", "api_gateway"
            }
            self.budget = 30.0  # Monthly cost in USD
            self.max_latency = 100.0  # in ms
            
            # Tutorial steps
            self.tutorial_steps = [
                "First, create an S3 bucket to store your static website files.",
                "Next, add CloudFront to distribute your content globally.",
                "Connect CloudFront to the S3 bucket.",
                "Consider adding WAF for additional security (optional).",
                "Validate your architecture to complete the level."
            ]
        
        # Load service icons
        self._load_service_icons()
    
    def _load_service_icons(self) -> None:
        """Load service icons for the available services."""
        self.service_icons = {}
        self.service_rects = {}
        
        # Panel layout
        panel_width = self.game.config.ui.service_panel_width
        icon_size = 64
        padding = 10
        icons_per_row = 2
        
        for i, service_id in enumerate(sorted(self.available_services)):
            service_info = ServiceRegistry.get_service(service_id)
            if service_info:
                # Load icon
                icon = pygame.image.load(service_info.icon_path)
                icon = pygame.transform.scale(icon, (icon_size, icon_size))
                self.service_icons[service_id] = icon
                
                # Calculate position
                row = i // icons_per_row
                col = i % icons_per_row
                x = padding + col * (icon_size + padding)
                y = padding + row * (icon_size + padding + 20)  # Extra space for text
                
                # Create rect for collision detection
                self.service_rects[service_id] = pygame.Rect(x, y, icon_size, icon_size)
    
    def update(self) -> None:
        """Update the level state."""
        # Call parent update to handle connection animations
        super().update()
        
        # Check if we should advance the tutorial step
        if self.game.state.mode.name == "TUTORIAL":
            if self.current_tutorial_step < len(self.tutorial_steps) - 1:
                # Check conditions to advance to next step
                if self.current_tutorial_step == 0 and "s3" in self.game.state.placed_services:
                    self.current_tutorial_step = 1
                elif self.current_tutorial_step == 1 and "cloudfront" in self.game.state.placed_services:
                    self.current_tutorial_step = 2
                elif self.current_tutorial_step == 2 and any(
                    conn == ("cloudfront", "s3") for conn in self.game.state.connections
                ):
                    self.current_tutorial_step = 3
                elif self.current_tutorial_step == 3 and "waf" in self.game.state.placed_services:
                    self.current_tutorial_step = 4
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the level.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw service panel background
        panel_rect = pygame.Rect(0, 0, self.game.config.ui.service_panel_width, self.game.config.window.height - self.game.config.ui.hud_height)
        pygame.draw.rect(surface, (220, 220, 220), panel_rect)
        pygame.draw.line(surface, (180, 180, 180), (panel_rect.right, 0), (panel_rect.right, panel_rect.bottom), 2)
        
        # Draw service icons in panel
        font = pygame.font.SysFont("Arial", 12)
        for service_id, rect in self.service_rects.items():
            # Draw icon
            surface.blit(self.service_icons[service_id], rect)
            
            # Draw service name
            service_info = ServiceRegistry.get_service(service_id)
            if service_info:
                text = font.render(service_info.display_name, True, (0, 0, 0))
                text_rect = text.get_rect(centerx=rect.centerx, top=rect.bottom + 2)
                surface.blit(text, text_rect)
        
        # Draw canvas background
        pygame.draw.rect(surface, (255, 255, 255), self.canvas_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.canvas_rect, 2)
        
        # Draw placed services on canvas
        for node in self.placed_service_nodes:
            node.render(surface)
        
        # Draw connections with animated styling
        self.connection_animator.render(surface, self.connections)
        
        # Draw tutorial step if in tutorial mode
        if self.game.state.mode.name == "TUTORIAL" and self.current_tutorial_step < len(self.tutorial_steps):
            tutorial_font = pygame.font.SysFont("Arial", 16)
            tutorial_text = tutorial_font.render(
                self.tutorial_steps[self.current_tutorial_step],
                True,
                (0, 0, 0)
            )
            tutorial_rect = tutorial_text.get_rect(
                centerx=self.canvas_rect.centerx,
                bottom=self.canvas_rect.bottom - 10
            )
            
            # Draw background for tutorial text
            bg_rect = tutorial_rect.inflate(20, 10)
            pygame.draw.rect(surface, (255, 255, 200), bg_rect)
            pygame.draw.rect(surface, (200, 200, 150), bg_rect, 2)
            
            surface.blit(tutorial_text, tutorial_rect)
    
    def get_service_at_panel(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Get the service at the given position in the service panel.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            Service ID if found, None otherwise
        """
        for service_id, rect in self.service_rects.items():
            if rect.collidepoint(pos):
                return service_id
        return None