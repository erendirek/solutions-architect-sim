# Solutions Architect Simulator

An interactive educational game that teaches AWS architecture principles through hands-on challenges.

This project was built as part of the [Amazon Q Developer "Quack The Code" Challenge – Crushing the Command Line](https://dev.to/challenges/aws-amazon-q-v2025-04-30).

## Overview

Solutions Architect Simulator is a pygame-based educational game where players design AWS architectures to solve real-world scenarios. The game features 10 progressive levels, each focusing on different AWS services and architectural patterns.

## Features

- 10 progressive levels with increasing complexity
- Drag-and-drop interface for AWS services
- Real-time validation of architecture connections
- Scoring system based on security, cost optimization, and performance
- Multiple gameplay modes including tutorials and time trials
- Automated evaluation of architectures

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/solutions-architect-simulator.git

# Navigate to the project directory
cd solutions-architect-simulator

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Project Structure

- `core/`: Main game loop, event handling, and base classes
- `levels/`: Level definitions with scenarios and requirements
- `services/`: AWS service models and connection rules
- `ui/`: Pygame UI components
- `tests/`: Automated evaluation scripts
- `assets/`: Game assets including images and sounds

## License

MIT
