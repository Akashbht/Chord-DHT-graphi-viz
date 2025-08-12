# Project Structure

This document provides an overview of the Chord DHT Graph Visualization project structure.

## Root Directory Files

```
Chord-DHT-graphi-viz/
├── Main.py              # Main application entry point
├── Network.py           # Network management and operations  
├── Node.py              # Individual node implementation
├── README.md            # Comprehensive project documentation
├── LICENSE              # MIT license
├── requirements.txt     # Python dependencies
├── setup.py             # Package setup configuration
├── setup.cfg            # Setuptools configuration
├── pyproject.toml       # Modern Python project metadata
├── config.ini           # Default application configuration
├── .gitignore           # Git ignore patterns
├── Makefile             # Development automation tasks
└── CONTRIBUTING.md      # Development and contribution guidelines
```

## Directories

### `/examples/`
Example scripts and tutorials:
- `basic_example.py` - Basic usage demonstration
- `performance_test.py` - Performance testing and benchmarks

### `/tests/`
Test suite for the application:
- `__init__.py` - Test package initialization
- `test_node.py` - Unit tests for Node class
- Additional test files can be added here

### `/backups/`
Network backup files:
- `README.md` - Backup directory documentation
- `*.json` - Network state backup files (ignored by git)

## Core Python Modules

### Main.py
- Application entry point
- Interactive terminal interface
- Command-line argument processing
- User interface management
- Application lifecycle coordination

### Network.py
- Network-wide operations and management
- Node lifecycle management (join/leave)
- Global monitoring and metrics collection
- Load balancing algorithms
- Health checks and diagnostics
- Backup and recovery coordination
- Data consistency verification

### Node.py
- Individual Chord node implementation
- Finger table management and maintenance
- Data storage with encryption
- Routing algorithms (find_successor)
- Local caching mechanisms
- Node-level metrics tracking
- Backup creation and recovery

## Configuration and Setup

### requirements.txt
Python package dependencies:
- `pydotplus` - Graph visualization
- `Pillow` - Image processing
- `pyfiglet` - ASCII art banners
- `prometheus-client` - Metrics collection
- `rich` - Terminal UI components
- `cryptography` - Data encryption

### config.ini
Default configuration settings:
- Network parameters (ring size, node limits)
- Security settings (encryption, authentication)
- Monitoring configuration (metrics, health checks)
- Visualization preferences
- Logging configuration
- Performance tuning options

### setup.py & pyproject.toml
Package installation and metadata:
- Package metadata and dependencies
- Entry points for console scripts
- Development dependencies
- Build system configuration

## Development Tools

### Makefile
Common development tasks:
- `make install` - Install package
- `make test` - Run test suite
- `make lint` - Code linting
- `make format` - Code formatting
- `make clean` - Clean build artifacts

### .gitignore
Ignore patterns for:
- Python cache files (`__pycache__/`)
- Build artifacts (`build/`, `dist/`)
- IDE files (`.vscode/`, `.idea/`)
- Log files (`*.log`)
- Generated graphs and backup files

## Documentation

### README.md
Comprehensive project documentation including:
- Installation instructions
- Usage examples
- API documentation
- Performance characteristics
- Troubleshooting guide

### CONTRIBUTING.md
Development guidelines covering:
- Code style and standards
- Testing requirements
- Pull request process
- Development workflow
- Debugging guidelines

## Generated Files (Not in Git)

### Runtime Files
- `*.log` - Application log files
- `graph.dot` - Graphviz intermediate files
- `network_graph.svg` - Generated network visualizations
- `network_graph.png` - Generated network images

### Backup Files
- `network_backup_*.json` - Network state backups
- Located in `/backups/` directory

## Key Features by Module

### Visualization (Main.py + Network.py)
- Real-time SVG/PNG graph generation
- Interactive network topology display
- Data distribution visualization
- Performance metrics display

### Distributed Hash Table (Node.py + Network.py)
- Complete Chord protocol implementation
- Consistent hashing with SHA-1
- Finger table routing (O(log N) lookups)
- Automatic stabilization and recovery

### Monitoring (Network.py)
- Prometheus metrics integration
- Health monitoring and diagnostics
- Load balancing and redistribution
- Performance tracking

### Security (Node.py)
- Data encryption with Fernet
- Authentication tokens
- Secure node communication
- Backup encryption

This structure provides a clean separation of concerns while maintaining the flexibility for future extensions and improvements.