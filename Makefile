# Makefile for Chord DHT Network project

.PHONY: help install install-dev test lint format clean build docs run example

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install package and dependencies"
	@echo "  install-dev - Install package with development dependencies"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build package"
	@echo "  docs        - Generate documentation"
	@echo "  run         - Run the main application"
	@echo "  example     - Run basic example"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Testing targets
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# Code quality targets
lint:
	flake8 *.py
	mypy *.py

format:
	black *.py examples/*.py tests/*.py

format-check:
	black --check *.py examples/*.py tests/*.py

# Clean targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Build targets
build:
	python -m build

# Documentation targets
docs:
	@echo "Documentation is in README.md and CONTRIBUTING.md"
	@echo "API documentation can be generated with:"
	@echo "  pip install pdoc"
	@echo "  pdoc --html --output-dir docs *.py"

# Run targets
run:
	python Main.py

example:
	python examples/basic_example.py

performance-test:
	python examples/performance_test.py

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

check: format-check lint test
	@echo "All checks passed!"

# Release workflow
release-test: clean test lint
	python -m build
	python -m twine check dist/*

# Quick development cycle
quick: format test
	@echo "Quick development check complete!"