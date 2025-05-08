"""
Level factory module for creating level instances.
"""
from typing import Any, Dict, Optional, Type

from levels.base_level import BaseLevel
from levels.level_1 import Level1
from levels.level_2 import Level2


class LevelFactory:
    """Factory for creating level instances."""
    
    # Registry of level classes
    _level_classes: Dict[int, Type[BaseLevel]] = {
        1: Level1,
        2: Level2,
    }
    
    @classmethod
    def create_level(cls, level_id: int, game: Any) -> Optional[BaseLevel]:
        """
        Create a level instance for the given level ID.
        
        Args:
            level_id: ID of the level to create
            game: Reference to the main game object
            
        Returns:
            Level instance if the level ID is valid, None otherwise
        """
        level_class = cls._level_classes.get(level_id)
        if level_class:
            return level_class(game)
        return None
    
    @classmethod
    def register_level(cls, level_id: int, level_class: Type[BaseLevel]) -> None:
        """
        Register a level class for a given level ID.
        
        Args:
            level_id: ID of the level
            level_class: Level class to register
        """
        cls._level_classes[level_id] = level_class