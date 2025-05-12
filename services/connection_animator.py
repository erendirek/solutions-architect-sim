"""
Connection animator module for animating connections between services.
"""
import math
from typing import Dict, List, Optional, Tuple

import pygame

from ui.aws_theme import AWSColors


class ConnectionAnimator:
    """Animates connections between services with flowing color transitions."""
    
    def __init__(self) -> None:
        """Initialize the connection animator."""
        # Dictionary to store animation state for each connection
        # Key: (source_id, target_id), Value: animation_progress (0.0 to 1.0)
        self.animations: Dict[Tuple[str, str], float] = {}
        
        # Animation speed (can be adjusted for faster/slower animations)
        self.animation_speed = 0.01
        
        # AWS color palette for animations
        self.colors = [
            AWSColors.SMILE_ORANGE,  # Orange
            AWSColors.POWDER_BLUE,   # Blue
            AWSColors.LIME,          # Green
            AWSColors.RIND           # Gold
        ]
        
        # Pulse effect parameters
        self.pulse_time = 0.0
        self.pulse_speed = 0.03
    
    def add_connection(self, source_id: str, target_id: str) -> None:
        """
        Add a new connection to animate.
        
        Args:
            source_id: Source service ID
            target_id: Target service ID
        """
        connection_key = (source_id, target_id)
        if connection_key not in self.animations:
            self.animations[connection_key] = 0.0
    
    def remove_connection(self, source_id: str, target_id: str) -> None:
        """
        Remove a connection from animation.
        
        Args:
            source_id: Source service ID
            target_id: Target service ID
        """
        connection_key = (source_id, target_id)
        if connection_key in self.animations:
            del self.animations[connection_key]
    
    def update(self) -> None:
        """Update all connection animations."""
        # Update animation progress for each connection
        for connection_key in list(self.animations.keys()):
            # Increment animation progress
            self.animations[connection_key] += self.animation_speed
            
            # Reset animation when it completes a cycle
            if self.animations[connection_key] >= 1.0:
                self.animations[connection_key] = 0.0
        
        # Update pulse effect
        self.pulse_time += self.pulse_speed
        if self.pulse_time >= 1.0:
            self.pulse_time = 0.0
    
    def render(self, surface: pygame.Surface, connections: List[Tuple[object, object]]) -> None:
        """
        Render animated connections.
        
        Args:
            surface: Pygame surface to render on
            connections: List of (source, target) node pairs
        """
        for source, target in connections:
            # Get connection points
            start_point = source.get_connection_point()
            end_point = target.get_connection_point()
            
            # Get connection key
            connection_key = (source.service_id, target.service_id)
            
            # Get animation progress (default to 0 if not found)
            progress = self.animations.get(connection_key, 0.0)
            
            # Draw animated connection
            self._draw_animated_connection(surface, start_point, end_point, progress)
    
    def _draw_animated_connection(
        self, 
        surface: pygame.Surface, 
        start: Tuple[int, int], 
        end: Tuple[int, int], 
        progress: float
    ) -> None:
        """
        Draw an animated connection with flowing color transitions.
        
        Args:
            surface: Pygame surface to render on
            start: Start point (x, y)
            end: End point (x, y)
            progress: Animation progress (0.0 to 1.0)
        """
        # Calculate line length
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        line_length = math.sqrt(dx * dx + dy * dy)
        
        # Calculate number of segments based on line length
        num_segments = max(5, int(line_length / 15))
        
        # Calculate pulse effect (0.0 to 1.0 and back)
        pulse_effect = (math.sin(self.pulse_time * math.pi * 2) + 1) / 2
        
        # Draw background line with pulse effect
        bg_width = 5 + int(pulse_effect * 2)  # Width varies between 5 and 7
        
        # Background color with pulse effect
        bg_alpha = 120 + int(pulse_effect * 60)  # Alpha varies between 120 and 180
        
        pygame.draw.line(
            surface,
            (*AWSColors.SQUID_INK, bg_alpha),  # Semi-transparent dark color with pulse
            start,
            end,
            bg_width
        )
        
        # Draw animated segments
        for i in range(num_segments):
            # Calculate segment position
            segment_progress = (i / num_segments + progress) % 1.0
            
            # Calculate segment start and end points
            segment_start_x = start[0] + dx * segment_progress
            segment_start_y = start[1] + dy * segment_progress
            
            segment_end_x = segment_start_x + dx / num_segments
            segment_end_y = segment_start_y + dy / num_segments
            
            # Ensure segment end doesn't exceed the line end
            if segment_progress + 1/num_segments > 1.0:
                segment_end_x = end[0]
                segment_end_y = end[1]
            
            # Choose color based on segment position with smooth transition
            # Use a sine wave to create a smooth color transition
            wave = (math.sin(segment_progress * math.pi * 2) + 1) / 2  # 0 to 1 value
            
            # Interpolate between AWS colors based on the wave value
            if wave < 0.33:
                # Transition from SMILE_ORANGE to POWDER_BLUE
                ratio = wave / 0.33
                color = (
                    int(AWSColors.SMILE_ORANGE[0] * (1 - ratio) + AWSColors.POWDER_BLUE[0] * ratio),
                    int(AWSColors.SMILE_ORANGE[1] * (1 - ratio) + AWSColors.POWDER_BLUE[1] * ratio),
                    int(AWSColors.SMILE_ORANGE[2] * (1 - ratio) + AWSColors.POWDER_BLUE[2] * ratio)
                )
            elif wave < 0.66:
                # Transition from POWDER_BLUE to LIME
                ratio = (wave - 0.33) / 0.33
                color = (
                    int(AWSColors.POWDER_BLUE[0] * (1 - ratio) + AWSColors.LIME[0] * ratio),
                    int(AWSColors.POWDER_BLUE[1] * (1 - ratio) + AWSColors.LIME[1] * ratio),
                    int(AWSColors.POWDER_BLUE[2] * (1 - ratio) + AWSColors.LIME[2] * ratio)
                )
            else:
                # Transition from LIME to SMILE_ORANGE
                ratio = (wave - 0.66) / 0.34
                color = (
                    int(AWSColors.LIME[0] * (1 - ratio) + AWSColors.SMILE_ORANGE[0] * ratio),
                    int(AWSColors.LIME[1] * (1 - ratio) + AWSColors.SMILE_ORANGE[1] * ratio),
                    int(AWSColors.LIME[2] * (1 - ratio) + AWSColors.SMILE_ORANGE[2] * ratio)
                )
            
            # Draw segment with glow effect
            # First draw a slightly thicker, semi-transparent line
            pygame.draw.line(
                surface,
                (*color, 100),  # Semi-transparent
                (segment_start_x, segment_start_y),
                (segment_end_x, segment_end_y),
                5
            )
            
            # Then draw the main segment
            pygame.draw.line(
                surface,
                color,
                (segment_start_x, segment_start_y),
                (segment_end_x, segment_end_y),
                3
            )
        
        # Draw arrow at the end to indicate direction
        self._draw_arrow(surface, start, end, AWSColors.SMILE_ORANGE)
    
    def _draw_arrow(
        self, 
        surface: pygame.Surface, 
        start: Tuple[int, int], 
        end: Tuple[int, int], 
        color: Tuple[int, int, int]
    ) -> None:
        """
        Draw an arrow at the end of a line to indicate direction.
        
        Args:
            surface: Pygame surface to render on
            start: Start point of the line (x, y)
            end: End point of the line (x, y)
            color: Arrow color (RGB)
        """
        # Calculate direction vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # Normalize direction vector
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
        
        dx /= length
        dy /= length
        
        # Calculate perpendicular vector
        perpendicular_x = -dy
        perpendicular_y = dx
        
        # Arrow size
        arrow_size = 10
        
        # Calculate arrow points
        arrow_point1 = (
            end[0] - dx * arrow_size + perpendicular_x * arrow_size/2,
            end[1] - dy * arrow_size + perpendicular_y * arrow_size/2
        )
        
        arrow_point2 = (
            end[0] - dx * arrow_size - perpendicular_x * arrow_size/2,
            end[1] - dy * arrow_size - perpendicular_y * arrow_size/2
        )
        
        # Draw arrow with glow effect
        # First draw a slightly larger, semi-transparent arrow for glow
        glow_points = [
            end,
            (end[0] - dx * (arrow_size+2) + perpendicular_x * (arrow_size+2)/2,
             end[1] - dy * (arrow_size+2) + perpendicular_y * (arrow_size+2)/2),
            (end[0] - dx * (arrow_size+2) - perpendicular_x * (arrow_size+2)/2,
             end[1] - dy * (arrow_size+2) - perpendicular_y * (arrow_size+2)/2)
        ]
        
        pygame.draw.polygon(
            surface,
            (*color, 100),  # Semi-transparent
            glow_points
        )
        
        # Draw main arrow
        pygame.draw.polygon(
            surface,
            color,
            [end, arrow_point1, arrow_point2]
        )