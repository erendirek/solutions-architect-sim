"""
Base level module defining the common interface for all game levels.
"""
from abc import ABC, abstractmethod
import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple

import pygame

from services.service_node import ServiceNode


class BaseLevel(ABC):
    """Abstract base class for all game levels."""
    
    def __init__(self, game: Any) -> None:
        """
        Initialize the base level.
        
        Args:
            game: Reference to the main game object
        """
        self.game = game
        self.level_id: int = 0
        self.title: str = "Base Level"
        self.description: str = "Base level description"
        self.objective: str = "Complete the level objective"
        
        # Level requirements
        self.required_services: Set[str] = set()
        self.optional_services: Set[str] = set()
        self.available_services: Set[str] = set()
        self.budget: float = 1000.0
        self.max_latency: float = 500.0  # in ms
        
        # Level state
        self.placed_service_nodes: List[ServiceNode] = []
        self.connections: List[Tuple[ServiceNode, ServiceNode]] = []
        self.tutorial_steps: List[str] = []
        self.current_tutorial_step: int = 0
        
        # Canvas dimensions
        self.canvas_rect = pygame.Rect(
            self.game.config.ui.service_panel_width + self.game.config.ui.canvas_padding,
            self.game.config.ui.canvas_padding,
            self.game.config.window.width - self.game.config.ui.service_panel_width - 2 * self.game.config.ui.canvas_padding,
            self.game.config.window.height - self.game.config.ui.hud_height - 2 * self.game.config.ui.canvas_padding
        )
        
        # Service panel rect for removing services
        self.service_panel_rect = pygame.Rect(
            0, 0, 
            self.game.config.ui.service_panel_width,
            self.game.config.window.height - self.game.config.ui.hud_height
        )
    
    def load_level_data(self, level_id: int) -> bool:
        """
        Load level data from the central levels.json file.
        
        Args:
            level_id: ID of the level to load
            
        Returns:
            True if level data was loaded successfully, False otherwise
        """
        try:
            # Load level data from JSON file
            levels_file = os.path.join("config", "levels.json")
            if not os.path.exists(levels_file):
                print(f"Error: {levels_file} not found")
                return False
                
            with open(levels_file, "r") as f:
                levels_data = json.load(f)
            
            # Find the level with the matching ID
            level_data = None
            for level in levels_data.get("levels", []):
                if level.get("id") == level_id:
                    level_data = level
                    break
            
            if not level_data:
                print(f"Error: Level {level_id} not found in levels.json")
                return False
            
            # Set level properties from the loaded data
            self.level_id = level_data.get("id", 0)
            self.title = level_data.get("title", "Unknown Level")
            self.description = level_data.get("description", "No description available")
            self.objective = level_data.get("objective", "No objective specified")
            
            self.required_services = set(level_data.get("required_services", []))
            self.optional_services = set(level_data.get("optional_services", []))
            self.available_services = set(level_data.get("available_services", []))
            
            self.budget = level_data.get("budget", 1000.0)
            self.max_latency = level_data.get("max_latency", 500.0)
            
            self.tutorial_steps = level_data.get("tutorial_steps", [])
            
            return True
            
        except Exception as e:
            print(f"Error loading level data: {e}")
            return False
    
    def update_connections(self) -> None:
        """Update connections when service nodes are moved."""
        # No need to update the connections list itself as it contains references to the nodes
        # The nodes' positions are updated automatically when they are moved
        pass
    
    def remove_service(self, node: ServiceNode) -> None:
        """
        Remove a service node and all its connections.
        
        Args:
            node: The service node to remove
        """
        if node in self.placed_service_nodes:
            # Store the service ID before removing the node
            service_id = node.service_id
            
            # Remove all connections involving this node
            self.connections = [
                (source, target) for source, target in self.connections
                if source != node and target != node
            ]
            
            # Update game state connections
            self.game.state.connections = [
                (source_id, target_id) for source_id, target_id in self.game.state.connections
                if source_id != service_id and target_id != service_id
            ]
            
            # Remove the node from placed services
            self.placed_service_nodes.remove(node)
            
            # Remove from game state
            # We need to handle the case where multiple instances of the same service might exist
            # Count occurrences of this service type in remaining nodes
            remaining_count = sum(1 for n in self.placed_service_nodes if n.service_id == service_id)
            
            # Count occurrences in the game state
            state_count = self.game.state.placed_services.count(service_id)
            
            # If we have more in state than remaining nodes, remove one
            if state_count > remaining_count:
                self.game.state.placed_services.remove(service_id)
    
    def remove_connection(self, source: ServiceNode, target: ServiceNode) -> bool:
        """
        Remove a connection between two service nodes.
        
        Args:
            source: Source service node
            target: Target service node
            
        Returns:
            True if connection was removed, False if not found
        """
        # Check if the connection exists
        connection = next(((s, t) for s, t in self.connections if s == source and t == target), None)
        if connection:
            # Remove from connections list
            self.connections.remove(connection)
            
            # Remove from game state
            state_connection = (source.service_id, target.service_id)
            if state_connection in self.game.state.connections:
                self.game.state.connections.remove(state_connection)
            
            return True
        
        return False
    
    def get_connection_at_point(self, pos: Tuple[int, int], tolerance: int = 10) -> Optional[Tuple[ServiceNode, ServiceNode]]:
        """
        Find a connection near the given point.
        
        Args:
            pos: Position to check (x, y)
            tolerance: Distance tolerance in pixels
            
        Returns:
            Tuple of (source, target) nodes if found, None otherwise
        """
        for source, target in self.connections:
            # Get connection points
            start = source.get_connection_point()
            end = target.get_connection_point()
            
            # Calculate distance from point to line segment
            distance = self._point_to_line_distance(pos, start, end)
            
            if distance <= tolerance:
                return (source, target)
        
        return None
    
    def _point_to_line_distance(self, point: Tuple[int, int], line_start: Tuple[int, int], line_end: Tuple[int, int]) -> float:
        """
        Calculate the distance from a point to a line segment.
        
        Args:
            point: The point (x, y)
            line_start: Start point of the line (x, y)
            line_end: End point of the line (x, y)
            
        Returns:
            Distance in pixels
        """
        import math
        
        # Convert to vectors
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Calculate line length squared
        line_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
        
        # If line is a point, return distance to that point
        if line_length_sq == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        
        # Calculate projection of point onto line
        t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / line_length_sq))
        
        # Calculate closest point on line
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        
        # Return distance to closest point
        return math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)
    
    @abstractmethod
    def update(self) -> None:
        """Update the level state."""
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the level.
        
        Args:
            surface: Pygame surface to render on
        """
        pass
    
    def get_canvas_rect(self) -> pygame.Rect:
        """
        Get the rectangle representing the canvas area.
        
        Returns:
            Pygame Rect object for the canvas area
        """
        return self.canvas_rect
    
    def get_service_at_panel(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Get the service at the given position in the service panel.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            Service ID if found, None otherwise
        """
        # This will be implemented by concrete level classes
        return None
    
    def get_service_node_at_canvas(self, pos: Tuple[int, int]) -> Optional[ServiceNode]:
        """
        Get the service node at the given position on the canvas.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            ServiceNode if found, None otherwise
        """
        for node in self.placed_service_nodes:
            if node.rect.collidepoint(pos):
                return node
        return None
    
    def get_service_node_at_point(self, point: Tuple[int, int]) -> Optional[ServiceNode]:
        """
        Get the service node that has a connection point at the given position.
        
        Args:
            point: Point position (x, y)
            
        Returns:
            ServiceNode if found, None otherwise
        """
        for node in self.placed_service_nodes:
            if node.get_connection_point() == point:
                return node
        return None
    
    def place_service(self, service_id: str, pos: Tuple[int, int]) -> None:
        """
        Place a service on the canvas.
        
        Args:
            service_id: ID of the service to place
            pos: Position (x, y) to place the service
        """
        from services.service_registry import ServiceRegistry
        
        service_info = ServiceRegistry.get_service(service_id)
        if service_info:
            node = ServiceNode(service_id, service_info, pos)
            self.placed_service_nodes.append(node)
            self.game.state.placed_services.append(service_id)
    
    def create_connection(self, source: ServiceNode, target: ServiceNode) -> bool:
        """
        Create a connection between two service nodes.
        
        Args:
            source: Source service node
            target: Target service node
            
        Returns:
            True if connection was created, False otherwise
        """
        from services.connection_validator import ConnectionValidator
        
        # Check if connection is valid
        validation_result = ConnectionValidator.validate_connection(
            source.service_id, target.service_id
        )
        
        if validation_result.is_valid:
            # Add the connection
            self.connections.append((source, target))
            self.game.state.connections.append((source.service_id, target.service_id))
            
            # Update score
            self.game.state.score += self.game.config.game.scoring.correct_connection
            
            return True
        else:
            # Show error message
            self.game.ui_manager.show_message(validation_result.message)
            return False
    
    def validate_architecture(self) -> Tuple[bool, str, int]:
        """
        Validate the current architecture against level requirements.
        
        Returns:
            Tuple of (is_valid, message, score_adjustment)
        """
        # Check if all required services are placed
        missing_services = self.required_services - set(self.game.state.placed_services)
        if missing_services:
            return (
                False,
                f"Missing required services: {', '.join(missing_services)}",
                0
            )
        
        # Check for unnecessary services
        unnecessary_services = []
        for service in self.game.state.placed_services:
            if service not in self.required_services and service not in self.optional_services:
                unnecessary_services.append(service)
                
        score_adjustment = 0
        if unnecessary_services:
            score_adjustment += len(unnecessary_services) * self.game.config.game.scoring.unnecessary_service
        
        # Run security audit
        from tests.security_audit import SecurityAudit
        security_issues = SecurityAudit.audit_architecture(
            self.game.state.placed_services,
            self.game.state.connections
        )
        
        if security_issues:
            score_adjustment += len(security_issues) * self.game.config.game.scoring.security_violation
            return (
                False,
                f"Security issues found: {security_issues[0]}",
                score_adjustment
            )
        
        # Check cost
        from tests.cost_estimator import CostEstimator
        estimated_cost = CostEstimator.estimate_monthly_cost(
            self.game.state.placed_services,
            self.game.state.connections
        )
        
        if estimated_cost > self.budget:
            return (
                False,
                f"Architecture exceeds budget: ${estimated_cost:.2f} > ${self.budget:.2f}",
                score_adjustment
            )
        
        # Check performance
        from tests.performance_test import PerformanceTest
        estimated_latency = PerformanceTest.estimate_latency(
            self.game.state.placed_services,
            self.game.state.connections
        )
        
        if estimated_latency > self.max_latency:
            return (
                False,
                f"Architecture exceeds max latency: {estimated_latency:.2f}ms > {self.max_latency:.2f}ms",
                score_adjustment
            )
        
        # Architecture is valid
        score_adjustment += self.game.config.game.scoring.requirements_fulfilled
        
        # Check for cost optimization bonus
        if estimated_cost < self.budget * 0.8:
            score_adjustment += self.game.config.game.scoring.cost_optimization
        
        return (
            True,
            "Architecture validated successfully!",
            score_adjustment
        )