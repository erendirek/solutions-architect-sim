"""
UI manager module for managing UI components.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame

from ui.aws_theme import AWSColors, AWSStyling
from ui.button import Button
from ui.hud import HUD
from ui.message import Message


class UIManager:
    """Manages UI components and interactions."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the UI manager.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.hud = HUD(game)
        self.buttons = []
        self.messages = []
        self.message_duration = 3000  # 3 seconds
        self.tooltip = None
        self.tooltip_delay = 500  # milliseconds
        self.tooltip_timer = 0
        self.tooltip_target = None
        
        # Create UI buttons
        self._create_buttons()
    
    def _create_buttons(self) -> None:
        """Create UI buttons."""
        # Validate architecture button
        validate_button = Button(
            rect=pygame.Rect(
                self.game.config.window.width - 220,
                self.game.config.window.height - self.game.config.ui.hud_height + 25,
                200,
                50
            ),
            text="Validate Architecture",
            callback=self._on_validate_click,
            style="primary"
        )
        self.buttons.append(validate_button)
        
        # Menu button
        menu_button = Button(
            rect=pygame.Rect(
                self.game.config.window.width - 100,
                10,
                80,
                30
            ),
            text="Menu",
            callback=self._on_menu_click,
            style="secondary"
        )
        self.buttons.append(menu_button)
        
        # Help button
        help_button = Button(
            rect=pygame.Rect(
                self.game.config.window.width - 150,
                10,
                40,
                30
            ),
            text="?",
            callback=self._on_help_click,
            style="secondary"
        )
        self.buttons.append(help_button)
    
    def update(self) -> None:
        """Update UI components."""
        # Update HUD
        self.hud.update()
        
        # Update messages
        current_time = pygame.time.get_ticks()
        self.messages = [msg for msg in self.messages if current_time - msg.creation_time < self.message_duration]
        
        # Update tooltip
        if self.tooltip_target and current_time - self.tooltip_timer > self.tooltip_delay:
            # Show tooltip
            if self.tooltip_target == "validate":
                self.tooltip = "Validate your architecture against level requirements"
            elif self.tooltip_target == "menu":
                self.tooltip = "Return to the main menu"
            elif self.tooltip_target == "help":
                self.tooltip = "Show help information"
    
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
        
        # Render messages
        for message in self.messages:
            message.render(surface)
            
        # Render tooltip if active
        if self.tooltip:
            mouse_pos = pygame.mouse.get_pos()
            self._render_tooltip(surface, self.tooltip, mouse_pos)
    
    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Reset tooltip
        self.tooltip = None
        self.tooltip_target = None
        
        # Check button clicks
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.on_click()
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
        for i, button in enumerate(self.buttons):
            was_hovered = button.is_hovered
            button.is_hovered = button.rect.collidepoint(event.pos)
            
            # Start tooltip timer if newly hovered
            if button.is_hovered and not was_hovered:
                self.tooltip_timer = pygame.time.get_ticks()
                if i == 0:  # Validate button
                    self.tooltip_target = "validate"
                elif i == 1:  # Menu button
                    self.tooltip_target = "menu"
                elif i == 2:  # Help button
                    self.tooltip_target = "help"
            
            # Reset tooltip if no longer hovering
            if not button.is_hovered and was_hovered and self.tooltip_target:
                self.tooltip = None
                self.tooltip_target = None
    
    def show_message(self, text: str) -> None:
        """
        Show a message on the screen.
        
        Args:
            text: Message text to display
        """
        message = Message(
            text=text,
            position=(self.game.config.window.width // 2, 100),
            font=pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_LARGE),
            color=AWSColors.WHITE,
            bg_color=AWSColors.SQUID_INK
        )
        self.messages.append(message)
    
    def _render_tooltip(self, surface: pygame.Surface, text: str, pos: Tuple[int, int]) -> None:
        """
        Render a tooltip at the given position.
        
        Args:
            surface: Pygame surface to render on
            text: Tooltip text
            pos: Position (x, y) to render the tooltip
        """
        # Create font and render text
        font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_SMALL)
        text_surface = font.render(text, True, AWSColors.WHITE)
        
        # Calculate tooltip dimensions
        padding = AWSStyling.PADDING_SMALL
        tooltip_width = text_surface.get_width() + padding * 2
        tooltip_height = text_surface.get_height() + padding * 2
        
        # Create tooltip rectangle
        tooltip_rect = pygame.Rect(
            pos[0] + 15,  # Offset from cursor
            pos[1] + 15,
            tooltip_width,
            tooltip_height
        )
        
        # Keep tooltip on screen
        if tooltip_rect.right > self.game.config.window.width:
            tooltip_rect.right = self.game.config.window.width - 5
        if tooltip_rect.bottom > self.game.config.window.height:
            tooltip_rect.bottom = self.game.config.window.height - 5
        
        # Draw tooltip background
        pygame.draw.rect(surface, AWSColors.SQUID_INK, tooltip_rect, border_radius=AWSStyling.BORDER_RADIUS_SMALL)
        pygame.draw.rect(surface, AWSColors.SMILE_ORANGE, tooltip_rect, 1, border_radius=AWSStyling.BORDER_RADIUS_SMALL)
        
        # Draw tooltip text
        text_rect = text_surface.get_rect(center=tooltip_rect.center)
        surface.blit(text_surface, text_rect)
    
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
        from core.state import GameMode
        if self.game.state.mode == GameMode.TIME_TRIAL:
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
        
    def _on_help_click(self) -> None:
        """Handle click on the help button."""
        # Show help message with controls
        help_text = "Left-click: Place/move services | Right-click: Create/remove connections | Drag to panel: Remove service"
        self.show_message(help_text)