# Contributing to Chord DHT Graph Visualization

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

Before creating a bug report, please check the existing issues to avoid duplicates.

**To submit a bug report:**

1. Use the GitHub issue tracker
2. Provide a clear and descriptive title
3. Include steps to reproduce the issue
4. Provide system information (OS, Python version, etc.)
5. Include relevant logs or error messages
6. Add screenshots if applicable

**Bug Report Template:**
```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Python version: [e.g. 3.9.5]
 - Package versions: [output of pip freeze]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

1. A clear and descriptive title
2. Detailed description of the proposed functionality
3. Rationale for why this enhancement would be useful
4. Possible implementation approaches
5. Examples of how it would be used

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** before submitting
6. **Submit a pull request** with a clear description

## 🛠️ Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Graphviz (system dependency)

### Setup Instructions

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/Chord-DHT-graphi-viz.git
cd Chord-DHT-graphi-viz
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies:**
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

4. **Install the package in development mode:**
```bash
pip install -e .
```

5. **Verify installation:**
```bash
python -m pytest tests/  # Run tests
python Main.py --help    # Test main application
```

### Development Workflow

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the coding standards

3. **Run tests frequently:**
```bash
python -m pytest tests/
```

4. **Format your code:**
```bash
black *.py
```

5. **Lint your code:**
```bash
flake8 *.py
```

6. **Commit your changes:**
```bash
git add .
git commit -m "Add your descriptive commit message"
```

7. **Push and create a pull request:**
```bash
git push origin feature/your-feature-name
```

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length:** Maximum 88 characters (Black's default)
- **Indentation:** 4 spaces (no tabs)
- **Quotes:** Prefer double quotes for strings
- **Imports:** Group imports (standard library, third-party, local)

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format all Python files
black *.py

# Check formatting without making changes
black --check *.py
```

### Linting

We use **Flake8** for linting:

```bash
# Lint all Python files
flake8 *.py

# With specific configuration
flake8 --max-line-length=88 --extend-ignore=E203,W503 *.py
```

### Type Hints

We encourage the use of type hints for new code:

```python
from typing import List, Dict, Optional

def process_nodes(node_ids: List[int]) -> Dict[int, str]:
    """Process a list of node IDs and return a mapping."""
    return {node_id: f"node_{node_id}" for node_id in node_ids}
```

### Documentation

#### Docstrings

Use Google-style docstrings for all public functions and classes:

```python
def find_successor(self, key: int) -> 'Node':
    """Find the successor node for a given key.
    
    Args:
        key: The key to find the successor for.
        
    Returns:
        The successor node responsible for the key.
        
    Raises:
        NetworkError: If the network is in an invalid state.
        
    Example:
        >>> node = network.first_node
        >>> successor = node.find_successor(42)
        >>> print(f"Node {successor.node_id} is responsible for key 42")
    """
```

#### Comments

- Use comments sparingly and only when the code is not self-explanatory
- Prefer descriptive variable and function names over comments
- Use TODO comments for known improvements needed

### Testing

#### Test Structure

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names: `test_function_name_expected_behavior`

#### Test Guidelines

```python
import pytest
from Node import Node
from Network import Network

class TestChordNetwork:
    """Test suite for Chord network functionality."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.m = 4
        self.node_ids = [0, 4, 8, 12]
        Node.m = self.m
        Node.ring_size = 2 ** self.m
        self.network = Network(self.m, self.node_ids)
    
    def test_node_insertion_success(self):
        """Test successful node insertion into the network."""
        node_id = 2
        initial_count = len(self.network.nodes)
        
        self.network.insert_node(node_id)
        
        assert len(self.network.nodes) == initial_count + 1
        assert any(node.node_id == node_id for node in self.network.nodes)
    
    def test_data_insertion_and_lookup(self):
        """Test data insertion and successful lookup."""
        test_data = "test_file.txt"
        
        self.network.insert_data(test_data)
        result = self.network.find_data(test_data)
        
        assert result == test_data
```

#### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.

# Run specific test file
python -m pytest tests/test_network.py

# Run with verbose output
python -m pytest tests/ -v

# Run only tests matching pattern
python -m pytest tests/ -k "test_insertion"
```

## 🏗️ Project Structure

```
Chord-DHT-graphi-viz/
├── Main.py              # Main application entry point
├── Network.py           # Network management and operations
├── Node.py              # Individual node implementation
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── setup.py             # Package setup configuration
├── config.ini           # Default configuration
├── LICENSE              # MIT license
├── .gitignore           # Git ignore patterns
├── examples/            # Example scripts and tutorials
│   ├── basic_example.py
│   └── performance_test.py
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_node.py
│   ├── test_network.py
│   └── test_integration.py
├── docs/                # Additional documentation
└── backups/             # Network backup files
```

## 📋 Commit Message Guidelines

We follow the conventional commit format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat:** A new feature
- **fix:** A bug fix
- **docs:** Documentation only changes
- **style:** Code style changes (formatting, missing semicolons, etc.)
- **refactor:** Code change that neither fixes a bug nor adds a feature
- **perf:** Performance improvements
- **test:** Adding missing tests or correcting existing tests
- **build:** Changes to build system or external dependencies
- **ci:** Changes to CI configuration files and scripts

### Examples

```
feat: add load balancing algorithm for network optimization

fix: resolve finger table inconsistency during node departure

docs: add comprehensive API documentation for Network class

test: add integration tests for node join/leave scenarios
```

## 🔍 Code Review Process

1. **Automated checks** must pass (tests, linting, formatting)
2. **At least one approval** from a maintainer required
3. **All conversations resolved** before merging
4. **Squash and merge** for feature branches
5. **Delete feature branch** after successful merge

### Review Checklist

**For Authors:**
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact considered
- [ ] Security implications reviewed

**For Reviewers:**
- [ ] Code is readable and maintainable
- [ ] Logic is correct and efficient
- [ ] Edge cases are handled
- [ ] Tests are comprehensive
- [ ] Documentation is accurate
- [ ] No security vulnerabilities

## 🐛 Debugging Guidelines

### Logging

Use the built-in logging system for debugging:

```python
import logging

# In your code
logging.info("Node joining network")
logging.warning("High load detected on node %d", node_id)
logging.error("Failed to contact node %d: %s", node_id, error)
logging.debug("Finger table: %s", finger_table)
```

### Common Issues

1. **Import errors:** Ensure all dependencies are installed
2. **Graphviz errors:** Install system Graphviz package
3. **Network inconsistencies:** Check finger table integrity
4. **Performance issues:** Enable profiling in config

### Debug Mode

Enable debug mode in `config.ini`:

```ini
[development]
debug_mode = true
verbose = true
```

## 📞 Getting Help

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and general discussion
- **Documentation:** Check README.md and inline documentation
- **Examples:** Review files in the `examples/` directory

## 🎉 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Chord DHT Graph Visualization project! 🚀