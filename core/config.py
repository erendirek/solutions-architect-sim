"""
Configuration module for the Solutions Architect Simulator.
"""
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class WindowConfig:
    """Window configuration settings."""
    width: int
    height: int
    title: str
    fps: int


@dataclass
class UIConfig:
    """UI configuration settings."""
    service_panel_width: int
    hud_height: int
    canvas_padding: int
    tooltip_delay_ms: int


@dataclass
class ScoringConfig:
    """Scoring configuration settings."""
    requirements_fulfilled: int
    correct_connection: int
    security_violation: int
    unnecessary_service: int
    cost_optimization: int


@dataclass
class ScoreThresholds:
    """Score thresholds for different architect ranks."""
    bronze: int
    silver: int


@dataclass
class GameplayConfig:
    """Gameplay configuration settings."""
    starting_level: int
    max_levels: int
    time_trial_seconds: int
    score_thresholds: ScoreThresholds
    scoring: ScoringConfig


@dataclass
class DebugConfig:
    """Debug configuration settings."""
    enabled: bool
    show_fps: bool
    unlock_all_levels: bool


@dataclass
class GameConfig:
    """Main game configuration."""
    window: WindowConfig
    ui: UIConfig
    game: GameplayConfig
    debug: DebugConfig
    
    @classmethod
    def load_from_file(cls, file_path: str) -> "GameConfig":
        """
        Load game configuration from a JSON file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            GameConfig object with settings from the file
        """
        with open(file_path, "r") as f:
            config_data = json.load(f)
        
        window = WindowConfig(**config_data["window"])
        ui = UIConfig(**config_data["ui"])
        
        score_thresholds = ScoreThresholds(**config_data["game"]["score_thresholds"])
        scoring = ScoringConfig(**config_data["game"]["scoring"])
        
        game = GameplayConfig(
            starting_level=config_data["game"]["starting_level"],
            max_levels=config_data["game"]["max_levels"],
            time_trial_seconds=config_data["game"]["time_trial_seconds"],
            score_thresholds=score_thresholds,
            scoring=scoring
        )
        
        debug = DebugConfig(**config_data["debug"])
        
        return cls(
            window=window,
            ui=ui,
            game=game,
            debug=debug
        )