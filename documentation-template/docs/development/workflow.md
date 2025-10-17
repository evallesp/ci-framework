# Development Workflow

This guide describes the day-to-day development workflow for contributing to the project.

## Overview

Our development workflow follows these principles:

- **Feature Branch Workflow**: All work happens in feature branches
- **Trunk-Based Development**: Main branch is always deployable
- **Pull Request Review**: All changes go through code review
- **Continuous Integration**: Automated tests run on all PRs
- **Semantic Versioning**: We follow semver for releases

## Daily Workflow

### 1. Start Your Day

```bash
# Navigate to project directory
cd ~/projects/project-name

# Activate virtual environment
source venv/bin/activate

# Update main branch
git checkout main
git pull upstream main

# Check for any updates to dependencies
git diff HEAD@{1} requirements.txt
# If changed, reinstall
pip install -r requirements.txt
```

### 2. Pick a Task

Choose what to work on:

- Browse [open issues](issues-url)
- Check project board
- Discuss with team in standup
- Look for issues labeled `good-first-issue` (for newcomers)

### 3. Create Feature Branch

```bash
# Create and checkout feature branch
git checkout -b feature/add-user-authentication

# Branch naming conventions:
# feature/  - new features
# bugfix/   - bug fixes
# hotfix/   - urgent production fixes
# refactor/ - code refactoring
# docs/     - documentation changes
# test/     - test additions/changes
```

### 4. Development Cycle

#### Write Code

```bash
# Open your editor
code .  # VS Code
# or
vim src/mymodule.py
```

**Best Practices**:
- Write small, focused commits
- Follow [coding standards](coding-standards.md)
- Add docstrings and comments
- Keep functions/methods small and focused

#### Run Tests Frequently

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_mymodule.py

# Run tests in watch mode (auto-rerun on changes)
pytest-watch

# Run only failed tests from last run
pytest --lf
```

#### Check Code Quality

```bash
# Run linters
make lint

# Auto-format code
make format

# Type checking
make type-check

# All quality checks at once
make quality
```

### 5. Commit Your Changes

#### Staging Changes

```bash
# View changes
git status
git diff

# Stage specific files
git add src/mymodule.py tests/test_mymodule.py

# Stage all changes (use carefully)
git add .

# Stage interactively (recommended for partial commits)
git add -p
```

#### Writing Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples**:

```bash
# Simple commit
git commit -m "feat: add user authentication"

# With scope
git commit -m "fix(api): handle null response in user endpoint"

# With body and footer
git commit -m "feat(auth): implement OAuth2 authentication

- Add OAuth2 client configuration
- Implement token refresh mechanism
- Add integration tests for OAuth flow

Closes #123
Refs #456"
```

**Commit Message Best Practices**:
- Use imperative mood ("add" not "added")
- First line < 50 characters
- Body lines < 72 characters
- Explain *what* and *why*, not *how*
- Reference related issues

#### Committing

```bash
# Commit staged changes
git commit

# Quick commit (for small changes)
git commit -m "fix: correct typo in error message"

# Amend last commit (if not pushed yet)
git commit --amend

# Amend without changing message
git commit --amend --no-edit
```

### 6. Keep Branch Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase on main (recommended)
git rebase upstream/main

# If conflicts occur
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git rebase --continue

# If rebase gets messy, abort and try merge
git rebase --abort
git merge upstream/main
```

### 7. Push to Your Fork

```bash
# First push
git push -u origin feature/add-user-authentication

# Subsequent pushes
git push

# Force push after rebase (use with caution)
git push --force-with-lease
```

### 8. Create Pull Request

#### Open PR

1. Go to repository on GitHub/GitLab
2. Click "New Pull Request" or "Create Merge Request"
3. Select your branch
4. Fill out PR template:

```markdown
## Description
Add OAuth2 authentication support for external identity providers

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Implemented OAuth2 client with support for Google and GitHub
- Added token refresh mechanism with automatic retry
- Created integration tests with mock OAuth provider
- Updated documentation with OAuth configuration examples

## Testing Done
- [x] All existing tests pass
- [x] Added unit tests for OAuth client
- [x] Added integration tests for full OAuth flow
- [x] Manual testing with Google OAuth
- [x] Tested token refresh scenario

## Screenshots
![Login screen with OAuth buttons](screenshot.png)

## Checklist
- [x] Code follows style guidelines
- [x] Self-reviewed my code
- [x] Commented complex logic
- [x] Updated documentation
- [x] No new warnings
- [x] Added tests
- [x] All tests passing

## Additional Notes
Configuration requires setting OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET environment variables.
```

#### PR Best Practices

- **Keep PRs Small**: < 400 lines of changes
- **One Concern Per PR**: Don't mix features
- **Self Review First**: Review your own PR before requesting reviews
- **Draft PRs**: Use draft status for work in progress
- **Link Issues**: Always link related issues

### 9. Respond to Review Feedback

#### Address Comments

```bash
# Make requested changes
vim src/mymodule.py

# Commit changes
git add .
git commit -m "refactor: extract validation logic to separate function"

# Push updates
git push
```

#### Respond to Comments

- **Be Respectful**: Assume good intentions
- **Explain Decisions**: If you disagree, explain why
- **Ask Questions**: If unclear, ask for clarification
- **Mark Resolved**: Mark conversations as resolved when addressed

#### Example Responses

Good:
```
Good catch! I've extracted that validation logic into a separate 
function as you suggested. Also added unit tests for it.
```

```
I considered that approach, but went with this implementation 
because it handles edge case X better. However, I'm open to 
alternatives if you have suggestions.
```

```
I'm not sure I understand this comment. Could you provide an 
example of what you're suggesting?
```

### 10. Keep PR Updated

```bash
# If main branch has moved ahead
git fetch upstream
git rebase upstream/main
git push --force-with-lease

# Squash commits if requested
git rebase -i HEAD~3  # Interactive rebase last 3 commits
# Mark commits as 'squash' in editor
git push --force-with-lease
```

### 11. After Merge

```bash
# Switch to main branch
git checkout main

# Pull merged changes
git pull upstream main

# Delete local feature branch
git branch -d feature/add-user-authentication

# Delete remote feature branch
git push origin --delete feature/add-user-authentication

# Clean up
make clean
```

## Advanced Workflows

### Working on Multiple Features

```bash
# Use git worktree for multiple concurrent branches
git worktree add ../project-feature-2 feature/another-feature

# Now you can work in different directories
cd ../project-feature-2
# Work on feature 2

# Switch back
cd ../project-name
# Work on original feature
```

### Handling Long-Running Features

```bash
# Create feature branch
git checkout -b feature/big-feature

# Regularly sync with main
git fetch upstream
git rebase upstream/main

# Break into smaller PRs
git checkout -b feature/big-feature-part-1
# Cherry-pick relevant commits
git cherry-pick <commit-hash>
git push origin feature/big-feature-part-1
# Create PR for part 1

# Repeat for subsequent parts
```

### Debugging Failed Tests

```bash
# Run failing test with verbose output
pytest -vv tests/test_mymodule.py::test_failing

# Run with debugger
pytest --pdb tests/test_mymodule.py::test_failing

# Run with print statements visible
pytest -s tests/test_mymodule.py

# Show slow tests
pytest --durations=10
```

### Bisecting to Find Bugs

```bash
# Find commit that introduced bug
git bisect start
git bisect bad                # Current commit is bad
git bisect good <commit-hash>  # Known good commit

# Git will checkout middle commit
make test
git bisect good  # or git bisect bad

# Repeat until bug is found
# When done
git bisect reset
```

## Workflow Tips

### Productivity Tips

1. **Use Aliases**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   alias gst='git status'
   alias gco='git checkout'
   alias gp='git push'
   alias gl='git pull'
   alias gd='git diff'
   alias gc='git commit'
   alias glog='git log --oneline --graph --all'
   ```

2. **Use Git Hooks**:
   - Pre-commit: Run linters automatically
   - Pre-push: Run tests before pushing
   - Commit-msg: Validate commit message format

3. **Use Make Targets**:
   ```bash
   make help  # See all available commands
   make dev   # Start development server
   make test-watch  # Run tests on file changes
   ```

4. **Use IDE Integration**:
   - Configure test runners in IDE
   - Use built-in Git tools
   - Set up debugging configurations

### Avoiding Common Pitfalls

❌ **DON'T**:
- Commit directly to main branch
- Force push to shared branches
- Mix unrelated changes in one commit
- Write vague commit messages
- Skip running tests before pushing
- Leave debugging code in commits

✅ **DO**:
- Work in feature branches
- Write descriptive commit messages
- Run tests before pushing
- Keep commits atomic and focused
- Review your own PRs first
- Ask for help when stuck

### Time Management

**Morning Routine** (30 min):
- Check notifications and reviews
- Update main branch
- Plan daily tasks
- Start development

**Focus Time** (2-3 hours):
- Deep work on features
- Minimize distractions
- Run tests frequently

**Lunch Break**:
- Let CI run while you're away

**Afternoon** (2-3 hours):
- Address review comments
- Code review for others
- Documentation updates

**End of Day** (15 min):
- Commit work in progress
- Push to backup
- Update task status

## Getting Help

### When Stuck

1. **Read Documentation**: Check project docs
2. **Search Issues**: Look for similar problems
3. **Ask Team**: Post in chat channel
4. **Pair Programming**: Schedule session with teammate
5. **Create Issue**: Document problem for team

### Questions to Ask

- **Slack/Teams**: Quick questions, discussions
- **GitHub Discussions**: Design decisions, proposals
- **Issues**: Bug reports, feature requests
- **Office Hours**: Complex problems, guidance

## Next Steps

- **[Testing Guide](testing.md)** - Learn testing practices
- **[Debugging Guide](debugging.md)** - Debug issues effectively
- **[Coding Standards](coding-standards.md)** - Code style guide
- **[Review Checklist](review-checklist.md)** - What to check in reviews



