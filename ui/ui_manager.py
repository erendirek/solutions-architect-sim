"""
UI manager module for handling UI components and interactions.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame

from ui.button import Button
from ui.tooltip import Tooltip
from ui.message_box import MessageBox
from ui.hud import HUD


class UIManager:
    """Manages UI components and interactions."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the UI manager.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.buttons: List[Button] = []
        self.active_tooltip: Optional[Tooltip] = None
        self.tooltip_timer: int = 0
        self.message_box: Optional[MessageBox] = None
        
        # Create HUD
        self.hud = HUD(game)
        
        # Create buttons
        self._create_buttons()
    
    def _create_buttons(self) -> None:
        """Create UI buttons."""
        # Validate architecture button
        validate_button = Button(
            rect=pygame.Rect(
                self.game.config.window.width - 200,
                self.game.config.window.height - self.game.config.ui.hud_height + 20,
                180,
                60
            ),
            text="Validate Architecture",
            callback=self._on_validate_click
        )
        self.buttons.append(validate_button)
        
        # Menu button
        menu_button = Button(
            rect=pygame.Rect(
                20,
                self.game.config.window.height - self.game.config.ui.hud_height + 20,
                100,
                60
            ),
            text="Menu",
            callback=self._on_menu_click
        )
        self.buttons.append(menu_button)
    
    def _on_validate_click(self) -> None:
        """Handle click on the validate architecture button."""
        if not self.game.level_manager.current_level:
            return
            
        # If completion screen is already showing, ignore additional clicks
        if self.game.show_completion_screen:
            return
            
        # Validate the current architecture
        is_valid, message, score_adjustment = self.game.level_manager.current_level.validate_architecture()
        
        # Update score
        self.game.state.score += score_adjustment
        
        # If not valid, show error message
        if not is_valid:
            self.show_message(message)
            return
            
        # If valid, mark level as completed
        level_id = self.game.state.current_level_id
        
        # Double the score if in time trial mode
        if self.game.state.mode == self.game.state.mode.TIME_TRIAL:
            self.game.state.score *= 2
            self.show_message("Time Trial bonus: Score doubled!")
            
            # Stop the timer
            self.game.time_manager.time_out = True
        
        # Complete the level
        self.game.state.complete_level(level_id, self.game.state.score)
        
        # Get rank
        rank = self.game.state.get_rank_for_score(self.game.state.score)
        
        # Show completion screen
        self.game.show_level_completion(self.game.state.score, rank, level_id)
    
    def _on_menu_click(self) -> None:
        """Handle click on the menu button."""
        self.game.show_menu()
    
    def update(self) -> None:
        """Update UI components."""
        # Update HUD
        self.hud.update()
        
        # Update tooltip timer
        if self.tooltip_timer > 0:
            self.tooltip_timer -= 1
            if self.tooltip_timer == 0 and self.active_tooltip is None:
                # Show tooltip for the hovered service
                mouse_pos = pygame.mouse.get_pos()
                service_id = self._get_hovered_service(mouse_pos)
                if service_id:
                    self._show_tooltip(service_id, mouse_pos)
        
        # Update message box
        if self.message_box:
            self.message_box.update()
            if not self.message_box.active:
                self.message_box = None
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render UI components.
        
        Args:
            surface: Pygame surface to render on
        """
        # Render HUD
        self.hud.render(surface)
        
        # Render buttons
        for button in self.buttons:
            button.render(surface)
        
        # Render tooltip
        if self.active_tooltip:
            self.active_tooltip.render(surface)
        
        # Render message box
        if self.message_box:
            self.message_box.render(surface)
    
    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Check button clicks
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.on_click()
                return True
        
        # Check message box clicks
        if self.message_box and self.message_box.rect.collidepoint(event.pos):
            self.message_box.on_click()
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
        # No specific handling for mouse up events yet
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
        
        # Handle tooltip
        service_id = self._get_hovered_service(event.pos)
        if service_id:
            # Start tooltip timer if not already showing a tooltip
            if self.active_tooltip is None and self.tooltip_timer == 0:
                self.tooltip_timer = self.game.config.ui.tooltip_delay_ms // (1000 // self.game.config.window.fps)
        else:
            # Hide tooltip and reset timer
            self.active_tooltip = None
            self.tooltip_timer = 0
    
    def _get_hovered_service(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Get the service ID at the given position in the service panel.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            Service ID if found, None otherwise
        """
        if self.game.level_manager.current_level:
            return self.game.level_manager.current_level.get_service_at_panel(pos)
        return None
    
    def _show_tooltip(self, service_id: str, pos: Tuple[int, int]) -> None:
        """
        Show a tooltip for the given service.
        
        Args:
            service_id: ID of the service to show tooltip for
            pos: Position (x, y) to show the tooltip at
        """
        from services.service_registry import ServiceRegistry
        
        service_info = ServiceRegistry.get_service(service_id)
        if service_info:
            content = [
                service_info.display_name,
                f"Category: {service_info.category}",
                f"Cost: ${service_info.cost_per_hour:.2f}/hour",
                f"Latency: {service_info.latency_ms}ms",
                "",
                service_info.description
            ]
            
            self.active_tooltip = Tooltip(pos, content)
    
    def show_message(self, message: str) -> None:
        """
        Show a message box with the given message.
        
        Args:
            message: Message to display
        """
        self.message_box = MessageBox(
            message,
            pygame.Rect(
                self.game.config.window.width // 2 - 200,
                self.game.config.window.height // 2 - 100,
                400,
                200
            )
        )