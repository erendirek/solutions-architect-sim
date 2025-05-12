"""
Level generator module for creating level classes from levels.json.
"""
import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Type

from levels.base_level import BaseLevel
from levels.level_factory import LevelFactory


class LevelTemplate(BaseLevel):
    """Template class for dynamically generated levels."""
    
    def __init__(self, game: Any, level_id: int) -> None:
        """
        Initialize a level from template.
        
        Args:
            game: Reference to the main game object
            level_id: ID of the level to load
        """
        super().__init__(game)
        
        # Load level data from levels.json
        self.load_level_data(level_id)
        
        # Load service icons
        self._load_service_icons()
    
    def _load_service_icons(self) -> None:
        """Load service icons for the available services."""
        from services.service_registry import ServiceRegistry
        
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
                import pygame
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
        # Call parent update to handle connection animations
        super().update()
        
        # Check if we should advance the tutorial step
        if self.game.state.mode.name == "TUTORIAL":
            if self.current_tutorial_step < len(self.tutorial_steps) - 1:
                # Simple tutorial progression based on required services
                required_services_list = list(self.required_services)
                
                # Check if the current step's service has been placed
                if self.current_tutorial_step < len(required_services_list):
                    current_service = required_services_list[self.current_tutorial_step]
                    if current_service in self.game.state.placed_services:
                        self.current_tutorial_step += 1
    
    def render(self, surface: Any) -> None:
        """
        Render the level.
        
        Args:
            surface: Pygame surface to render on
        """
        import pygame
        
        # Draw service panel background with gradient
        panel_rect = pygame.Rect(0, 0, self.game.config.ui.service_panel_width, self.game.config.window.height - self.game.config.ui.hud_height)
        
        # Create gradient from top to bottom
        for y in range(panel_rect.height):
            # Calculate color for this line
            ratio = y / panel_rect.height
            
            # Gradient from light to slightly darker
            color = (
                int(230 * (1 - ratio) + 210 * ratio),
                int(230 * (1 - ratio) + 210 * ratio),
                int(235 * (1 - ratio) + 220 * ratio)
            )
            
            pygame.draw.line(surface, color, (0, y), (panel_rect.right, y))
        
        # Draw panel title
        title_font = pygame.font.SysFont("Arial", 16, bold=True)
        title_text = title_font.render("AWS Services", True, (50, 50, 50))
        title_rect = title_text.get_rect(centerx=panel_rect.width // 2, top=10)
        
        # Draw title background
        title_bg_rect = title_rect.inflate(20, 10)
        pygame.draw.rect(surface, (255, 255, 255, 180), title_bg_rect, border_radius=5)
        
        # Draw title text
        surface.blit(title_text, title_rect)
        
        # Draw separator line
        pygame.draw.line(
            surface, 
            (180, 180, 180), 
            (panel_rect.right, 0), 
            (panel_rect.right, panel_rect.bottom), 
            2
        )
        
        # Draw subtle pattern in panel
        pattern_color = (200, 200, 205)
        pattern_spacing = 15
        
        for x in range(0, panel_rect.width, pattern_spacing):
            pygame.draw.line(
                surface,
                pattern_color,
                (x, 0),
                (x, panel_rect.height),
                1
            )
        
        # Draw service icons in panel with improved styling
        font = pygame.font.SysFont("Arial", 12, bold=True)
        for service_id, rect in self.service_rects.items():
            # Draw icon background and border
            bg_rect = rect.inflate(8, 8)
            
            # Draw background
            pygame.draw.rect(
                surface,
                (240, 240, 240),  # Light background
                bg_rect,
                border_radius=6
            )
            
            # Draw border
            pygame.draw.rect(
                surface,
                (180, 180, 180),  # Border color
                bg_rect,
                2,
                border_radius=6
            )
            
            # Draw icon
            surface.blit(self.service_icons[service_id], rect)
            
            # Draw service name with better visibility
            from services.service_registry import ServiceRegistry
            service_info = ServiceRegistry.get_service(service_id)
            if service_info:
                # Draw text shadow for better readability
                shadow_text = font.render(service_info.display_name, True, (50, 50, 50))
                shadow_rect = shadow_text.get_rect(centerx=rect.centerx + 1, top=rect.bottom + 3)
                surface.blit(shadow_text, shadow_rect)
                
                # Draw text
                text = font.render(service_info.display_name, True, (0, 0, 0))
                text_rect = text.get_rect(centerx=rect.centerx, top=rect.bottom + 2)
                surface.blit(text, text_rect)
        
        # Draw canvas background with grid pattern
        # Fill with base color
        pygame.draw.rect(surface, (240, 240, 245), self.canvas_rect)
        
        # Draw subtle grid pattern
        grid_spacing = 20
        grid_color = (230, 230, 235)
        
        # Draw horizontal grid lines
        for y in range(self.canvas_rect.top, self.canvas_rect.bottom, grid_spacing):
            pygame.draw.line(
                surface,
                grid_color,
                (self.canvas_rect.left, y),
                (self.canvas_rect.right, y),
                1
            )
        
        # Draw vertical grid lines
        for x in range(self.canvas_rect.left, self.canvas_rect.right, grid_spacing):
            pygame.draw.line(
                surface,
                grid_color,
                (x, self.canvas_rect.top),
                (x, self.canvas_rect.bottom),
                1
            )
        
        # Draw border with gradient effect
        border_colors = [
            (180, 180, 200),  # Top and left
            (150, 150, 170)   # Bottom and right
        ]
        
        # Top border
        pygame.draw.line(
            surface,
            border_colors[0],
            (self.canvas_rect.left, self.canvas_rect.top),
            (self.canvas_rect.right, self.canvas_rect.top),
            2
        )
        
        # Left border
        pygame.draw.line(
            surface,
            border_colors[0],
            (self.canvas_rect.left, self.canvas_rect.top),
            (self.canvas_rect.left, self.canvas_rect.bottom),
            2
        )
        
        # Bottom border
        pygame.draw.line(
            surface,
            border_colors[1],
            (self.canvas_rect.left, self.canvas_rect.bottom),
            (self.canvas_rect.right, self.canvas_rect.bottom),
            2
        )
        
        # Right border
        pygame.draw.line(
            surface,
            border_colors[1],
            (self.canvas_rect.right, self.canvas_rect.top),
            (self.canvas_rect.right, self.canvas_rect.bottom),
            2
        )
        
        # Draw placed services on canvas
        for node in self.placed_service_nodes:
            node.render(surface)
        
        # Draw connections with animated styling
        self.connection_animator.render(surface, self.connections)
        
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


def generate_level_classes() -> None:
    """Generate level classes from levels.json and register them with the LevelFactory."""
    try:
        # Load level data from JSON file
        levels_file = os.path.join("config", "levels.json")
        if not os.path.exists(levels_file):
            print(f"Error: {levels_file} not found")
            return
                
        with open(levels_file, "r") as f:
            levels_data = json.load(f)
        
        # Generate a class for each level
        for level_data in levels_data.get("levels", []):
            level_id = level_data.get("id")
            if level_id is None:
                continue
                
            # Skip levels 1 and 2 as they have custom implementations
            if level_id in [1, 2]:
                continue
                
            # Create a factory function to create a level instance
            def create_level_instance(game: Any, level_id=level_id) -> BaseLevel:
                return LevelTemplate(game, level_id)
                
            # Register the factory function with the LevelFactory
            LevelFactory.register_level(level_id, create_level_instance)
            
        print(f"Generated classes for {len(levels_data.get('levels', [])) - 2} levels")
            
    except Exception as e:
        print(f"Error generating level classes: {e}")


# Generate level classes when this module is imported
generate_level_classes()