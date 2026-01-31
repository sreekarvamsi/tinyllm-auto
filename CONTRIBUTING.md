# Contributing to TinyLLM-Auto

Thank you for your interest in contributing to TinyLLM-Auto! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- System information (OS, Python version, hardware specs)
- Relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Potential implementation approach (optional)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code formatting
   black src/
   
   # Check linting
   flake8 src/
   ```

4. **Submit the pull request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure CI checks pass

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tinyllm-auto.git
cd tinyllm-auto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Download model for testing
python scripts/download_model.py
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters

### Documentation
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update API documentation for interface changes

### Testing
- Write unit tests for new functionality
- Maintain test coverage above 80%
- Test on multiple platforms when possible

## Project Structure

```
tinyllm-auto/
├── src/              # Source code
├── tests/            # Test files
├── scripts/          # Utility scripts
├── docs/             # Documentation
└── data/             # Data files and benchmarks
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Fine-tuning on automotive datasets
- [ ] Multi-language support
- [ ] CAN bus integration
- [ ] Additional benchmarks

### Medium Priority
- [ ] Voice activity detection
- [ ] Personalized driver profiles
- [ ] Web-based configuration UI
- [ ] Docker deployment

### Nice to Have
- [ ] Mobile app integration
- [ ] Cloud sync capabilities
- [ ] Advanced diagnostics
- [ ] Video tutorials

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in existing issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to TinyLLM-Auto! 🚗🤖
