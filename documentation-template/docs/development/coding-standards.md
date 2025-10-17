# Coding Standards

This document defines the coding standards and best practices for this project.

## General Principles

### Code Quality Principles

1. **Readability First**: Code is read more often than it's written
2. **Explicit Over Implicit**: Clear code beats clever code
3. **DRY (Don't Repeat Yourself)**: Avoid code duplication
4. **KISS (Keep It Simple, Stupid)**: Simple solutions are usually better
5. **YAGNI (You Aren't Gonna Need It)**: Don't add unnecessary features
6. **Composition Over Inheritance**: Prefer composing objects over inheritance
7. **Single Responsibility**: Each module/class/function should do one thing well

### Code Review Standards

All code must:
- Pass automated linting checks
- Have appropriate test coverage (>80%)
- Include documentation for public APIs
- Be reviewed by at least 2 team members
- Pass all CI/CD checks

## Python Standards

### Style Guide

We follow [PEP 8](https://pep8.org/) with these specifications:

**Line Length**:
- Maximum 88 characters (Black formatter default)
- Maximum 79 for comments and docstrings

**Indentation**:
- 4 spaces (never tabs)
- Continuation lines should be indented to opening delimiter

```python
# Good
my_list = [
    1, 2, 3,
    4, 5, 6,
]

result = my_function(
    argument1,
    argument2,
    argument3,
)

# Also good
my_list = [1, 2, 3, 4, 5, 6]

# Bad
my_list = [1, 2, 3,
4, 5, 6]
```

**Imports**:
```python
# Good: Organized and clear
import os
import sys
from typing import Optional, List

import requests
import pytest

from myapp.core import Database
from myapp.models import User
from myapp.utils import logger

# Bad: Mixed order and grouping
from myapp.models import User
import sys
import requests
from myapp.core import Database
import os
```

**Import Grouping**:
1. Standard library imports
2. Related third-party imports
3. Local application imports

Separate each group with blank line.

### Naming Conventions

**Modules**: `lowercase_with_underscores.py`
```python
# Good
user_service.py
authentication_handler.py

# Bad
UserService.py
authenticationHandler.py
```

**Classes**: `PascalCase`
```python
# Good
class UserManager:
    pass

class HTTPRequest:
    pass

# Bad
class user_manager:
    pass

class Http_Request:
    pass
```

**Functions and Variables**: `snake_case`
```python
# Good
def calculate_total(items):
    user_count = len(items)
    return user_count

# Bad
def calculateTotal(items):
    UserCount = len(items)
    return UserCount
```

**Constants**: `UPPER_CASE_WITH_UNDERSCORES`
```python
# Good
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# Bad
max_connections = 100
DefaultTimeout = 30
```

**Private**: Prefix with single underscore
```python
class MyClass:
    def __init__(self):
        self._internal_state = {}  # Private attribute
    
    def public_method(self):
        """Public method."""
        pass
    
    def _private_method(self):
        """Private method."""
        pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Optional, List, Dict, Union

# Good: Clear types
def get_user(user_id: int) -> Optional[User]:
    """Retrieve user by ID."""
    return database.get(User, user_id)

def process_items(
    items: List[Dict[str, Any]],
    max_count: int = 100,
) -> List[ProcessedItem]:
    """Process list of items."""
    return [process_item(item) for item in items[:max_count]]

# Also good: Use Protocol for duck typing
from typing import Protocol

class Readable(Protocol):
    def read(self, size: int) -> bytes: ...

def read_data(source: Readable) -> bytes:
    return source.read(1024)
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_total(
    items: List[Item],
    tax_rate: float = 0.0,
    discount: Optional[float] = None,
) -> float:
    """Calculate total price with tax and discount.
    
    This function calculates the total price of items including
    tax and applying any discount if provided.
    
    Args:
        items: List of items to calculate total for
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
        discount: Optional discount as decimal (e.g., 0.10 for 10%)
    
    Returns:
        Total price as float
    
    Raises:
        ValueError: If tax_rate is negative or discount is > 1.0
        TypeError: If items list is empty
    
    Example:
        >>> items = [Item(price=10.0), Item(price=20.0)]
        >>> calculate_total(items, tax_rate=0.08)
        32.4
    """
    if not items:
        raise TypeError("Items list cannot be empty")
    if tax_rate < 0 or (discount and discount > 1.0):
        raise ValueError("Invalid tax rate or discount")
    
    subtotal = sum(item.price for item in items)
    if discount:
        subtotal *= (1 - discount)
    return subtotal * (1 + tax_rate)
```

**Class Docstrings**:
```python
class UserManager:
    """Manage user operations and lifecycle.
    
    This class provides methods for creating, updating, and
    deleting users, as well as managing user authentication.
    
    Attributes:
        database: Database connection instance
        cache: Optional cache for frequently accessed users
        logger: Logger instance for this manager
    
    Example:
        >>> manager = UserManager(database)
        >>> user = manager.create_user("john", "john@example.com")
        >>> manager.authenticate(user.id, "password")
    """
    
    def __init__(self, database: Database):
        """Initialize UserManager.
        
        Args:
            database: Database instance for user storage
        """
        self.database = database
        self.cache: Dict[int, User] = {}
        self.logger = logging.getLogger(__name__)
```

### Error Handling

**Use Specific Exceptions**:
```python
# Good
class UserNotFoundError(Exception):
    """Raised when user cannot be found."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""
    pass

def authenticate(username: str, password: str) -> User:
    user = get_user(username)
    if user is None:
        raise UserNotFoundError(f"User '{username}' not found")
    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid password")
    return user

# Bad: Generic exceptions
def authenticate(username: str, password: str) -> User:
    user = get_user(username)
    if user is None:
        raise Exception("User not found")  # Too generic
    if not verify_password(password, user.password_hash):
        raise Exception("Authentication failed")  # Too generic
    return user
```

**Proper Context**:
```python
# Good: Preserve exception context
try:
    data = json.loads(response.text)
except json.JSONDecodeError as e:
    raise InvalidResponseError(
        f"Failed to parse response: {response.text[:100]}"
    ) from e

# Bad: Swallowing exceptions
try:
    data = json.loads(response.text)
except:
    pass  # Silent failure
```

**Use Context Managers**:
```python
# Good
with open('file.txt') as f:
    data = f.read()

with database.transaction():
    user = create_user(...)
    send_welcome_email(user)

# Bad
f = open('file.txt')
data = f.read()
f.close()  # Might not be called if exception occurs
```

### Code Organization

**Module Structure**:
```python
"""Module for user management operations.

This module provides classes and functions for managing
user accounts, authentication, and authorization.
"""

# Imports grouped and ordered
import logging
from typing import Optional, List

import bcrypt
from sqlalchemy.orm import Session

from myapp.core.database import Base
from myapp.models.user import User
from myapp.utils.validation import validate_email

# Module-level constants
DEFAULT_PASSWORD_MIN_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 3

# Module logger
logger = logging.getLogger(__name__)


# Classes
class UserManager:
    """Manage user operations."""
    pass


class AuthenticationService:
    """Handle user authentication."""
    pass


# Public functions
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    pass


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    pass


# Private helper functions
def _validate_password_strength(password: str) -> bool:
    """Validate password meets strength requirements."""
    pass
```

## Ansible Standards

### Playbook Structure

```yaml
---
# Good: Clear structure with proper spacing
- name: Configure web servers
  hosts: webservers
  become: true
  
  vars:
    nginx_version: "1.20"
    app_port: 8080
  
  tasks:
    - name: Install nginx
      ansible.builtin.package:
        name: "nginx-{{ nginx_version }}"
        state: present
      tags:
        - packages
    
    - name: Configure nginx
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: '0644'
      notify: Restart nginx
      tags:
        - configuration
  
  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

### Role Standards

**Variable Naming**:
```yaml
# Good: Prefix with role name
myapp_version: "1.0.0"
myapp_config_path: "/etc/myapp"
myapp_enable_ssl: true

# Bad: No prefix
version: "1.0.0"
config_path: "/etc/myapp"
enable_ssl: true
```

**Task Naming**:
```yaml
# Good: Clear, descriptive names
- name: Install application dependencies
  ...

- name: Copy application configuration file to /etc/myapp
  ...

- name: Ensure application service is running and enabled
  ...

# Bad: Vague or missing names
- package:
    name: myapp
  ...

- name: Configure
  ...
```

**FQCN (Fully Qualified Collection Names)**:
```yaml
# Good: Use FQCN
- name: Create directory
  ansible.builtin.file:
    path: /opt/myapp
    state: directory

- name: Install package
  ansible.builtin.package:
    name: myapp
    state: present

# Bad: Short names
- name: Create directory
  file:  # Not using FQCN
    path: /opt/myapp
    state: directory
```

## Git Standards

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance
- `perf`: Performance improvement
- `ci`: CI/CD changes

**Examples**:
```
feat(auth): add OAuth2 authentication support

Implement OAuth2 authentication flow with support for
Google and GitHub providers. Includes token refresh
mechanism and session management.

Closes #123
```

```
fix(api): handle null response in user endpoint

The /api/users endpoint was returning 500 error when
user data was null. Now returns 404 with appropriate
error message.

Fixes #456
```

### Branch Naming

```
<type>/<short-description>
```

**Examples**:
```
feature/add-user-authentication
bugfix/fix-null-pointer-error
hotfix/security-vulnerability
refactor/simplify-database-queries
docs/update-contributing-guide
```

## Code Review Checklist

### For Authors

Before requesting review:
- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Self-reviewed the changes
- [ ] No debug code or commented-out code
- [ ] Commit messages follow convention
- [ ] PR description is clear and complete

### For Reviewers

Check for:
- [ ] Code is readable and maintainable
- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate
- [ ] Tests are comprehensive
- [ ] Documentation is accurate
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Breaking changes are documented

## Tools

### Linters

```bash
# Python
ruff check .         # Fast linter
pylint myapp/        # Comprehensive linting
mypy myapp/          # Type checking

# Ansible
ansible-lint playbooks/

# YAML
yamllint .

# All at once
make lint
```

### Formatters

```bash
# Python
black .              # Auto-format
isort .              # Sort imports

# All at once
make format
```

### Pre-commit Hooks

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

## Resources

- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Conventional Commits](https://www.conventionalcommits.org/)



