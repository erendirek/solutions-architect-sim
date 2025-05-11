"""
Main menu UI component.
"""
from typing import Any, Dict, List, Optional, Tuple

import pygame

from core.state import GameState, GameMode
from ui.aws_theme import AWSColors, AWSStyling
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
        self.title_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_XXLARGE, bold=True)
        self.heading_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_XLARGE, bold=True)
        self.text_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_MEDIUM)
        self.level_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_LARGE, bold=True)
        self.info_font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, AWSStyling.FONT_SIZE_NORMAL)
        
        # Calculate layout
        self.window_width = self.game.config.window.width
        self.window_height = self.game.config.window.height
        
        # Animation state
        self.animation_progress = 0.0
        self.animation_speed = 0.05
        
        # Create buttons
        self._create_buttons()
        
        # Load level data
        self._load_level_data()
        
        # Create AWS logo
        self.aws_logo = self._create_aws_logo()
    
    def _create_aws_logo(self) -> pygame.Surface:
        """Create a simple AWS logo."""
        logo_width = 120
        logo_height = 60
        logo = pygame.Surface((logo_width, logo_height), pygame.SRCALPHA)
        
        # Draw "AWS" text
        font = pygame.font.SysFont(AWSStyling.FONT_FAMILY, 36, bold=True)
        text = font.render("AWS", True, AWSColors.WHITE)
        text_rect = text.get_rect(center=(logo_width // 2, logo_height // 2))
        
        # Draw orange background
        pygame.draw.rect(logo, AWSColors.SMILE_ORANGE, (0, 0, logo_width, logo_height), border_radius=5)
        
        # Draw text
        logo.blit(text, text_rect)
        
        return logo
    
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
            callback=self._on_start_click,
            style="primary"
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
            style="secondary"
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
            style="secondary"
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
            
            # Determine if level is unlocked
            is_unlocked = i in self.game.state.unlocked_levels
            is_completed = i in self.game.state.completed_levels
            
            # Set button style based on status
            style = "secondary"
            if not is_unlocked:
                style = "disabled"
            
            level_button = Button(
                rect=pygame.Rect(x, y, level_button_width, level_button_height),
                text=str(i),
                callback=lambda level=i: self._on_level_click(level),
                style=style,
                disabled=not is_unlocked
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
        # Update animation progress
        if self.animation_progress < 1.0:
            self.animation_progress += self.animation_speed
            if self.animation_progress > 1.0:
                self.animation_progress = 1.0
        
        # Update button states based on unlocked levels
        for i, button in enumerate(self.level_buttons):
            level_id = i + 1
            is_unlocked = level_id in self.game.state.unlocked_levels
            is_completed = level_id in self.game.state.completed_levels
            is_selected = level_id == self.selected_level
            
            # Set button style based on status
            if is_selected:
                button.bg_color = AWSColors.SMILE_ORANGE
                button.hover_color = (230, 138, 0)  # Darker orange
            elif is_completed:
                button.bg_color = AWSColors.SUCCESS
                button.hover_color = (48, 155, 68)  # Darker green
            elif is_unlocked:
                button.bg_color = AWSColors.BUTTON_SECONDARY
                button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
            else:
                button.bg_color = AWSColors.BUTTON_DISABLED
                button.hover_color = AWSColors.BUTTON_DISABLED
                button.disabled = True
        
        # Update mode toggle button states
        # Tutorial button
        if self.tutorial_mode:
            self.tutorial_button.text = "Tutorial Mode: ON"
            self.tutorial_button.bg_color = AWSColors.SUCCESS
            self.tutorial_button.hover_color = (48, 155, 68)  # Darker green
        elif self.selected_level > 2:  # Only levels 1-2 have tutorials
            self.tutorial_mode = False
            self.tutorial_button.text = "Tutorial Mode: OFF"
            self.tutorial_button.bg_color = AWSColors.BUTTON_DISABLED
            self.tutorial_button.hover_color = AWSColors.BUTTON_DISABLED
            self.tutorial_button.disabled = True
        else:
            self.tutorial_button.text = "Tutorial Mode: OFF"
            self.tutorial_button.bg_color = AWSColors.BUTTON_SECONDARY
            self.tutorial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
            self.tutorial_button.disabled = False
            
        # Time trial button
        if self.time_trial_mode:
            self.time_trial_button.text = "Time Trial: ON"
            self.time_trial_button.bg_color = AWSColors.SUCCESS
            self.time_trial_button.hover_color = (48, 155, 68)  # Darker green
        else:
            self.time_trial_button.text = "Time Trial: OFF"
            self.time_trial_button.bg_color = AWSColors.BUTTON_SECONDARY
            self.time_trial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the main menu.
        
        Args:
            surface: Pygame surface to render on
        """
        # Draw background gradient
        self._draw_background(surface)
        
        # Draw AWS logo
        logo_rect = self.aws_logo.get_rect(topleft=(20, 20))
        surface.blit(self.aws_logo, logo_rect)
        
        # Draw title with animation
        title_alpha = int(min(255, 255 * self.animation_progress / 0.3))
        title_text = self.title_font.render("Solutions Architect Simulator", True, AWSColors.WHITE)
        title_text.set_alpha(title_alpha)
        title_rect = title_text.get_rect(centerx=self.window_width // 2, top=30)
        surface.blit(title_text, title_rect)
        
        # Draw level selection heading with animation
        if self.animation_progress > 0.2:
            heading_alpha = int(min(255, 255 * (self.animation_progress - 0.2) / 0.3))
            heading_text = self.heading_font.render("Select Level", True, AWSColors.WHITE)
            heading_text.set_alpha(heading_alpha)
            heading_rect = heading_text.get_rect(centerx=self.window_width // 2, top=120)
            surface.blit(heading_text, heading_rect)
        
        # Draw buttons with animation
        if self.animation_progress > 0.3:
            for button in self.buttons:
                button.render(surface)
        
        # Draw selected level info with animation
        if self.animation_progress > 0.5 and self.selected_level and 1 <= self.selected_level <= len(self.level_data):
            level_info = self.level_data[self.selected_level - 1]
            
            # Create a panel for level info
            panel_rect = pygame.Rect(
                self.window_width // 2 - 300,
                self.window_height - 320,
                600,
                120
            )
            self._draw_panel(surface, panel_rect)
            
            # Draw level title
            level_title_text = self.level_font.render(
                f"Level {level_info['id']}: {level_info['title']}",
                True,
                AWSColors.WHITE
            )
            level_title_rect = level_title_text.get_rect(
                centerx=self.window_width // 2,
                top=panel_rect.top + 10
            )
            surface.blit(level_title_text, level_title_rect)
            
            # Draw level description
            description_lines = self._wrap_text(
                level_info["description"],
                self.info_font,
                panel_rect.width - 40
            )
            y = level_title_rect.bottom + 10
            for line in description_lines:
                line_text = self.info_font.render(line, True, AWSColors.LIGHT_GRAY)
                line_rect = line_text.get_rect(centerx=self.window_width // 2, top=y)
                surface.blit(line_text, line_rect)
                y += line_rect.height + 5
            
            # Draw required services in a separate panel
            services_panel_rect = pygame.Rect(
                self.window_width // 2 - 300,
                panel_rect.bottom + 10,
                600,
                60
            )
            self._draw_panel(surface, services_panel_rect)
            
            # Draw required services
            required_services = ", ".join(level_info["required_services"])
            req_label = self.info_font.render("Required Services:", True, AWSColors.SMILE_ORANGE)
            req_label_rect = req_label.get_rect(
                left=services_panel_rect.left + 20,
                top=services_panel_rect.top + 10
            )
            surface.blit(req_label, req_label_rect)
            
            req_text = self.info_font.render(required_services, True, AWSColors.WHITE)
            req_rect = req_text.get_rect(
                left=services_panel_rect.left + 20,
                top=req_label_rect.bottom + 5
            )
            surface.blit(req_text, req_rect)
            
            # Draw completion status if completed
            if self.selected_level in self.game.state.completed_levels:
                score = self.game.state.completed_levels[self.selected_level]
                rank = self.game.state.get_rank_for_score(score)
                
                # Determine rank color
                rank_color = AWSColors.RIND  # Default gold
                if rank == "Silver":
                    rank_color = (192, 192, 192)  # Silver
                elif rank == "Bronze":
                    rank_color = (205, 127, 50)  # Bronze
                
                # Create completion badge
                badge_rect = pygame.Rect(
                    services_panel_rect.right - 150,
                    services_panel_rect.top + 10,
                    130,
                    40
                )
                pygame.draw.rect(surface, rank_color, badge_rect, border_radius=10)
                pygame.draw.rect(surface, AWSColors.WHITE, badge_rect, 2, border_radius=10)
                
                # Draw rank text
                rank_text = self.info_font.render(f"{rank} Architect", True, AWSColors.SQUID_INK)
                rank_rect = rank_text.get_rect(center=badge_rect.center)
                surface.blit(rank_text, rank_rect)
                
                # Draw score
                score_text = self.info_font.render(f"Score: {score}", True, AWSColors.WHITE)
                score_rect = score_text.get_rect(
                    right=badge_rect.left - 10,
                    centery=badge_rect.centery
                )
                surface.blit(score_text, score_rect)
    
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a gradient background."""
        # Create gradient from top to bottom
        for y in range(self.window_height):
            # Calculate color for this line
            ratio = y / self.window_height
            
            # Gradient from dark blue to slightly lighter blue
            color = (
                int(AWSColors.SQUID_INK[0] * (1 - ratio) + (AWSColors.SQUID_INK[0] + 20) * ratio),
                int(AWSColors.SQUID_INK[1] * (1 - ratio) + (AWSColors.SQUID_INK[1] + 20) * ratio),
                int(AWSColors.SQUID_INK[2] * (1 - ratio) + (AWSColors.SQUID_INK[2] + 20) * ratio)
            )
            
            pygame.draw.line(surface, color, (0, y), (self.window_width, y))
        
        # Draw subtle grid pattern
        grid_color = (AWSColors.SQUID_INK[0] + 10, AWSColors.SQUID_INK[1] + 10, AWSColors.SQUID_INK[2] + 10)
        grid_spacing = 30
        
        # Draw horizontal grid lines
        for y in range(0, self.window_height, grid_spacing):
            pygame.draw.line(surface, grid_color, (0, y), (self.window_width, y), 1)
        
        # Draw vertical grid lines
        for x in range(0, self.window_width, grid_spacing):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.window_height), 1)
    
    def _draw_panel(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw a semi-transparent panel with rounded corners."""
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel_color = (*AWSColors.PANEL_DARK, 200)  # Semi-transparent
        
        # Draw panel background
        pygame.draw.rect(
            panel, 
            panel_color, 
            panel.get_rect(), 
            border_radius=AWSStyling.BORDER_RADIUS_MEDIUM
        )
        
        # Draw border
        pygame.draw.rect(
            panel, 
            AWSColors.SMILE_ORANGE, 
            panel.get_rect(), 
            2, 
            border_radius=AWSStyling.BORDER_RADIUS_MEDIUM
        )
        
        # Blit panel to surface
        surface.blit(panel, rect)
    
    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.
        
        Args:
            event: Pygame mouse event
            
        Returns:
            True if the event was handled, False otherwise
        """
        # Only handle events if animation is complete
        if self.animation_progress < 0.5:
            return False
            
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
            self.game.state.time_remaining = None
        elif self.time_trial_mode:
            self.game.state.mode = GameMode.TIME_TRIAL
            self.game.state.time_remaining = float(self.game.config.game.time_trial_seconds)
            # Reset time manager
            self.game.time_manager.reset()
        else:
            self.game.state.mode = GameMode.NORMAL
            self.game.state.time_remaining = None
        
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
                self.tutorial_button.bg_color = AWSColors.SUCCESS
                self.tutorial_button.hover_color = (48, 155, 68)  # Darker green
                
                # Disable time trial mode
                self.time_trial_mode = False
                self.time_trial_button.text = "Time Trial: OFF"
                self.time_trial_button.bg_color = AWSColors.BUTTON_SECONDARY
                self.time_trial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
            else:
                self.tutorial_button.text = "Tutorial Mode: OFF"
                self.tutorial_button.bg_color = AWSColors.BUTTON_SECONDARY
                self.tutorial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
    
    def _on_time_trial_click(self) -> None:
        """Handle click on the time trial mode button."""
        self.time_trial_mode = not self.time_trial_mode
        
        # Update button appearance immediately
        if self.time_trial_mode:
            self.time_trial_button.text = "Time Trial: ON"
            self.time_trial_button.bg_color = AWSColors.SUCCESS
            self.time_trial_button.hover_color = (48, 155, 68)  # Darker green
            
            # Disable tutorial mode
            self.tutorial_mode = False
            self.tutorial_button.text = "Tutorial Mode: OFF"
            self.tutorial_button.bg_color = AWSColors.BUTTON_SECONDARY
            self.tutorial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
            
            # Gray out tutorial button if not available for this level
            if self.selected_level > 2:
                self.tutorial_button.bg_color = AWSColors.BUTTON_DISABLED
                self.tutorial_button.hover_color = AWSColors.BUTTON_DISABLED
                self.tutorial_button.disabled = True
        else:
            self.time_trial_button.text = "Time Trial: OFF"
            self.time_trial_button.bg_color = AWSColors.BUTTON_SECONDARY
            self.time_trial_button.hover_color = AWSColors.BUTTON_SECONDARY_HOVER
    
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