# Development Guide

Complete guide for developers who want to contribute to or extend this project.

## Table of Contents

1. [Environment Setup](environment-setup.md) - Set up your development environment
2. [Development Workflow](workflow.md) - Day-to-day development process
3. [Coding Standards](coding-standards.md) - Code style and best practices
4. [Testing Guide](testing.md) - Writing and running tests
5. [Debugging Guide](debugging.md) - Tools and techniques for debugging
6. [Documentation Guide](documentation-style-guide.md) - Writing documentation
7. [Release Process](release-process.md) - How releases are made

## Quick Start for Developers

### 1. Set Up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd <project-name>

# Run development setup
make dev-setup

# Install git hooks
make setup-hooks
```

### 2. Create Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 3. Make Changes and Test

```bash
# Make your changes
vim src/mymodule.py

# Run tests
make test

# Run linters
make lint

# Fix formatting
make format
```

### 4. Commit and Push

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/my-new-feature
```

### 5. Create Pull Request

Go to GitHub/GitLab and create a PR using the template.

## Development Tools

### Required Tools

- **Git** 2.x+
- **Python** 3.9+
- **Make** - Build automation
- **Docker/Podman** - Container testing
- **Pre-commit** - Git hooks framework

### Recommended Tools

#### Code Editors

**Visual Studio Code**:
- Install from: https://code.visualstudio.com/
- Recommended extensions:
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)
  - GitLens (eamodio.gitlens)
  - YAML (redhat.vscode-yaml)
  - Markdown All in One (yzhang.markdown-all-in-one)

**PyCharm**:
- Professional or Community Edition
- Configure Python interpreter to use venv

**Vim/Neovim**:
- Install python-mode or use coc-python
- Recommended plugins: vim-gitgutter, nerdtree, fzf

#### Command Line Tools

```bash
# ripgrep - fast code search
sudo dnf install ripgrep  # Fedora/RHEL
brew install ripgrep      # macOS

# jq - JSON processor
sudo dnf install jq
brew install jq

# httpie - better curl
pip install httpie

# gh - GitHub CLI
sudo dnf install gh
brew install gh
```

## Project Structure

```
project/
├── src/                    # Source code
│   ├── myapp/
│   │   ├── __init__.py
│   │   ├── main.py        # Entry point
│   │   ├── core/          # Core functionality
│   │   ├── api/           # API endpoints
│   │   └── utils/         # Utilities
├── tests/                  # Tests
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures
├── docs/                   # Documentation
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── examples/               # Example code
├── .github/                # GitHub workflows
├── Makefile               # Build automation
├── requirements.txt       # Production dependencies
├── dev-requirements.txt   # Development dependencies
├── setup.py               # Package setup
└── README.md              # Project README
```

## Common Development Tasks

### Running the Application

```bash
# Development mode with auto-reload
make dev

# Production mode
make run

# With specific configuration
make run CONFIG=config/custom.yml

# In debug mode
DEBUG=1 make run
```

### Testing

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests
make test-integration

# Run with coverage report
make coverage

# Run specific test
pytest tests/unit/test_mymodule.py::test_specific_function

# Run tests matching pattern
pytest -k "test_auth"

# Run with verbose output
pytest -v

# Run with debugging
pytest --pdb
```

### Code Quality

```bash
# Run all linters
make lint

# Individual linters
make lint-python    # Ruff, pylint
make lint-yaml      # yamllint
make lint-ansible   # ansible-lint

# Auto-format code
make format

# Type checking
make type-check

# Security scanning
make security-scan
```

### Building and Packaging

```bash
# Build package
make build

# Install in development mode
make install-dev

# Create distribution packages
make dist

# Build container image
make container-build
```

### Database Operations

```bash
# Create database
make db-create

# Run migrations
make db-migrate

# Seed test data
make db-seed

# Reset database
make db-reset
```

### Documentation

```bash
# Build documentation
make docs

# Serve documentation locally
make docs-serve

# Check for broken links
make docs-check
```

## Development Workflow

### Daily Workflow

```bash
# Start your day
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-feature

# Start development server
make dev  # In terminal 1

# Run tests in watch mode
make test-watch  # In terminal 2

# Make changes, tests run automatically
vim src/mymodule.py

# Commit when ready
git add .
git commit -m "feat: implement feature"

# Push and create PR
git push origin feature/my-feature
```

### Code Review Workflow

1. **Self Review**: Review your own changes first
2. **Create PR**: Use the PR template
3. **Address Feedback**: Respond to review comments
4. **Update PR**: Push additional commits
5. **Merge**: Maintainer will merge when approved

### Debugging Workflow

```bash
# Add debugging statements
import pdb; pdb.set_trace()

# Run with debugger
python -m pdb src/myapp/main.py

# Run tests with debugger
pytest --pdb tests/test_mymodule.py

# Use IDE debugger
# Set breakpoints in VS Code/PyCharm and use "Debug" run configuration
```

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│           API Layer                     │
│  (REST API, CLI, Web Interface)         │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│        Business Logic Layer             │
│   (Core functionality, workflows)       │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         Data Layer                      │
│  (Database, cache, external services)   │
└─────────────────────────────────────────┘
```

For detailed architecture documentation, see [Architecture Overview](../architecture/overview.md).

## Useful Resources

### Internal Documentation

- [Architecture Overview](../architecture/overview.md)
- [API Reference](../api/README.md)
- [Configuration Guide](../configuration.md)
- [Troubleshooting](../troubleshooting.md)

### External Resources

- [Python Documentation](https://docs.python.org/3/)
- [Ansible Documentation](https://docs.ansible.com/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

### For Development Questions

- **Slack/Teams**: [#dev-channel](chat-url)
- **Office Hours**: Fridays 2-3 PM
- **Pair Programming**: Schedule via calendar

### For Technical Issues

- **GitHub Issues**: [Report issue](issues-url)
- **Developer Mailing List**: [dev@example.com](mailto:dev@example.com)

## Contributing

Ready to contribute? Start with:

1. Read the [Contributing Guide](../../CONTRIBUTING.md)
2. Set up your [Development Environment](environment-setup.md)
3. Review [Coding Standards](coding-standards.md)
4. Pick an issue labeled "good first issue"
5. Create a PR and get feedback!

## Next Steps

- **[Environment Setup](environment-setup.md)** - Detailed setup instructions
- **[Development Workflow](workflow.md)** - In-depth workflow guide
- **[Testing Guide](testing.md)** - Comprehensive testing documentation
- **[Debugging Guide](debugging.md)** - Debugging tips and tricks



