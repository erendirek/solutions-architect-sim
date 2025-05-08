"""
Level 1: Build a blog API and store posts.
"""
from typing import Any, Dict, List, Optional, Set, Tuple

import pygame

from levels.base_level import BaseLevel
from services.service_registry import ServiceRegistry


class Level1(BaseLevel):
    """Level 1: Simple CRUD web API tutorial."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize Level 1.
        
        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        
        # Load level data from levels.json
        if not self.load_level_data(1):
            # Fallback to hardcoded values if loading fails
            self.level_id = 1
            self.title = "Build a Blog API"
            self.description = (
                "Create a simple blog API that allows users to create, read, update, "
                "and delete blog posts. The API should store post content in DynamoDB "
                "and media files in S3."
            )
            self.objective = (
                "Build a serverless architecture using API Gateway, Lambda, "
                "DynamoDB, and S3 to create a functional blog API."
            )
            
            # Level requirements
            self.required_services = {
                "api_gateway", "lambda", "dynamodb", "s3"
            }
            self.optional_services = {
                "iam", "cloudwatch"
            }
            self.available_services = {
                "api_gateway", "lambda", "dynamodb", "s3", 
                "iam", "cloudwatch", "ec2", "rds"
            }
            self.budget = 50.0  # Monthly cost in USD
            self.max_latency = 300.0  # in ms
            
            # Tutorial steps
            self.tutorial_steps = [
                "First, create an API Gateway to handle HTTP requests.",
                "Next, add a Lambda function to process the API requests.",
                "Create a DynamoDB table to store blog post data.",
                "Add an S3 bucket to store media files like images.",
                "Connect API Gateway to the Lambda function.",
                "Connect Lambda to both DynamoDB and S3.",
                "Create an IAM role with appropriate permissions for Lambda.",
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
        # Check if we should advance the tutorial step
        if self.game.state.mode.name == "TUTORIAL":
            if self.current_tutorial_step < len(self.tutorial_steps) - 1:
                # Check conditions to advance to next step
                if self.current_tutorial_step == 0 and "api_gateway" in self.game.state.placed_services:
                    self.current_tutorial_step = 1
                elif self.current_tutorial_step == 1 and "lambda" in self.game.state.placed_services:
                    self.current_tutorial_step = 2
                elif self.current_tutorial_step == 2 and "dynamodb" in self.game.state.placed_services:
                    self.current_tutorial_step = 3
                elif self.current_tutorial_step == 3 and "s3" in self.game.state.placed_services:
                    self.current_tutorial_step = 4
                elif self.current_tutorial_step == 4 and any(
                    conn == ("api_gateway", "lambda") for conn in self.game.state.connections
                ):
                    self.current_tutorial_step = 5
                elif self.current_tutorial_step == 5 and any(
                    conn == ("lambda", "dynamodb") for conn in self.game.state.connections
                ) and any(
                    conn == ("lambda", "s3") for conn in self.game.state.connections
                ):
                    self.current_tutorial_step = 6
                elif self.current_tutorial_step == 6 and "iam" in self.game.state.placed_services:
                    self.current_tutorial_step = 7
    
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
        
        # Draw connections
        for source, target in self.connections:
            pygame.draw.line(
                surface,
                (0, 0, 0),
                source.get_connection_point(),
                target.get_connection_point(),
                2
            )
        
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