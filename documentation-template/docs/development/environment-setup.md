# Development Environment Setup

This guide walks you through setting up a complete development environment from scratch.

## Prerequisites

### Operating System Support

- **Linux**: RHEL 9+, Fedora 38+, CentOS Stream 9+, Ubuntu 22.04+
- **macOS**: 12 (Monterey) or higher
- **Windows**: WSL2 with Ubuntu 22.04

### Hardware Requirements

**Minimum**:
- 8 GB RAM
- 4 CPU cores
- 20 GB free disk space

**Recommended**:
- 16 GB RAM
- 8 CPU cores
- 50 GB free disk space (especially for container development)

## Step 1: Install System Dependencies

### Fedora/RHEL/CentOS

```bash
sudo dnf install -y \
    git \
    make \
    python3.11 \
    python3.11-devel \
    python3-pip \
    gcc \
    gcc-c++ \
    podman \
    openssl-devel \
    libffi-devel \
    sqlite-devel

# Optional but recommended
sudo dnf install -y \
    vim \
    ripgrep \
    jq \
    tree \
    htop
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y \
    git \
    make \
    python3.11 \
    python3.11-dev \
    python3-pip \
    build-essential \
    docker.io \
    libssl-dev \
    libffi-dev \
    sqlite3

# Optional but recommended
sudo apt install -y \
    vim \
    ripgrep \
    jq \
    tree \
    htop
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install \
    git \
    python@3.11 \
    make \
    podman \
    ripgrep \
    jq \
    tree
```

## Step 2: Configure Git

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configure default branch name
git config --global init.defaultBranch main

# Enable colored output
git config --global color.ui auto

# Set default editor (choose one)
git config --global core.editor vim
# git config --global core.editor "code --wait"  # VS Code
# git config --global core.editor nano

# Configure pull behavior
git config --global pull.rebase false

# Set up credential helper
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'
```

### SSH Key Setup

If you haven't set up SSH keys for GitHub/GitLab:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub
# Then add this to your GitHub/GitLab account settings
```

## Step 3: Clone the Repository

```bash
# Clone via SSH (recommended)
git clone git@github.com:organization/project-name.git
cd project-name

# OR via HTTPS
git clone https://github.com/organization/project-name.git
cd project-name

# Add upstream remote (if you forked)
git remote add upstream git@github.com:organization/project-name.git

# Verify remotes
git remote -v
```

## Step 4: Set Up Python Environment

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\activate   # Windows

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel
```

### Install Project Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r dev-requirements.txt

# Install package in editable mode
pip install -e .
```

### Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify project imports work
python -c "import myapp; print(myapp.__version__)"
```

## Step 5: Configure Pre-commit Hooks

Pre-commit hooks run checks before each commit to ensure code quality.

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run against all files (optional, to test)
pre-commit run --all-files
```

### Configure Git Hooks (Alternative)

If using project-specific hooks:

```bash
# Enable custom git hooks
make setup-hooks

# Or manually
ln -s ../../.githooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Step 6: Configure Development Tools

### Visual Studio Code

#### Install Extensions

```bash
# Install via command line
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension redhat.vscode-yaml
code --install-extension eamodio.gitlens
```

#### Configure Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "[yaml]": {
        "editor.defaultFormatter": "redhat.vscode-yaml"
    }
}
```

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: Main Module",
            "type": "python",
            "request": "launch",
            "module": "myapp.main",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

### PyCharm

1. Open the project directory in PyCharm
2. Go to **File → Settings → Project → Python Interpreter**
3. Click gear icon → **Add** → **Existing Environment**
4. Select `venv/bin/python`
5. Enable **pytest** as test runner:
   - **Settings → Tools → Python Integrated Tools**
   - Set **Default test runner** to **pytest**

### Vim/Neovim

Add to your `.vimrc` or `init.vim`:

```vim
" Python-specific settings
autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4
autocmd FileType python setlocal textwidth=88

" Install vim-plug if not present
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

" Recommended plugins
call plug#begin()
Plug 'dense-analysis/ale'        " Linting
Plug 'davidhalter/jedi-vim'      " Python completion
Plug 'preservim/nerdtree'        " File explorer
Plug 'airblade/vim-gitgutter'    " Git diff
Plug 'junegunn/fzf.vim'          " Fuzzy finder
call plug#end()
```

## Step 7: Set Up Database (if applicable)

### PostgreSQL

```bash
# Install PostgreSQL
sudo dnf install postgresql-server postgresql-contrib  # Fedora/RHEL
# sudo apt install postgresql postgresql-contrib        # Ubuntu

# Initialize and start
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE myapp_dev;
CREATE USER myapp WITH PASSWORD 'devpassword';
GRANT ALL PRIVILEGES ON DATABASE myapp_dev TO myapp;
\q
```

### SQLite (Development)

```bash
# SQLite is usually included with Python
# Initialize database
python scripts/init_db.py

# Or using make
make db-init
```

## Step 8: Set Up Container Environment

### Podman (Linux)

```bash
# Already installed in Step 1
# Configure rootless mode
podman info

# Test
podman run --rm hello-world
```

### Docker (macOS/Windows)

```bash
# macOS
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Verify
docker run --rm hello-world
```

## Step 9: Configure Environment Variables

Create `.env` file in project root:

```bash
# Copy from example
cp .env.example .env

# Edit with your settings
vim .env
```

Example `.env`:

```bash
# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://myapp:devpassword@localhost/myapp_dev
# or for SQLite
# DATABASE_URL=sqlite:///./dev.db

# API Keys (get from team)
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here

# External Services
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

**Important**: Never commit `.env` file (should be in `.gitignore`)!

## Step 10: Verify Setup

Run the verification script:

```bash
# Automated verification
make verify-setup

# Manual verification steps
python --version              # Should show Python 3.11+
pip list                      # Should show all dependencies
git --version                 # Should show Git 2.x+
podman --version              # Should show Podman version
pre-commit --version          # Should show pre-commit version

# Test imports
python -c "import myapp; print('✓ Package imports successfully')"

# Run tests
make test

# Expected output: All tests passing
```

## Step 11: Run the Application

```bash
# Start in development mode
make dev

# Or manually
python -m myapp.main

# Application should start on http://localhost:8000
```

Test the application:

```bash
# In another terminal
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}
```

## Troubleshooting

### Common Issues

#### Python Version Mismatch

**Problem**: System has wrong Python version

**Solution**:
```bash
# Install specific Python version
sudo dnf install python3.11

# Use that version explicitly
python3.11 -m venv venv
```

#### Permission Errors

**Problem**: Permission denied errors

**Solution**:
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/project-name

# Fix permissions
chmod +x scripts/*.sh
```

#### Virtual Environment Activation Fails

**Problem**: `venv/bin/activate` not found

**Solution**:
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Dependencies Won't Install

**Problem**: Pip install fails with compilation errors

**Solution**:
```bash
# Install system development tools
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Try again
pip install -r requirements.txt
```

#### Podman/Docker Issues

**Problem**: Cannot connect to container daemon

**Solution**:
```bash
# For Podman - ensure rootless is configured
podman info

# For Docker - ensure daemon is running
sudo systemctl start docker  # Linux
# or start Docker Desktop      # macOS/Windows
```

### Getting Help

If you encounter issues not covered here:

1. Check [Troubleshooting Guide](../troubleshooting.md)
2. Search [existing issues](issues-url)
3. Ask in [Slack/Teams channel](chat-url)
4. Create a [new issue](issues-url/new)

## Next Steps

Now that your environment is set up:

1. **[Development Workflow](workflow.md)** - Learn the day-to-day workflow
2. **[Coding Standards](coding-standards.md)** - Review code standards
3. **[Testing Guide](testing.md)** - Learn how to write and run tests
4. **[Contributing Guide](../../CONTRIBUTING.md)** - Start contributing!

## Environment Maintenance

### Keeping Dependencies Updated

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update development dependencies
pip install --upgrade -r dev-requirements.txt

# Update pre-commit hooks
pre-commit autoupdate
```

### Regular Maintenance

```bash
# Update repository
git fetch upstream
git checkout main
git merge upstream/main

# Clean build artifacts
make clean

# Rebuild if needed
make build

# Re-run tests
make test
```

### Switching Python Versions

```bash
# Deactivate current environment
deactivate

# Remove old venv
rm -rf venv

# Create new venv with different Python
python3.12 -m venv venv

# Activate and reinstall
source venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
```



