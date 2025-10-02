# Contributing to File to Image Encoder/Decoder

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/file-to-image.git`
3. **Install** dependencies: `pip install -r requirements.txt`
4. **Create** a new branch: `git checkout -b feature/your-feature-name`
5. **Make** your changes
6. **Test** your changes: `python -m pytest tests/ -v`
7. **Commit** your changes: `git commit -m "Add your feature"`
8. **Push** to your fork: `git push origin feature/your-feature-name`
9. **Create** a Pull Request

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate (for Python 3.8+ compatibility)

### Code Formatting
We use the following tools to maintain consistent code style:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

Run these before committing:
```bash
black .
isort .
flake8 .
```

### Testing
- Write tests for all new functionality
- Ensure all existing tests pass
- Aim for high test coverage
- Test edge cases and error conditions

Run tests:
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_encode.py -v
```

### Documentation
- Update README.md if you add new features
- Add docstrings to new functions
- Update code examples if the API changes
- Keep documentation clear and concise

## 🐛 Bug Reports

When filing an issue, please include:

1. **Environment**: Python version, OS, dependencies
2. **Steps to reproduce**: Clear, minimal steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Error messages**: Full traceback if applicable
6. **Sample files**: If relevant, include small test files

## 💡 Feature Requests

For new feature requests:

1. Check if it's already requested in issues
2. Explain the use case and benefits
3. Consider implementation complexity
4. Be open to feedback and iteration

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- git

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/file-to-image.git
cd file-to-image

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black isort flake8

# Run tests to ensure everything works
python -m pytest tests/ -v
```

### Project Structure
```
file-to-image/
├── Encode.py           # Main encoding script
├── Decode.py           # Main decoding script
├── requirements.txt    # Production dependencies
├── setup.py           # Package setup
├── tests/             # Test suite
│   ├── test_encode.py
│   ├── test_decode.py
│   └── test_data/
├── Sample/            # Sample files
├── .github/           # GitHub workflows
└── docs/              # Documentation
```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- **Performance improvements**: Optimize encoding/decoding speed
- **Memory optimization**: Reduce memory usage for large files
- **Error handling**: Improve error messages and edge case handling
- **Documentation**: Improve README, add tutorials, API docs

### Medium Priority
- **New features**: GUI interface, batch processing, progress bars
- **File format support**: Support for other image formats (TIFF, BMP)
- **Compression**: Optional compression to reduce image size
- **Encryption**: Add optional encryption for security

### Low Priority
- **Platform-specific optimizations**: Platform-specific improvements
- **Additional tests**: More comprehensive test coverage
- **Examples**: More usage examples and tutorials
- **Localization**: Support for different languages

## 📝 Pull Request Process

1. **Ensure tests pass**: All existing and new tests must pass
2. **Update documentation**: Update relevant documentation
3. **Add tests**: Include tests for new functionality
4. **Follow style guide**: Ensure code follows project conventions
5. **Write clear commit messages**: Use descriptive commit messages
6. **Keep PR focused**: One feature/fix per PR when possible

### PR Checklist
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] No breaking changes (or clearly documented)
- [ ] Related issues referenced
- [ ] Self-review completed

### Commit Message Format
Use clear, descriptive commit messages:
```
Add support for TIFF image format

- Implement TIFF encoding in Encode.py
- Add TIFF decoding in Decode.py  
- Update tests for TIFF support
- Add TIFF examples to README

Fixes #123
```

## 🤝 Code of Conduct

This project follows a simple code of conduct:

- **Be respectful**: Treat all contributors with respect
- **Be inclusive**: Welcome people of all backgrounds and skill levels
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor stats

## ❓ Questions?

- Check existing [Issues](https://github.com/yourusername/file-to-image/issues)
- Create a new issue with the "question" label
- Review the [README.md](README.md) for basic usage

## 📚 Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [pytest Documentation](https://docs.pytest.org/)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

---

Thank you for contributing! 🎉