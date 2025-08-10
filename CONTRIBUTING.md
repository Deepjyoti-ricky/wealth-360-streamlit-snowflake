# Contributing to Wealth 360 Streamlit

We welcome contributions to improve this BFSI analytics application! Please follow these guidelines to ensure a smooth collaboration process.

## Code of Conduct

This project adheres to a professional code of conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Set up your development environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

## Development Guidelines

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write docstrings for all functions and classes
- Maintain test coverage above 80%

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for adding tests

### Pull Request Process
1. Ensure all tests pass: `pytest`
2. Run linting: `black . && flake8`
3. Update documentation if needed
4. Create a clear PR description explaining changes
5. Link any related issues

## Testing

- Write unit tests for new functions
- Test both Snowpark session modes (active session vs. credentials)
- Ensure UI components render correctly
- Test with sample data scenarios

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Include usage examples for new features

## Questions?

Open an issue for questions or discussion before starting major changes.

## Contact

For direct questions or collaboration opportunities:

**Deepjyoti Dev**
Senior Data Cloud Architect, Snowflake GXC Team
📧 deepjyoti.dev@snowflake.com
📱 +917205672310
