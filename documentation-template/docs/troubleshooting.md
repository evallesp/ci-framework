# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### Python Version Mismatch

**Problem**: "Python 3.9+ required" error

**Symptoms**:
```
ERROR: This package requires Python 3.9 or higher
You are using Python 3.8.x
```

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.11 (Fedora/RHEL)
sudo dnf install python3.11

# Install Python 3.11 (Ubuntu)
sudo apt install python3.11

# Use specific Python version
python3.11 -m venv venv
source venv/bin/activate
```

### Dependency Installation Fails

**Problem**: pip install fails with compilation errors

**Symptoms**:
```
error: command 'gcc' failed with exit status 1
fatal error: Python.h: No such file or directory
```

**Solution**:
```bash
# Install development tools (Fedora/RHEL)
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel openssl-devel libffi-devel

# Install development tools (Ubuntu)
sudo apt update
sudo apt install build-essential python3-dev libssl-dev libffi-dev

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Try installation again
pip install -r requirements.txt
```

### Permission Denied

**Problem**: Permission errors during installation

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied: '/usr/local/lib/python3.x/'
```

**Solution**:
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use --user flag (not recommended)
pip install --user -r requirements.txt

# Fix ownership of project directory
sudo chown -R $USER:$USER ~/project-name
```

### Virtual Environment Won't Activate

**Problem**: Cannot activate virtual environment

**Symptoms**:
```bash
bash: venv/bin/activate: No such file or directory
```

**Solution**:
```bash
# Remove corrupted venv
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

## Runtime Issues

### Application Won't Start

**Problem**: Application fails to start

**Symptoms**:
```
Error: Could not start application
Connection refused
```

**Diagnostic Steps**:

1. **Check logs**:
   ```bash
   cat logs/app.log
   tail -f logs/error.log
   ```

2. **Verify configuration**:
   ```bash
   ./myapp --config config/config.yml --validate
   ```

3. **Check port availability**:
   ```bash
   # Linux/macOS
   lsof -i :8000
   netstat -tuln | grep 8000
   
   # Kill process if needed
   kill <pid>
   ```

4. **Test with debug mode**:
   ```bash
   DEBUG=true LOG_LEVEL=DEBUG ./myapp
   ```

### Port Already in Use

**Problem**: "Address already in use" error

**Symptoms**:
```
OSError: [Errno 98] Address already in use
```

**Solution**:
```bash
# Find process using the port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process
kill <pid>  # Linux/macOS
taskkill /PID <pid> /F  # Windows

# Or use different port
./myapp --port 8001
```

### Database Connection Errors

**Problem**: Cannot connect to database

**Symptoms**:
```
OperationalError: could not connect to server
Connection refused
Authentication failed
```

**Diagnostic Steps**:

1. **Verify database is running**:
   ```bash
   # PostgreSQL
   sudo systemctl status postgresql
   
   # Check if listening
   netstat -tuln | grep 5432
   ```

2. **Test connection manually**:
   ```bash
   # PostgreSQL
   psql -h localhost -U myapp -d myapp_dev
   
   # MySQL
   mysql -h localhost -u myapp -p myapp_dev
   ```

3. **Check connection string**:
   ```bash
   # Should be in format:
   # postgresql://user:password@host:port/database
   echo $DATABASE_URL
   ```

4. **Verify credentials**:
   ```sql
   # PostgreSQL - check user exists
   sudo -u postgres psql
   \du  # List users
   \l   # List databases
   ```

**Solutions**:

```bash
# Recreate database
sudo -u postgres psql
DROP DATABASE IF EXISTS myapp_dev;
CREATE DATABASE myapp_dev;
GRANT ALL PRIVILEGES ON DATABASE myapp_dev TO myapp;

# Reset password
ALTER USER myapp WITH PASSWORD 'newpassword';

# Update connection string
export DATABASE_URL=postgresql://myapp:newpassword@localhost/myapp_dev
```

### Import Errors

**Problem**: ModuleNotFoundError or ImportError

**Symptoms**:
```
ModuleNotFoundError: No module named 'myapp'
ImportError: cannot import name 'MyClass'
```

**Solutions**:

1. **Ensure virtual environment is activated**:
   ```bash
   which python
   # Should show: /path/to/venv/bin/python
   
   source venv/bin/activate
   ```

2. **Install package in development mode**:
   ```bash
   pip install -e .
   ```

3. **Check PYTHONPATH**:
   ```bash
   # Add project directory to PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   
   # Or run as module
   python -m myapp.main
   ```

4. **Verify package is installed**:
   ```bash
   pip list | grep myapp
   ```

### Configuration Not Loading

**Problem**: Application not using custom configuration

**Symptoms**:
- Settings not taking effect
- Using default values instead of config values

**Solutions**:

1. **Verify config file location**:
   ```bash
   ls -la config/config.yml
   ```

2. **Check config file syntax**:
   ```bash
   # Validate YAML
   python -c "import yaml; yaml.safe_load(open('config/config.yml'))"
   ```

3. **Specify config explicitly**:
   ```bash
   ./myapp --config config/config.yml
   ```

4. **Check environment variables**:
   ```bash
   # Environment variables override config files
   env | grep -i myapp
   ```

5. **Enable config debugging**:
   ```python
   # Add to code temporarily
   import logging
   logging.basicConfig(level=logging.DEBUG)
   # See which config is loaded
   ```

## Testing Issues

### Tests Fail Locally

**Problem**: Tests failing on local machine

**Diagnostic Steps**:

1. **Run with verbose output**:
   ```bash
   pytest -vv
   ```

2. **Run specific failing test**:
   ```bash
   pytest tests/test_mymodule.py::test_specific -vv
   ```

3. **Run with debugger**:
   ```bash
   pytest --pdb tests/test_mymodule.py::test_specific
   ```

**Common Causes**:

1. **Missing test dependencies**:
   ```bash
   pip install -r dev-requirements.txt
   ```

2. **Database state**:
   ```bash
   # Reset test database
   make db-reset
   ```

3. **File permissions**:
   ```bash
   chmod -R u+w tests/
   ```

### Tests Pass Locally but Fail in CI

**Problem**: Tests pass locally but fail in CI/CD

**Common Causes and Solutions**:

1. **Environment differences**:
   ```bash
   # Check Python version matches CI
   python --version
   
   # Use same Python version as CI
   pyenv install 3.11.5
   pyenv local 3.11.5
   ```

2. **Missing environment variables**:
   ```yaml
   # Add to CI config
   env:
     DATABASE_URL: postgresql://test:test@localhost/test_db
     SECRET_KEY: test-secret-key
   ```

3. **Timezone issues**:
   ```python
   # Use UTC in tests
   from datetime import timezone
   now = datetime.now(timezone.utc)
   ```

4. **Test order dependency**:
   ```bash
   # Run tests in random order
   pytest --random-order
   
   # If fails, tests have order dependency
   # Fix by making tests independent
   ```

5. **File path issues**:
   ```python
   # Bad: Absolute path
   file_path = "/home/user/project/data.txt"
   
   # Good: Relative path
   import os
   file_path = os.path.join(os.path.dirname(__file__), "data.txt")
   ```

### Slow Tests

**Problem**: Tests take too long to run

**Solutions**:

1. **Run tests in parallel**:
   ```bash
   pip install pytest-xdist
   pytest -n auto
   ```

2. **Identify slow tests**:
   ```bash
   pytest --durations=10
   ```

3. **Skip slow tests during development**:
   ```python
   # Mark slow tests
   @pytest.mark.slow
   def test_large_dataset():
       pass
   
   # Skip during development
   pytest -m "not slow"
   ```

4. **Use test database in memory**:
   ```python
   # SQLite in memory
   DATABASE_URL = "sqlite:///:memory:"
   ```

## Development Issues

### Git Issues

**Problem**: Git operations failing

#### Merge Conflicts

**Symptoms**:
```
CONFLICT (content): Merge conflict in file.py
Automatic merge failed
```

**Solution**:
```bash
# View conflicted files
git status

# Edit files to resolve conflicts
# Look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# After resolving, mark as resolved
git add resolved-file.py

# Continue merge
git merge --continue
# or
git rebase --continue
```

#### Detached HEAD State

**Symptoms**:
```
You are in 'detached HEAD' state
```

**Solution**:
```bash
# Create branch from current state
git checkout -b temp-branch

# Or return to main branch (lose changes)
git checkout main
```

#### Accidental Commit to Main

**Symptoms**:
- Committed directly to main branch instead of feature branch

**Solution**:
```bash
# Create feature branch from current state
git branch feature/my-feature

# Reset main to remote state
git checkout main
git reset --hard origin/main

# Switch to feature branch
git checkout feature/my-feature
```

### IDE Issues

#### VS Code Python Extension Not Working

**Problem**: IntelliSense, linting not working in VS Code

**Solution**:

1. **Select correct Python interpreter**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Select the one in your venv: `./venv/bin/python`

2. **Reload window**:
   - Press `Ctrl+Shift+P`
   - Type "Developer: Reload Window"

3. **Check Python extension is installed**:
   - Extensions → Search "Python"
   - Install Microsoft Python extension

4. **Check workspace settings**:
   ```json
   {
       "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
   }
   ```

### Container Issues

**Problem**: Container-related errors

#### Container Build Fails

**Symptoms**:
```
Error building image
COPY failed: no such file or directory
```

**Solution**:

1. **Check Containerfile/Dockerfile**:
   ```dockerfile
   # Ensure paths are correct
   COPY requirements.txt ./
   RUN pip install -r requirements.txt
   ```

2. **Check .dockerignore**:
   ```
   # Don't ignore required files
   !requirements.txt
   !src/
   ```

3. **Build with no cache**:
   ```bash
   podman build --no-cache -t myapp .
   ```

#### Container Won't Start

**Solution**:

1. **Check container logs**:
   ```bash
   podman logs <container-id>
   docker logs <container-id>
   ```

2. **Run interactively**:
   ```bash
   podman run -it myapp /bin/bash
   # Debug inside container
   ```

3. **Check port mapping**:
   ```bash
   podman run -p 8000:8000 myapp
   ```

## Performance Issues

### High Memory Usage

**Problem**: Application consuming too much memory

**Diagnostic Steps**:

1. **Monitor memory usage**:
   ```bash
   # Linux
   htop
   ps aux | grep python
   
   # Get process memory
   ps -p <pid> -o rss,vsz
   ```

2. **Profile memory**:
   ```bash
   pip install memory_profiler
   python -m memory_profiler myapp.py
   ```

3. **Check for memory leaks**:
   ```python
   # Add to code
   import tracemalloc
   tracemalloc.start()
   
   # Your code here
   
   snapshot = tracemalloc.take_snapshot()
   top_stats = snapshot.statistics('lineno')
   for stat in top_stats[:10]:
       print(stat)
   ```

**Solutions**:

1. **Enable garbage collection**:
   ```python
   import gc
   gc.collect()
   ```

2. **Use generators instead of lists**:
   ```python
   # Bad: Loads all in memory
   data = [process(item) for item in huge_list]
   
   # Good: Lazy evaluation
   data = (process(item) for item in huge_list)
   ```

3. **Limit cache size**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def expensive_function(arg):
       pass
   ```

### High CPU Usage

**Problem**: Application using too much CPU

**Diagnostic Steps**:

1. **Profile CPU usage**:
   ```bash
   pip install py-spy
   py-spy top --pid <process-id>
   ```

2. **Generate flame graph**:
   ```bash
   py-spy record -o profile.svg --pid <process-id>
   ```

**Solutions**:

1. **Optimize hot paths**:
   - Use profiler to identify bottlenecks
   - Optimize algorithms
   - Use caching

2. **Use multiprocessing**:
   ```python
   from multiprocessing import Pool
   
   with Pool() as pool:
       results = pool.map(process_item, items)
   ```

## Getting More Help

### Before Asking for Help

1. **Search documentation**: [Documentation](README.md)
2. **Search existing issues**: [GitHub Issues](issues-url)
3. **Check FAQ**: [FAQ](FAQ.md)

### When Asking for Help

Include:

1. **What you're trying to do**
2. **What you expected to happen**
3. **What actually happened**
4. **Steps to reproduce**
5. **System information**:
   ```bash
   # Operating system
   uname -a
   
   # Python version
   python --version
   
   # Package versions
   pip list
   
   # Application version
   ./myapp --version
   ```

6. **Relevant logs**:
   ```bash
   # Last 50 lines of logs
   tail -50 logs/app.log
   ```

7. **Configuration** (sanitize secrets!):
   ```yaml
   # config.yml (remove passwords/keys)
   ```

### Where to Get Help

- **Chat**: [Slack/Teams Channel](chat-url) - Quick questions
- **Issues**: [GitHub Issues](issues-url) - Bug reports
- **Discussions**: [GitHub Discussions](discussions-url) - General questions
- **Email**: [support@example.com](mailto:support@example.com) - Private issues

### Emergency Support

For critical production issues:

1. **Email**: [urgent@example.com](mailto:urgent@example.com)
2. **On-call**: See [On-Call Schedule](operations/oncall.md)
3. **Slack**: Post in `#urgent` channel

## Still Stuck?

Create a detailed issue: [New Issue](issues-url/new)

We'll help you figure it out!



