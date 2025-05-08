# Contributing to Solutions Architect Simulator

Thank you for your interest in contributing to the Solutions Architect Simulator project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/solutions-architect-simulator.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin feature/your-feature-name`
8. Submit a pull request

## Development Environment

1. Install Python 3.8 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Download AWS service icons and place them in `assets/images/services/`
4. Run the game: `python main.py`

## Code Style

This project follows PEP 8 style guidelines with the following additions:

- Use type hints for all function parameters and return values
- Use docstrings for all modules, classes, and functions
- Maximum line length is 88 characters
- Use double quotes for strings

You can check your code style with:

```bash
black --check .
mypy .
```

## Testing

Write tests for all new features and bug fixes. Run tests with:

```bash
pytest tests/
```

## Documentation

Update documentation when making changes:

- Update docstrings for modified code
- Update README.md if necessary
- Update relevant documentation in the `docs/` directory

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as necessary
3. Add tests for new features
4. Ensure all tests pass
5. Update the README.md with details of changes if applicable
6. The pull request will be merged once it has been reviewed and approved

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We welcome contributions from everyone, regardless of experience level.