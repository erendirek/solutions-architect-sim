"""
Game state management module.
"""
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Any


class GameMode(Enum):
    """Game modes available in the simulator."""
    NORMAL = auto()
    TUTORIAL = auto()
    TIME_TRIAL = auto()


class GameState:
    """Class to manage the game state."""
    
    def __init__(self) -> None:
        """Initialize the game state."""
        # Current game mode
        self.mode: GameMode = GameMode.NORMAL
        
        # Level progress
        self.current_level_id: int = 1
        self.unlocked_levels: Set[int] = {1}  # Start with level 1 unlocked
        self.completed_levels: Dict[int, int] = {}  # level_id -> score
        
        # Current level state
        self.placed_services: List[str] = []
        self.connections: List[Tuple[str, str]] = []
        self.score: int = 0
        self.time_remaining: Optional[int] = None  # Only used in time trial mode
        
        # Player profile
        self.player_name: str = "Architect"
        self.total_score: int = 0
        self.highest_rank: str = "Bronze"
        
        # For debugging/development, unlock all levels if specified in config
        self._check_debug_unlock()
    
    def _check_debug_unlock(self) -> None:
        """Check if all levels should be unlocked for debugging."""
        try:
            import json
            import os
            
            config_path = os.path.join("config", "game_config.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                    if config.get("debug", {}).get("unlock_all_levels", False):
                        self.unlocked_levels = set(range(1, 11))  # Unlock levels 1-10
        except Exception:
            # Silently fail if there's an issue loading the config
            pass
    
    def reset_level(self) -> None:
        """Reset the current level state."""
        self.placed_services = []
        self.connections = []
        self.score = 0
        
        # Only reset time_remaining if not in TIME_TRIAL mode
        if self.mode != GameMode.TIME_TRIAL:
            self.time_remaining = None
    
    def complete_level(self, level_id: int, score: int) -> None:
        """
        Mark a level as completed with the given score.
        
        Args:
            level_id: ID of the completed level
            score: Score achieved in the level
        """
        # Update the completed levels dictionary
        if level_id not in self.completed_levels or score > self.completed_levels[level_id]:
            self.completed_levels[level_id] = score
        
        # Unlock the next level if available
        if level_id < 10:  # Assuming 10 is the maximum level
            self.unlocked_levels.add(level_id + 1)
        
        # Update total score
        self.total_score = sum(self.completed_levels.values())
        
        # Update highest rank
        rank = self.get_rank_for_score(score)
        if rank == "Gold" or (rank == "Silver" and self.highest_rank == "Bronze"):
            self.highest_rank = rank
    
    def get_rank_for_score(self, score: int) -> str:
        """
        Get the architect rank for a given score.
        
        Args:
            score: The score to evaluate
            
        Returns:
            Rank as a string: "Gold", "Silver", or "Bronze"
        """
        if score >= 250:
            return "Gold"
        elif score >= 150:
            return "Silver"
        else:
            return "Bronze"