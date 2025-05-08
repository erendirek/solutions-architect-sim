# Solutions Architect Simulator - Development Guide

This document provides guidelines for developers working on the Solutions Architect Simulator project.

## Project Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download AWS service icons and place them in `assets/images/services/`
4. Run the game: `python main.py`

## Code Style

This project follows PEP 8 style guidelines with the following additions:

- Use type hints for all function parameters and return values
- Use docstrings for all modules, classes, and functions
- Maximum line length is 88 characters
- Use double quotes for strings

## Adding a New Level

To add a new level to the game:

1. Create a new file in the `levels` directory (e.g., `level_11.py`)
2. Define a class that inherits from `BaseLevel`
3. Implement the required methods: `__init__`, `update`, `render`, and `get_service_at_panel`
4. Add the level configuration to `config/levels.json`

Example:

```python
from typing import Any, Dict, List, Optional, Set, Tuple
import pygame
from levels.base_level import BaseLevel
from services.service_registry import ServiceRegistry

class Level11(BaseLevel):
    """Level 11: Your level description."""
    
    def __init__(self, game: Any) -> None:
        """Initialize Level 11."""
        super().__init__(game)
        
        self.level_id = 11
        self.title = "Your Level Title"
        self.description = "Your level description."
        self.objective = "Your level objective."
        
        # Level requirements
        self.required_services = {"service1", "service2"}
        self.optional_services = {"service3", "service4"}
        self.available_services = {"service1", "service2", "service3", "service4", "service5"}
        self.budget = 100.0
        self.max_latency = 200.0
        
        # Load service icons
        self._load_service_icons()
    
    # Implement other required methods
```

## Adding a New AWS Service

To add a new AWS service to the game:

1. Add the service definition to `config/services.json`
2. Place the service icon in `assets/images/services/`

Example service definition:

```json
"new_service": {
  "display_name": "New Service",
  "description": "Description of the new service.",
  "category": "compute",
  "icon_path": "assets/images/services/new_service.png",
  "cost_per_hour": 0.05,
  "latency_ms": 10.0,
  "connection_rules": {
    "direct": ["service1", "service2"],
    "requires": []
  }
}
```

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Building Executable

To build a standalone executable:

```bash
pyinstaller --onefile --windowed main.py
```