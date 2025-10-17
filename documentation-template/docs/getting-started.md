# Getting Started

This guide will help you get started with the project in just a few minutes.

## Prerequisites

Before you begin, ensure you have:

- **Operating System**: Linux (RHEL 9, Fedora 38+, Ubuntu 22.04+) or macOS 12+
- **Python**: 3.9 or higher
- **Git**: 2.x or higher
- **Memory**: At least 8GB RAM
- **Disk Space**: At least 20GB free space

## Quick Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-name>
```

### 2. Install Dependencies

#### Using Make (Recommended)

```bash
make install
```

#### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Application

Create a configuration file:

```bash
cp config/config.example.yml config/config.yml
```

Edit `config/config.yml` with your settings:

```yaml
# Minimal configuration
environment: development
debug: true
log_level: INFO

# Database settings
database:
  host: localhost
  port: 5432
  name: myapp_dev
```

### 4. Verify Installation

Run the test suite to ensure everything is working:

```bash
make test
```

Expected output:
```
===== test session starts =====
collected 42 items

tests/test_basic.py ......                     [ 14%]
tests/test_advanced.py ................................  [100%]

===== 42 passed in 2.45s =====
```

## First Run

### Start the Application

```bash
# Development mode
make run

# Or directly
python -m myapp.main
```

You should see output similar to:

```
INFO: Starting application...
INFO: Server running on http://localhost:8000
INFO: Press CTRL+C to quit
```

### Verify It's Working

Open your browser or use curl:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-15T12:00:00Z"
}
```

## Basic Usage

### Example 1: Simple Operation

```bash
# Run a basic command
./myapp hello --name "World"
```

Output:
```
Hello, World!
```

### Example 2: With Configuration

```bash
# Run with custom config
./myapp process --config config/custom.yml --input data.txt
```

### Example 3: Interactive Mode

```bash
# Start interactive shell
./myapp shell
```

```python
>>> from myapp import tasks
>>> result = tasks.run("example")
>>> print(result)
Task completed successfully
```

## Common Tasks

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_mymodule.py

# Run with coverage
make coverage
```

### Linting and Formatting

```bash
# Check code style
make lint

# Auto-format code
make format
```

### Viewing Logs

```bash
# Tail application logs
tail -f logs/app.log

# View errors only
grep ERROR logs/app.log
```

### Cleaning Up

```bash
# Clean temporary files
make clean

# Full cleanup (including virtual environment)
make distclean
```

## Next Steps

Now that you have the basics working:

1. **Read the [User Guide](user-guide.md)** - Learn about all features
2. **Explore [Configuration Options](configuration.md)** - Customize for your needs
3. **Check [Examples](../examples/)** - See real-world usage examples
4. **Join the [Community](#getting-help)** - Ask questions and get help

### For Developers

If you want to contribute or develop:

1. **[Development Environment Setup](development/environment-setup.md)**
2. **[Development Workflow](development/workflow.md)**
3. **[Contributing Guide](../CONTRIBUTING.md)**

## Troubleshooting

### Common Issues

#### Installation Fails

**Problem**: `pip install` fails with dependency errors

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Try installation again
pip install -r requirements.txt
```

#### Port Already in Use

**Problem**: Error "Address already in use: 8000"

**Solution**:
```bash
# Find process using the port
lsof -i :8000  # On Linux/Mac
# OR
netstat -ano | findstr :8000  # On Windows

# Kill the process or use a different port
./myapp run --port 8001
```

#### Permission Denied

**Problem**: Permission denied when running commands

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Or run with python
python -m myapp.main
```

For more troubleshooting help, see the [Troubleshooting Guide](troubleshooting.md).

## Getting Help

- **Documentation**: [Full Documentation](README.md)
- **Issues**: [Report a bug](issues-url)
- **Chat**: [Slack/Teams Channel](chat-url)
- **Email**: [support@example.com](mailto:support@example.com)

## What's Next?

- **[User Guide](user-guide.md)** - Detailed feature documentation
- **[Configuration](configuration.md)** - All configuration options
- **[API Documentation](api/README.md)** - For programmatic usage
- **[Examples](../examples/)** - Sample code and use cases



