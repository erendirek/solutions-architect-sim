"""
Level management module for the Solutions Architect Simulator.
"""
import importlib
from typing import Any, Dict, List, Optional, Tuple, Type

import pygame

from core.state import GameState
from levels.base_level import BaseLevel
from levels.level_factory import LevelFactory


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
        self.dragging_service: Optional[str] = None
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
                    (0, 0, 0),
                    self.connection_start,
                    self.connection_end,
                    2
                )
    
    def handle_canvas_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse click on the canvas.
        
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
            
        # Check if clicking on a placed service to start a connection
        service_node = self.current_level.get_service_node_at_canvas(pos)
        if service_node:
            self.drawing_connection = True
            self.connection_start = service_node.get_connection_point()
            self.connection_end = pos
    
    def handle_canvas_release(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse release on the canvas.
        
        Args:
            pos: Mouse position (x, y)
        """
        if not self.current_level:
            return
            
        # If dragging a service, place it on the canvas
        if self.dragging_service:
            canvas_rect = self.current_level.get_canvas_rect()
            if canvas_rect.collidepoint(pos):
                self.current_level.place_service(self.dragging_service, pos)
            self.dragging_service = None
            
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
        if self.drawing_connection and self.connection_start:
            self.connection_end = pos