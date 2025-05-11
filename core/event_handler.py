"""
Event handling module for the Solutions Architect Simulator.
"""
from typing import Any, Dict, List, Optional, Tuple
import pygame


class EventHandler:
    """Handles pygame events and dispatches them to appropriate handlers."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the event handler.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        
    def process_events(self) -> None:
        """Process all pygame events in the queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
    
    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard key press events.
        
        Args:
            event: Pygame key event
        """
        if event.key == pygame.K_ESCAPE:
            # If in a level, return to main menu
            if not self.game.show_main_menu:
                self.game.show_menu()
        elif event.key == pygame.K_F1:
            # Toggle help screen
            pass
        elif event.key == pygame.K_F2 and self.game.config.debug.enabled:
            # Toggle debug information
            self.game.config.debug.show_fps = not self.game.config.debug.show_fps
    
    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
        """
        # Handle main menu interactions if active
        if self.game.show_main_menu:
            self.game.main_menu.handle_mouse_down(event)
            return
            
        # Handle completion screen interactions if active
        if self.game.show_completion_screen and self.game.completion_screen:
            self.game.completion_screen.handle_mouse_down(event)
            return
            
        # Delegate to UI manager for UI element clicks
        if self.game.ui_manager.handle_mouse_down(event):
            return
        
        # Handle canvas interactions based on mouse button
        if event.button == 1:  # Left click
            self.game.level_manager.handle_left_click(event.pos)
        elif event.button == 3:  # Right click
            self.game.level_manager.handle_right_click(event.pos)
    
    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """
        Handle mouse button up events.
        
        Args:
            event: Pygame mouse event
        """
        # Handle main menu interactions if active
        if self.game.show_main_menu:
            self.game.main_menu.handle_mouse_up(event)
            return
            
        # Handle completion screen interactions if active
        if self.game.show_completion_screen and self.game.completion_screen:
            self.game.completion_screen.handle_mouse_up(event)
            return
            
        # Delegate to UI manager
        if self.game.ui_manager.handle_mouse_up(event):
            return
        
        # Handle canvas interactions based on mouse button
        if event.button == 1:  # Left click
            self.game.level_manager.handle_left_release(event.pos)
        elif event.button == 3:  # Right click
            self.game.level_manager.handle_right_release(event.pos)
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """
        Handle mouse motion events.
        
        Args:
            event: Pygame mouse motion event
        """
        # Handle main menu interactions if active
        if self.game.show_main_menu:
            self.game.main_menu.handle_mouse_motion(event)
            return
            
        # Handle completion screen interactions if active
        if self.game.show_completion_screen and self.game.completion_screen:
            self.game.completion_screen.handle_mouse_motion(event)
            return
            
        # Update UI hover states
        self.game.ui_manager.handle_mouse_motion(event)
        
        # Update canvas hover states, connection drawing, and node dragging
        self.game.level_manager.handle_canvas_motion(event.pos)