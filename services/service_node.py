"""
Service node module for representing AWS services on the canvas.
"""
from typing import Dict, List, Optional, Tuple

import pygame

from services.service_registry import ServiceInfo


class ServiceNode:
    """Represents an AWS service placed on the canvas."""
    
    def __init__(self, service_id: str, service_info: ServiceInfo, position: Tuple[int, int]) -> None:
        """
        Initialize a service node.
        
        Args:
            service_id: ID of the service
            service_info: Service information
            position: Position (x, y) on the canvas
        """
        self.service_id = service_id
        self.service_info = service_info
        
        # Load and scale icon
        self.icon = pygame.image.load(service_info.icon_path)
        self.icon = pygame.transform.scale(self.icon, (64, 64))
        
        # Create rect for collision detection
        self.rect = self.icon.get_rect(center=position)
        
        # Store original position for connection point calculation
        self.position = position
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the service node.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw a glowing effect behind the icon
        glow_size = 4
        glow_rect = pygame.Rect(
            self.rect.left - glow_size,
            self.rect.top - glow_size,
            self.rect.width + glow_size * 2,
            self.rect.height + glow_size * 2
        )
        
        # Draw outer glow (orange)
        pygame.draw.rect(
            surface, 
            (255, 153, 0, 150),  # AWS Orange with transparency
            glow_rect,
            border_radius=10
        )
        
        # Draw inner border (darker)
        border_rect = pygame.Rect(
            self.rect.left - 2,
            self.rect.top - 2,
            self.rect.width + 4,
            self.rect.height + 4
        )
        pygame.draw.rect(
            surface, 
            (50, 60, 70),  # Dark border
            border_rect,
            border_radius=8
        )
        
        # Draw icon background (lighter)
        bg_rect = pygame.Rect(
            self.rect.left - 1,
            self.rect.top - 1,
            self.rect.width + 2,
            self.rect.height + 2
        )
        pygame.draw.rect(
            surface, 
            (240, 240, 240),  # Light background
            bg_rect,
            border_radius=6
        )
        
        # Draw icon
        surface.blit(self.icon, self.rect)
        
        # Draw service name with shadow for better visibility
        font = pygame.font.SysFont("Arial", 12, bold=True)
        
        # Draw text shadow
        shadow_text = font.render(self.service_info.display_name, True, (30, 30, 30))
        shadow_rect = shadow_text.get_rect(centerx=self.rect.centerx + 1, top=self.rect.bottom + 3)
        surface.blit(shadow_text, shadow_rect)
        
        # Draw text
        text = font.render(self.service_info.display_name, True, (255, 255, 255))
        text_rect = text.get_rect(centerx=self.rect.centerx, top=self.rect.bottom + 2)
        surface.blit(text, text_rect)
    
    def get_connection_point(self) -> Tuple[int, int]:
        """
        Get the point where connections should attach to this node.
        
        Returns:
            (x, y) coordinates for the connection point
        """
        return self.rect.center
    
    def move_to(self, position: Tuple[int, int]) -> None:
        """
        Move the service node to a new position.
        
        Args:
            position: New position (x, y)
        """
        self.rect.center = position
        self.position = position