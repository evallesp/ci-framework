# Testing Guide

Comprehensive guide to writing, running, and maintaining tests in this project.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Types](#test-types)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Mocking and Fixtures](#mocking-and-fixtures)
- [CI/CD Integration](#cicd-integration)

## Testing Philosophy

We believe in:

- **Testing as Documentation**: Tests show how code should be used
- **Fast Feedback**: Tests should run quickly for rapid iteration
- **Comprehensive Coverage**: Critical paths must have 100% coverage
- **Maintainable Tests**: Tests should be as clean as production code
- **Test-Driven Development**: Write tests first when it makes sense

## Test Types

### 1. Unit Tests

Test individual functions or classes in isolation.

**Characteristics**:
- Fast (< 1ms per test)
- No external dependencies
- Test single units of code
- Use mocking for dependencies

**Location**: `tests/unit/`

**Example**:
```python
# tests/unit/test_calculator.py
import pytest
from myapp.calculator import Calculator

def test_add():
    """Test addition of two numbers."""
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_add_negative_numbers():
    """Test addition with negative numbers."""
    calc = Calculator()
    assert calc.add(-1, -2) == -3

def test_divide_by_zero():
    """Test that division by zero raises ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
```

### 2. Integration Tests

Test interaction between multiple components.

**Characteristics**:
- Slower (< 1s per test)
- May use test database
- Test component interactions
- Minimal mocking

**Location**: `tests/integration/`

**Example**:
```python
# tests/integration/test_user_service.py
import pytest
from myapp.services.user_service import UserService
from myapp.database import Database

@pytest.fixture
def db():
    """Provide a test database."""
    database = Database("sqlite:///:memory:")
    database.create_tables()
    yield database
    database.drop_tables()

def test_create_and_retrieve_user(db):
    """Test creating and retrieving a user."""
    service = UserService(db)
    
    # Create user
    user = service.create_user(
        username="testuser",
        email="test@example.com"
    )
    assert user.id is not None
    
    # Retrieve user
    retrieved = service.get_user(user.id)
    assert retrieved.username == "testuser"
    assert retrieved.email == "test@example.com"
```

### 3. End-to-End Tests

Test complete workflows from user perspective.

**Characteristics**:
- Slowest (seconds per test)
- Use real services (or close replicas)
- Test user workflows
- No mocking

**Location**: `tests/e2e/`

**Example**:
```python
# tests/e2e/test_authentication_flow.py
import pytest
from myapp.client import APIClient

def test_full_authentication_flow():
    """Test complete user authentication workflow."""
    client = APIClient(base_url="http://localhost:8000")
    
    # Register new user
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "SecurePass123!",
        "email": "new@example.com"
    })
    assert response.status_code == 201
    
    # Login
    response = client.post("/auth/login", json={
        "username": "newuser",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Access protected endpoint
    client.set_token(token)
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
```

### 4. Performance Tests

Test system performance and identify bottlenecks.

**Location**: `tests/performance/`

**Example**:
```python
# tests/performance/test_api_performance.py
import pytest
import time
from myapp.api import process_request

def test_api_response_time():
    """Test API responds within acceptable time."""
    start = time.time()
    result = process_request({"data": "test"})
    duration = time.time() - start
    
    assert duration < 0.1  # Should respond in < 100ms
    assert result is not None

@pytest.mark.benchmark
def test_bulk_processing(benchmark):
    """Benchmark bulk data processing."""
    data = [{"id": i, "value": i * 2} for i in range(1000)]
    result = benchmark(process_bulk, data)
    assert len(result) == 1000
```

## Writing Tests

### Test Structure

Follow the **Arrange-Act-Assert** pattern:

```python
def test_user_creation():
    # Arrange: Set up test data and dependencies
    username = "testuser"
    email = "test@example.com"
    service = UserService()
    
    # Act: Perform the action being tested
    user = service.create_user(username, email)
    
    # Assert: Verify the results
    assert user.username == username
    assert user.email == email
    assert user.id is not None
```

### Naming Conventions

**Test Files**: `test_<module_name>.py`

**Test Functions**: `test_<what>_<condition>_<expected_result>`

```python
# Good names
def test_login_with_valid_credentials_succeeds():
    pass

def test_login_with_invalid_password_returns_401():
    pass

def test_user_creation_with_duplicate_email_raises_error():
    pass

# Avoid vague names
def test_login():  # Too vague
    pass

def test_1():  # Meaningless
    pass
```

### Docstrings

Add docstrings to explain test purpose:

```python
def test_password_hashing():
    """Test that passwords are properly hashed using bcrypt.
    
    Ensures that:
    1. Plain text passwords are never stored
    2. Same password produces different hashes (salt)
    3. Hash can be verified against original password
    """
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
```

### Parametrized Tests

Test multiple cases with same logic:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (-2, 4),
])
def test_square(input, expected):
    """Test square function with various inputs."""
    assert square(input) == expected

@pytest.mark.parametrize("email", [
    "invalid",
    "@example.com",
    "user@",
    "user @example.com",
    "",
])
def test_invalid_email_validation(email):
    """Test that invalid emails are rejected."""
    with pytest.raises(ValueError):
        validate_email(email)
```

## Running Tests

### Basic Commands

```bash
# Run all tests
make test
# or
pytest

# Run specific test file
pytest tests/unit/test_calculator.py

# Run specific test function
pytest tests/unit/test_calculator.py::test_add

# Run tests matching pattern
pytest -k "test_user"

# Run tests with specific marker
pytest -m "slow"
pytest -m "integration"
```

### Verbosity Options

```bash
# Minimal output
pytest -q

# Normal output
pytest

# Verbose output
pytest -v

# Very verbose (show all output)
pytest -vv

# Show print statements
pytest -s
```

### Running Subsets

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run fast tests only
pytest -m "not slow"

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

### Watch Mode

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw

# Run specific tests on changes
ptw -- tests/unit/
```

## Test Coverage

### Measuring Coverage

```bash
# Run tests with coverage
make coverage
# or
pytest --cov=myapp --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Critical Paths**: 100% coverage required
  - Authentication/Authorization
  - Data validation
  - Financial calculations
  - Security features

### Excluding Code from Coverage

```python
# Exclude specific lines
def debug_only():  # pragma: no cover
    print("Debug information")

# Exclude entire blocks
if TYPE_CHECKING:  # pragma: no cover
    from typing import Protocol
```

## Best Practices

### DO ✅

1. **Write Tests First** (TDD when appropriate)
   ```python
   # Write test
   def test_new_feature():
       result = new_feature()
       assert result == expected
   
   # Then implement
   def new_feature():
       # Implementation
       pass
   ```

2. **Keep Tests Simple**
   ```python
   # Good: Simple and clear
   def test_add():
       assert add(2, 3) == 5
   
   # Bad: Complex test logic
   def test_add():
       numbers = [(2, 3), (4, 5), (6, 7)]
       for a, b in numbers:
           if a > 5:
                expected = a + b + 1
           else:
               expected = a + b
           assert add(a, b) == expected
   ```

3. **Test One Thing Per Test**
   ```python
   # Good: Separate tests
   def test_user_creation():
       user = create_user("test")
       assert user.username == "test"
   
   def test_user_validation():
       with pytest.raises(ValueError):
           create_user("")
   
   # Bad: Multiple assertions testing different things
   def test_user():
       user = create_user("test")
       assert user.username == "test"
       with pytest.raises(ValueError):
           create_user("")
       updated = update_user(user, "new")
       assert updated.username == "new"
   ```

4. **Use Descriptive Assertions**
   ```python
   # Good: Clear failure message
   assert user.is_active, f"User {user.id} should be active after creation"
   
   # Better: Use assertion helpers
   assert user.is_active is True
   ```

5. **Clean Up Resources**
   ```python
   @pytest.fixture
   def temp_file():
       """Provide a temporary file."""
       f = open("test.txt", "w")
       yield f
       f.close()
       os.remove("test.txt")
   ```

### DON'T ❌

1. **Don't Test Implementation Details**
   ```python
   # Bad: Tests internal implementation
   def test_user_storage():
       service = UserService()
       service.create_user("test")
       assert len(service._users_cache) == 1  # Internal detail
   
   # Good: Tests public interface
   def test_user_creation():
       service = UserService()
       user = service.create_user("test")
       assert service.get_user(user.id) is not None
   ```

2. **Don't Use Random Data**
   ```python
   # Bad: Random data makes tests non-deterministic
   def test_sorting():
       data = [random.randint(1, 100) for _ in range(10)]
       sorted_data = sort(data)
       assert is_sorted(sorted_data)
   
   # Good: Use fixed test data
   def test_sorting():
       data = [5, 2, 8, 1, 9]
       sorted_data = sort(data)
       assert sorted_data == [1, 2, 5, 8, 9]
   ```

3. **Don't Depend on Test Order**
   ```python
   # Bad: Tests depend on execution order
   user_id = None
   
   def test_create_user():
       global user_id
       user = create_user("test")
       user_id = user.id
   
   def test_get_user():
       user = get_user(user_id)  # Depends on previous test
       assert user is not None
   
   # Good: Each test is independent
   @pytest.fixture
   def user():
       return create_user("test")
   
   def test_create_user():
       user = create_user("test")
       assert user.id is not None
   
   def test_get_user(user):
       retrieved = get_user(user.id)
       assert retrieved is not None
   ```

## Mocking and Fixtures

### Fixtures

Fixtures provide reusable test components:

```python
import pytest

@pytest.fixture
def database():
    """Provide a test database."""
    db = Database("sqlite:///:memory:")
    db.create_tables()
    yield db
    db.drop_tables()

@pytest.fixture
def sample_user(database):
    """Provide a sample user."""
    user = User(username="testuser", email="test@example.com")
    database.save(user)
    return user

def test_user_retrieval(database, sample_user):
    """Test retrieving a user from database."""
    user = database.get_user(sample_user.id)
    assert user.username == "testuser"
```

### Mocking

Mock external dependencies:

```python
from unittest.mock import Mock, patch, MagicMock

# Mock a function
def test_api_call():
    with patch('myapp.api.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        result = fetch_data()
        assert result["status"] == "ok"
        mock_get.assert_called_once()

# Mock a class
def test_email_service():
    mock_smtp = Mock()
    with patch('smtplib.SMTP', return_value=mock_smtp):
        send_email("test@example.com", "subject", "body")
        mock_smtp.send_message.assert_called_once()

# Mock environment variables
def test_config_from_env():
    with patch.dict('os.environ', {'API_KEY': 'test-key'}):
        config = load_config()
        assert config.api_key == 'test-key'
```

### Pytest-mock

Use pytest-mock plugin for cleaner mocking:

```python
def test_api_call(mocker):
    """Test API call with mocked response."""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"data": "test"}
    
    result = fetch_data()
    assert result["data"] == "test"
```

## CI/CD Integration

### Running Tests in CI

Tests run automatically on:
- Every push to feature branches
- Every pull request
- Before merge to main
- Scheduled nightly runs

### CI Configuration

Example GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r dev-requirements.txt
      - name: Run tests
        run: pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Test Markers for CI

```python
# Mark slow tests
@pytest.mark.slow
def test_large_dataset_processing():
    pass

# Mark tests requiring external services
@pytest.mark.external
def test_api_integration():
    pass

# Skip in CI
@pytest.mark.skipif(os.getenv('CI'), reason="Skip in CI")
def test_local_only():
    pass
```

Configure in `pytest.ini`:
```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    external: marks tests requiring external services
    integration: marks integration tests
    e2e: marks end-to-end tests
```

## Troubleshooting Tests

### Debugging Failed Tests

```bash
# Run with debugger
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show local variables on failure
pytest -l

# Show full diff for assertions
pytest -vv
```

### Common Issues

**Tests Pass Locally but Fail in CI**:
- Check for environment differences
- Look for test order dependencies
- Verify external service availability
- Check for timezone/locale issues

**Flaky Tests**:
- Add retries for external calls
- Use fixed test data, not random
- Mock time-dependent code
- Ensure proper cleanup

**Slow Tests**:
- Profile with `pytest --durations=10`
- Mock expensive operations
- Use smaller test datasets
- Parallelize with `pytest-xdist`

## Next Steps

- **[Debugging Guide](debugging.md)** - Debug issues effectively
- **[Coding Standards](coding-standards.md)** - Code quality guidelines
- **[CI/CD Documentation](../operations/cicd.md)** - CI/CD pipeline details



