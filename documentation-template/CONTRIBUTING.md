# Contributing Guide

Thank you for your interest in contributing to this project! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)
- [Communication Channels](#communication-channels)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information

## Getting Started

### Prerequisites

Before you begin, ensure you have:

1. **Required Tools**:
   - Git 2.x or higher
   - Python 3.9+ (or relevant language)
   - Make
   - Docker/Podman (for containerized testing)

2. **Required Accounts**:
   - GitHub/GitLab account
   - Access to internal systems (if applicable)

3. **Permissions**:
   - Read/write access to the repository (request from maintainers)

### First Time Setup

1. **Fork and Clone**:
   ```bash
   # Fork the repository on GitHub/GitLab first, then:
   git clone <your-fork-url>
   cd <project-name>
   
   # Add upstream remote
   git remote add upstream <original-repo-url>
   ```

2. **Install Dependencies**:
   ```bash
   # Install development dependencies
   make dev-setup
   
   # Or manually:
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```

3. **Verify Setup**:
   ```bash
   # Run tests to ensure everything is working
   make test
   
   # Run linters
   make lint
   ```

4. **Configure Git Hooks** (optional but recommended):
   ```bash
   make setup-hooks
   ```

## Development Workflow

We follow a feature branch workflow:

### 1. Create a Feature Branch

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming Conventions**:
- `feature/` - for new features
- `bugfix/` - for bug fixes
- `docs/` - for documentation changes
- `refactor/` - for code refactoring
- `test/` - for test additions/changes

### 2. Make Your Changes

- Write clean, readable code following our [coding standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Commit Your Changes

We follow conventional commit message format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```bash
git commit -m "feat(auth): add OAuth2 authentication support

- Implement OAuth2 flow with token refresh
- Add configuration options for OAuth providers
- Include unit tests for authentication logic

Closes #123"
```

### 4. Keep Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Rebase your branch on top of main
git rebase upstream/main

# Force push to your fork (only for your own branches!)
git push --force-with-lease origin feature/your-feature-name
```

### 5. Run Tests Locally

Before submitting, always run:

```bash
# Run all tests
make test

# Run linters and formatters
make lint
make format

# Check test coverage
make coverage
```

## Coding Standards

### General Principles

- **Readability**: Code is read more often than written
- **Simplicity**: Prefer simple solutions over clever ones
- **Consistency**: Follow existing patterns in the codebase
- **Documentation**: Document why, not what

### Language-Specific Standards

#### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints for function signatures
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for all public functions and classes

```python
def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Calculate total price including tax.
    
    Args:
        items: List of item dictionaries with 'price' key
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
    
    Returns:
        Total price including tax
        
    Raises:
        ValueError: If items list is empty or tax_rate is negative
    """
    if not items or tax_rate < 0:
        raise ValueError("Invalid input parameters")
    
    subtotal = sum(item['price'] for item in items)
    return subtotal * (1 + tax_rate)
```

#### Ansible

- Follow [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- Use fully qualified collection names (FQCN)
- Prefix role variables with role name
- Use `ansible.builtin.import_*` over `include_*` unless dynamic loading is needed

```yaml
---
- name: Configure web server
  ansible.builtin.import_role:
    name: webserver
  vars:
    webserver_port: 8080
    webserver_ssl_enabled: true
```

### File Organization

```
project/
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── scripts/          # Utility scripts
├── config/           # Configuration files
└── examples/         # Example usage
```

### Naming Conventions

- **Files**: lowercase with underscores (`my_module.py`)
- **Classes**: PascalCase (`MyClass`)
- **Functions**: snake_case (`my_function`)
- **Constants**: UPPER_CASE (`MAX_RETRIES`)
- **Private**: prefix with underscore (`_internal_function`)

## Testing Requirements

All contributions must include appropriate tests.

### Test Types

1. **Unit Tests**: Test individual functions/methods in isolation
2. **Integration Tests**: Test interaction between components
3. **End-to-End Tests**: Test complete workflows

### Writing Tests

```python
import pytest
from mymodule import calculate_total

def test_calculate_total_basic():
    """Test basic total calculation."""
    items = [{'price': 10.0}, {'price': 20.0}]
    assert calculate_total(items) == 30.0

def test_calculate_total_with_tax():
    """Test calculation with tax."""
    items = [{'price': 100.0}]
    assert calculate_total(items, tax_rate=0.08) == 108.0

def test_calculate_total_empty_items():
    """Test that empty items raises ValueError."""
    with pytest.raises(ValueError):
        calculate_total([])
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_mymodule.py

# Run with coverage
make coverage

# Run only unit tests
pytest tests/unit/

# Run with verbose output
pytest -v
```

### Test Coverage Requirements

- Minimum 80% code coverage for new code
- 100% coverage for critical paths (authentication, data validation)
- Use `make coverage` to generate coverage reports

## Submitting Changes

### Creating a Pull Request

1. **Push Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request**:
   - Go to the repository on GitHub/GitLab
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template (see below)

### Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Related Issues
Closes #<issue-number>
Relates to #<issue-number>

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing locally

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
- [ ] Dependent changes merged

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Additional Notes
Any additional information reviewers should know
```

### PR Best Practices

- **Keep PRs Small**: Aim for < 400 lines of changes
- **One Concern Per PR**: Don't mix features, bugs, and refactoring
- **Clear Description**: Explain what and why, not just how
- **Self Review**: Review your own PR before requesting reviews
- **Respond Promptly**: Address review comments in a timely manner

## Review Process

### What Reviewers Look For

1. **Correctness**: Does the code do what it claims?
2. **Tests**: Are there adequate tests?
3. **Style**: Does it follow coding standards?
4. **Documentation**: Is it properly documented?
5. **Performance**: Are there any performance concerns?
6. **Security**: Are there any security implications?

### Review Timeline

- **Initial Review**: Within 2 business days
- **Follow-up Reviews**: Within 1 business day
- **Approval Requirements**: 2 approvals from maintainers

### Responding to Review Comments

- Address all comments (implement changes or explain why not)
- Mark resolved conversations as resolved
- Request re-review when ready
- Be receptive to feedback

### After Approval

- Maintainers will merge your PR
- Your branch will be automatically deleted
- Ensure you pull the latest main branch

## Communication Channels

### Where to Ask for Help

- **General Questions**: [Slack/Teams Channel](link)
- **Bug Reports**: [GitHub Issues](link)
- **Feature Requests**: [GitHub Discussions](link)
- **Security Issues**: [security@example.com](mailto:security@example.com)

### Team Meetings

- **Weekly Standup**: Mondays at 10:00 AM (Time Zone)
- **Sprint Planning**: Every other Wednesday
- **Office Hours**: Fridays 2-3 PM for questions

### Response Times

- **Slack**: Within 1 business day
- **Pull Requests**: Within 2 business days
- **Issues**: Within 3 business days

## Additional Resources

- [Development Guide](docs/development/README.md)
- [Architecture Documentation](docs/architecture/overview.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [FAQ](docs/FAQ.md)

## Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes
- Project website (if applicable)

Thank you for contributing! 🎉



