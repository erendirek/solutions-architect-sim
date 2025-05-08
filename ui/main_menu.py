"""
Main menu UI component.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame

from core.state import GameState, GameMode
from ui.button import Button


class MainMenu:
    """Main menu UI component for level selection and game mode settings."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the main menu.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.active = True
        self.selected_level = 1
        self.tutorial_mode = False
        self.time_trial_mode = False
        
        # Create fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 18)
        self.level_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 16)
        
        # Calculate layout
        self.window_width = self.game.config.window.width
        self.window_height = self.game.config.window.height
        
        # Create buttons
        self._create_buttons()
        
        # Load level data
        self._load_level_data()
    
    def _create_buttons(self) -> None:
        """Create UI buttons for the main menu."""
        self.buttons = []
        
        # Start button
        start_button = Button(
            rect=pygame.Rect(
                self.window_width // 2 - 100,
                self.window_height - 120,
                200,
                50
            ),
            text="Start Level",
            callback=self._on_start_click
        )
        self.buttons.append(start_button)
        
        # Tutorial mode toggle button
        tutorial_button = Button(
            rect=pygame.Rect(
                self.window_width // 2 - 220,
                self.window_height - 180,
                200,
                40
            ),
            text="Tutorial Mode: OFF",
            callback=self._on_tutorial_click,
            bg_color=(100, 100, 180)
        )
        self.buttons.append(tutorial_button)
        self.tutorial_button = tutorial_button
        
        # Time trial mode toggle button
        time_trial_button = Button(
            rect=pygame.Rect(
                self.window_width // 2 + 20,
                self.window_height - 180,
                200,
                40
            ),
            text="Time Trial: OFF",
            callback=self._on_time_trial_click,
            bg_color=(100, 100, 180)
        )
        self.buttons.append(time_trial_button)
        self.time_trial_button = time_trial_button
        
        # Level selection buttons
        level_button_width = 80
        level_button_height = 80
        levels_per_row = 5
        start_x = (self.window_width - (level_button_width * levels_per_row + 20 * (levels_per_row - 1))) // 2
        start_y = 180
        
        self.level_buttons = []
        for i in range(1, 11):  # 10 levels
            row = (i - 1) // levels_per_row
            col = (i - 1) % levels_per_row
            x = start_x + col * (level_button_width + 20)
            y = start_y + row * (level_button_height + 20)
            
            level_button = Button(
                rect=pygame.Rect(x, y, level_button_width, level_button_height),
                text=str(i),
                callback=lambda level=i: self._on_level_click(level),
                bg_color=(80, 80, 200),
                hover_color=(100, 100, 220)
            )
            self.buttons.append(level_button)
            self.level_buttons.append(level_button)
    
    def _load_level_data(self) -> None:
        """Load level data from configuration."""
        import json
        import os
        
        levels_file = os.path.join("config", "levels.json")
        if os.path.exists(levels_file):
            with open(levels_file, "r") as f:
                self.level_data = json.load(f)["levels"]
        else:
            self.level_data = []
    
    def update(self) -> None:
        """Update the main menu state."""
        # Update button states based on unlocked levels
        for i, button in enumerate(self.level_buttons):
            level_id = i + 1
            is_unlocked = level_id in self.game.state.unlocked_levels
            
            # Set button color based on unlock status
            if level_id == self.selected_level:
                button.bg_color = (100, 180, 100)  # Green for selected
                button.hover_color = (120, 200, 120)
            elif is_unlocked:
                button.bg_color = (80, 80, 200)  # Blue for unlocked
                button.hover_color = (100, 100, 220)
            else:
                button.bg_color = (150, 150, 150)  # Gray for locked
                button.hover_color = (170, 170, 170)
        
        # Update mode toggle button colors based on state
        # Tutorial button
        if self.tutorial_mode:
            self.tutorial_button.bg_color = (100, 180, 100)  # Green for active
            self.tutorial_button.hover_color = (120, 200, 120)
        elif self.selected_level > 2:  # Only levels 1-2 have tutorials
            self.tutorial_mode = False
            self.tutorial_button.bg_color = (150, 150, 150)  # Gray for disabled
            self.tutorial_button.hover_color = (170, 170, 170)
        else:
            self.tutorial_button.bg_color = (100, 100, 180)  # Blue for available but inactive
            self.tutorial_button.hover_color = (120, 120, 200)
            
        # Time trial button
        if self.time_trial_mode:
            self.time_trial_button.bg_color = (100, 180, 100)  # Green for active
            self.time_trial_button.hover_color = (120, 200, 120)
        else:
            self.time_trial_button.bg_color = (100, 100, 180)  # Blue for inactive
            self.time_trial_button.hover_color = (120, 120, 200)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the main menu.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw background
        surface.fill((240, 240, 240))
        
        # Draw title
        title_text = self.title_font.render("Solutions Architect Simulator", True, (0, 0, 0))
        title_rect = title_text.get_rect(centerx=self.window_width // 2, top=30)
        surface.blit(title_text, title_rect)
        
        # Draw level selection heading
        heading_text = self.heading_font.render("Select Level", True, (0, 0, 0))
        heading_rect = heading_text.get_rect(centerx=self.window_width // 2, top=120)
        surface.blit(heading_text, heading_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.render(surface)
        
        # Draw selected level info
        if self.selected_level and 1 <= self.selected_level <= len(self.level_data):
            level_info = self.level_data[self.selected_level - 1]
            
            # Draw level title
            level_title_text = self.level_font.render(
                f"Level {level_info['id']}: {level_info['title']}",
                True,
                (0, 0, 0)
            )
            level_title_rect = level_title_text.get_rect(
                centerx=self.window_width // 2,
                top=self.window_height - 300
            )
            surface.blit(level_title_text, level_title_rect)
            
            # Draw level description
            description_lines = self._wrap_text(
                level_info["description"],
                self.info_font,
                self.window_width - 200
            )
            y = level_title_rect.bottom + 10
            for line in description_lines:
                line_text = self.info_font.render(line, True, (0, 0, 0))
                line_rect = line_text.get_rect(centerx=self.window_width // 2, top=y)
                surface.blit(line_text, line_rect)
                y += line_rect.height + 5
            
            # Draw level requirements
            required_services = ", ".join(level_info["required_services"])
            req_text = self.info_font.render(
                f"Required Services: {required_services}",
                True,
                (0, 0, 0)
            )
            req_rect = req_text.get_rect(centerx=self.window_width // 2, top=y + 10)
            surface.blit(req_text, req_rect)
            
            # Draw completion status
            if self.selected_level in self.game.state.completed_levels:
                score = self.game.state.completed_levels[self.selected_level]
                rank = self.game.state.get_rank_for_score(score)
                completion_text = self.info_font.render(
                    f"Completed with {score} points - {rank} Architect",
                    True,
                    (0, 100, 0)
                )
                completion_rect = completion_text.get_rect(
                    centerx=self.window_width // 2,
                    top=req_rect.bottom + 10
                )
                surface.blit(completion_text, completion_rect)
    
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
    
    def _on_level_click(self, level_id: int) -> None:
        """
        Handle click on a level button.
        
        Args:
            level_id: ID of the clicked level
        """
        # Only allow selecting unlocked levels
        if level_id in self.game.state.unlocked_levels:
            self.selected_level = level_id
    
    def _on_start_click(self) -> None:
        """Handle click on the start button."""
        # Set game mode
        if self.tutorial_mode:
            self.game.state.mode = GameMode.TUTORIAL
        elif self.time_trial_mode:
            self.game.state.mode = GameMode.TIME_TRIAL
            self.game.state.time_remaining = self.game.config.game.time_trial_seconds
        else:
            self.game.state.mode = GameMode.NORMAL
        
        # Load the selected level
        self.game.level_manager.load_level(self.selected_level)
        
        # Close the main menu
        self.active = False
    
    def _on_tutorial_click(self) -> None:
        """Handle click on the tutorial mode button."""
        # Only toggle if the selected level supports tutorials (levels 1-2)
        if self.selected_level <= 2:
            self.tutorial_mode = not self.tutorial_mode
            
            # Update button appearance immediately
            if self.tutorial_mode:
                self.tutorial_button.text = "Tutorial Mode: ON"
                self.tutorial_button.bg_color = (100, 180, 100)  # Green for active
                self.tutorial_button.hover_color = (120, 200, 120)
                
                # Disable time trial mode
                self.time_trial_mode = False
                self.time_trial_button.text = "Time Trial: OFF"
                self.time_trial_button.bg_color = (100, 100, 180)  # Blue for inactive
                self.time_trial_button.hover_color = (120, 120, 200)
            else:
                self.tutorial_button.text = "Tutorial Mode: OFF"
                self.tutorial_button.bg_color = (100, 100, 180)  # Blue for inactive
                self.tutorial_button.hover_color = (120, 120, 200)
    
    def _on_time_trial_click(self) -> None:
        """Handle click on the time trial mode button."""
        self.time_trial_mode = not self.time_trial_mode
        
        # Update button appearance immediately
        if self.time_trial_mode:
            self.time_trial_button.text = "Time Trial: ON"
            self.time_trial_button.bg_color = (100, 180, 100)  # Green for active
            self.time_trial_button.hover_color = (120, 200, 120)
            
            # Disable tutorial mode
            self.tutorial_mode = False
            self.tutorial_button.text = "Tutorial Mode: OFF"
            self.tutorial_button.bg_color = (100, 100, 180)  # Blue for inactive
            self.tutorial_button.hover_color = (120, 120, 200)
            
            # Gray out tutorial button if not available for this level
            if self.selected_level > 2:
                self.tutorial_button.bg_color = (150, 150, 150)  # Gray for disabled
                self.tutorial_button.hover_color = (170, 170, 170)
        else:
            self.time_trial_button.text = "Time Trial: OFF"
            self.time_trial_button.bg_color = (100, 100, 180)  # Blue for inactive
            self.time_trial_button.hover_color = (120, 120, 200)
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """
        Wrap text to fit within a given width.
        
        Args:
            text: Text to wrap
            font: Font to use for measuring text
            max_width: Maximum width in pixels
            
        Returns:
            List of wrapped text lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # If the word is too long for a single line, force it
                    lines.append(word)
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines