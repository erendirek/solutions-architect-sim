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
        # Draw icon
        surface.blit(self.icon, self.rect)
        
        # Draw service name
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(self.service_info.display_name, True, (0, 0, 0))
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