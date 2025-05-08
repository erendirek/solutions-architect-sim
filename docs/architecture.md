# Solutions Architect Simulator - Architecture

This document describes the high-level architecture of the Solutions Architect Simulator game.

## Overview

The Solutions Architect Simulator is built using pygame and follows object-oriented design principles. The code is organized into several modules, each with a specific responsibility.

## Module Structure

### Core

The `core` module contains the main game loop, event handling, and base classes:

- `game.py`: Main game class that manages the game loop and state
- `config.py`: Configuration classes and loading
- `state.py`: Game state management
- `event_handler.py`: Event handling and dispatching
- `level_manager.py`: Level loading and management

### Levels

The `levels` module contains level definitions:

- `base_level.py`: Abstract base class for all levels
- `level_1.py`, `level_2.py`, etc.: Individual level implementations

### Services

The `services` module defines AWS service models:

- `service_registry.py`: Registry of all AWS services
- `service_node.py`: Representation of a service on the canvas
- `connection_validator.py`: Validates connections between services

### UI

The `ui` module contains UI components:

- `ui_manager.py`: Manages all UI components
- `button.py`: Button component
- `tooltip.py`: Tooltip component
- `message_box.py`: Message box component
- `hud.py`: Heads-up display component

### Tests

The `tests` module contains evaluation scripts:

- `security_audit.py`: Checks for security issues
- `cost_estimator.py`: Estimates architecture cost
- `performance_test.py`: Evaluates architecture performance

## Data Flow

1. The main game loop runs in `Game.run()`
2. Events are processed by `EventHandler`
3. Game state is updated in `Game.update()`
4. The current level is rendered in `Game.render()`
5. UI components are rendered on top of the level

## Configuration

Game configuration is stored in JSON files:

- `config/game_config.json`: General game settings
- `config/services.json`: AWS service definitions
- `config/levels.json`: Level definitions

## Class Diagram

```
Game
├── EventHandler
├── LevelManager
│   └── BaseLevel (abstract)
│       ├── Level1
│       ├── Level2
│       └── ...
├── UIManager
│   ├── Button
│   ├── Tooltip
│   ├── MessageBox
│   └── HUD
└── GameState

ServiceRegistry
└── ServiceInfo

ServiceNode

ConnectionValidator
└── ValidationResult

SecurityAudit
CostEstimator
PerformanceTest
```