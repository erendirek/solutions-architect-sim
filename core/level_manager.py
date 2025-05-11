"""
Level management module for the Solutions Architect Simulator.
"""
import importlib
from typing import Any, Dict, List, Optional, Tuple, Type

import pygame

from core.state import GameState
from levels.base_level import BaseLevel
from levels.level_factory import LevelFactory
from services.service_node import ServiceNode


class LevelManager:
    """Manages level loading, transitions, and state."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the level manager.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.current_level: Optional[BaseLevel] = None
        
        # Service dragging state
        self.dragging_service: Optional[str] = None  # For new service from panel
        self.dragging_node: Optional[ServiceNode] = None  # For existing service on canvas
        self.drag_offset: Tuple[int, int] = (0, 0)  # Offset from mouse to node center
        
        # Connection drawing state
        self.drawing_connection: bool = False
        self.connection_start: Optional[Tuple[int, int]] = None
        self.connection_end: Optional[Tuple[int, int]] = None
        
        # Load the initial level
        self.load_level(self.game.state.current_level_id)
    
    def load_level(self, level_id: int) -> None:
        """
        Load a level by its ID.
        
        Args:
            level_id: ID of the level to load
        """
        try:
            # Use the LevelFactory to create the level
            level = LevelFactory.create_level(level_id, self.game)
            
            if level:
                self.current_level = level
                
                # Reset the game state for the new level
                self.game.state.reset_level()
                self.game.state.current_level_id = level_id
                
                # Reset dragging and connection state
                self.dragging_service = None
                self.dragging_node = None
                self.drawing_connection = False
                self.connection_start = None
                self.connection_end = None
            else:
                print(f"Error: Level {level_id} not found")
                # Fall back to level 1 if there's an error
                if level_id != 1:
                    self.load_level(1)
            
        except Exception as e:
            print(f"Error loading level {level_id}: {e}")
            # Fall back to level 1 if there's an error
            if level_id != 1:
                self.load_level(1)
    
    def update(self) -> None:
        """Update the current level."""
        if self.current_level:
            self.current_level.update()
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the current level.
        
        Args:
            surface: Pygame surface to render on
        """
        if self.current_level:
            self.current_level.render(surface)
            
            # Draw connection being created if applicable
            if self.drawing_connection and self.connection_start and self.connection_end:
                pygame.draw.line(
                    surface,
                    (255, 153, 0),  # AWSColors.SMILE_ORANGE - Daha görünür bağlantı çizgisi
                    self.connection_start,
                    self.connection_end,
                    3
                )
            
            # Draw service being dragged from panel if applicable
            if self.dragging_service and not self.dragging_node:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()
                
                # Get service info
                from services.service_registry import ServiceRegistry
                service_info = ServiceRegistry.get_service(self.dragging_service)
                
                if service_info:
                    # Load and scale icon
                    icon = pygame.image.load(service_info.icon_path)
                    icon = pygame.transform.scale(icon, (64, 64))
                    
                    # Draw icon at mouse position
                    icon_rect = icon.get_rect(center=mouse_pos)
                    surface.blit(icon, icon_rect)
    
    def handle_left_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle left mouse click on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        if not self.current_level:
            return
            
        # Check if clicking on a service in the panel to start dragging
        service = self.current_level.get_service_at_panel(pos)
        if service:
            self.dragging_service = service
            return
            
        # Check if clicking on a placed service to start dragging it
        service_node = self.current_level.get_service_node_at_canvas(pos)
        if service_node:
            self.dragging_node = service_node
            # Calculate offset between mouse position and node center
            self.drag_offset = (
                service_node.rect.centerx - pos[0],
                service_node.rect.centery - pos[1]
            )
            return
    
    def handle_right_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle right mouse click on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        if not self.current_level:
            return
            
        # Check if clicking on a connection to remove it
        connection = self.current_level.get_connection_at_point(pos)
        if connection:
            source, target = connection
            self.current_level.remove_connection(source, target)
            return
            
        # Check if clicking on a placed service to start a connection
        service_node = self.current_level.get_service_node_at_canvas(pos)
        if service_node:
            self.drawing_connection = True
            self.connection_start = service_node.get_connection_point()
            self.connection_end = pos
    
    def handle_left_release(self, pos: Tuple[int, int]) -> None:
        """
        Handle left mouse button release on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        if not self.current_level:
            return
            
        # If dragging a new service from panel, place it on the canvas
        if self.dragging_service:
            canvas_rect = self.current_level.get_canvas_rect()
            if canvas_rect.collidepoint(pos):
                self.current_level.place_service(self.dragging_service, pos)
            self.dragging_service = None
        
        # If dragging an existing service node, check if it should be removed or released
        if self.dragging_node:
            # Check if the node is being dragged to the service panel (to remove it)
            if self.current_level.service_panel_rect.collidepoint(pos):
                # Remove the service
                self.current_level.remove_service(self.dragging_node)
                self.game.ui_manager.show_message("Service removed")
            
            # Reset dragging state
            self.dragging_node = None
    
    def handle_right_release(self, pos: Tuple[int, int]) -> None:
        """
        Handle right mouse button release on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        if not self.current_level:
            return
            
        # If drawing a connection, try to complete it
        if self.drawing_connection and self.connection_start:
            target_node = self.current_level.get_service_node_at_canvas(pos)
            if target_node:
                source_node = self.current_level.get_service_node_at_point(self.connection_start)
                if source_node and source_node != target_node:
                    self.current_level.create_connection(source_node, target_node)
            
            self.drawing_connection = False
            self.connection_start = None
            self.connection_end = None
    
    def handle_canvas_motion(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse motion on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        # Update connection drawing
        if self.drawing_connection and self.connection_start:
            self.connection_end = pos
        
        # Update node dragging
        if self.dragging_node:
            # Calculate new position with offset
            new_pos = (
                pos[0] + self.drag_offset[0],
                pos[1] + self.drag_offset[1]
            )
            
            # Move the node to the new position (we'll check boundaries in the release handler)
            self.dragging_node.move_to(new_pos)
            
            # Update connections in the game state
            self.current_level.update_connections()