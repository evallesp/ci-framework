# Documentation Template Customization Guide

This guide explains how to customize this documentation template for your specific project.

## Quick Start

1. **Replace Placeholders**
2. **Customize Content**  
3. **Remove Unnecessary Sections**
4. **Add Project-Specific Details**

## Placeholders to Replace

Search and replace these throughout all documentation files:

### Basic Information

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `<project-name>` | Your project name | `ci-framework` |
| `<repository-url>` | Your repo URL | `https://github.com/org/project` |
| `myapp` | Your app name | `cifmw` |
| `organization` | Your organization | `openstack-k8s-operators` |
| `example.com` | Your domain | `redhat.com` |

### URLs and Links

| Placeholder | Replace With |
|-------------|--------------|
| `issues-url` | Your issues page URL |
| `discussions-url` | Your discussions page URL |
| `chat-url` | Your chat/Slack URL |
| `blog-url` | Your blog URL |
| `wiki-url` | Your wiki URL |

### Contact Information

| Placeholder | Replace With |
|-------------|--------------|
| `support@example.com` | Your support email |
| `security@example.com` | Your security email |
| `docs@example.com` | Your documentation email |
| `team@example.com` | Your team email |

### Project Specifics

| Placeholder | Replace With |
|-------------|--------------|
| `[LICENSE]` | Your actual license |
| `[Organization/Team Name]` | Your team name |
| `[Brief description...]` | Your project description |

## Find and Replace Commands

### Using grep and sed (Linux/macOS)

```bash
# Navigate to documentation template
cd documentation-template/

# Find all occurrences of placeholder
grep -r "<project-name>" .

# Replace in all markdown files
find . -type f -name "*.md" -exec sed -i 's/<project-name>/your-actual-project-name/g' {} +

# Replace in all files
find . -type f -exec sed -i 's/example\.com/yourdomain.com/g' {} +

# Replace email addresses
find . -type f -name "*.md" -exec sed -i 's/support@example\.com/support@yourdomain.com/g' {} +
```

### Using VS Code

1. Press `Ctrl+Shift+H` (or `Cmd+Shift+H` on Mac)
2. Enter search term (e.g., `<project-name>`)
3. Enter replacement (e.g., `ci-framework`)
4. Click "Replace All"

### Using sed Script

```bash
#!/bin/bash
# replace-placeholders.sh

# Project specifics
sed -i 's/<project-name>/your-project-name/g' $(find . -type f -name "*.md")
sed -i 's/<repository-url>/your-repo-url/g' $(find . -type f -name "*.md")
sed -i 's/myapp/yourapp/g' $(find . -type f -name "*.md")
sed -i 's/example\.com/yourdomain.com/g' $(find . -type f -name "*.md")

# Emails
sed -i 's/support@example\.com/support@yourdomain.com/g' $(find . -type f -name "*.md")
sed -i 's/security@example\.com/security@yourdomain.com/g' $(find . -type f -name "*.md")

echo "Placeholders replaced!"
```

## Content Customization

### README.md

1. **Update Project Description**: Replace generic description with yours
2. **Update Features**: List your actual features
3. **Update Prerequisites**: Match your requirements
4. **Update Quick Start**: Adjust for your installation

### CONTRIBUTING.md

1. **Code of Conduct**: Add your organization's code of conduct
2. **Branch Naming**: Adjust to your conventions
3. **Commit Format**: Use your preferred format
4. **Review Process**: Match your review workflow
5. **Approval Requirements**: Set your approval policy

### Documentation Files

#### docs/getting-started.md
- Update installation steps for your project
- Adjust system requirements
- Modify configuration examples
- Update command examples

#### docs/configuration.md
- Replace with your actual configuration options
- Update environment variables
- Modify configuration file examples
- Add your specific settings

#### docs/development/environment-setup.md
- Update dependencies for your project
- Adjust setup steps
- Modify IDE configurations
- Update tool recommendations

#### docs/architecture/overview.md
- Replace with your actual architecture
- Update component descriptions
- Modify diagrams (create your own)
- Update technology stack

## Technology-Specific Adjustments

### For Python Projects

Keep:
- Python coding standards
- pytest examples
- Type hints documentation
- Virtual environment setup

Update:
- Python version requirements
- Specific packages used
- Framework (Flask/Django/FastAPI)

### For Ansible Projects

Keep:
- Ansible best practices
- YAML linting
- Molecule testing
- Role structure

Update:
- Collection name
- Role naming conventions
- Variable prefixes

### For Non-Python Projects

Replace:
- Language-specific coding standards
- Testing frameworks
- Build tools
- Package managers

## Sections to Remove/Modify

### Might Not Need

- **Database sections** - If not using databases
- **Container sections** - If not using containers
- **API documentation** - If no API
- **Frontend docs** - If backend-only
- **Deployment guides** - If library/SDK only

### Might Need to Add

- **Language-specific sections** - For Go, Rust, Java, etc.
- **Framework-specific docs** - For specific frameworks
- **Cloud-specific guides** - For AWS, GCP, Azure
- **Mobile app docs** - For mobile development
- **Hardware requirements** - For embedded systems

## Adding Project-Specific Content

### Custom Workflows

Add documentation for:
- Specific development workflows
- Custom testing procedures
- Release processes
- Deployment pipelines

### Domain-Specific Content

Add sections for:
- Domain terminology
- Business logic explanations
- Use case scenarios
- Integration guides

### Team-Specific Information

Add:
- Team structure
- Meeting schedules
- Communication channels
- Decision-making process

## Documentation Structure Adjustments

### Reorganize if Needed

```
# Example: Microservices project
docs/
  services/
    service-a/
    service-b/
  shared/
  infrastructure/

# Example: Monorepo
docs/
  backend/
  frontend/
  mobile/
  shared/

# Example: Library
docs/
  api-reference/
  examples/
  guides/
  tutorials/
```

### Add New Sections

```markdown
## New Section Template

### Overview
Brief description of the section

### Prerequisites
What you need to know/have

### Instructions
Step-by-step guide

### Examples
Real-world examples

### Troubleshooting
Common issues

### References
Related documentation
```

## Makefile Customization

### Adjust for Your Build System

```makefile
# For Go projects
build:
	go build -o bin/myapp .

test:
	go test ./...

# For Node.js projects  
build:
	npm run build

test:
	npm test

# For Rust projects
build:
	cargo build --release

test:
	cargo test
```

## Style Customization

### Tone and Voice

Current tone: Professional but friendly

Adjust for:
- **More formal**: Corporate/enterprise
- **More casual**: Startup/community
- **More technical**: Research/academic

### Terminology

Replace generic terms with your:
- Product names
- Feature names
- Component names
- Role titles

## Localization

### Adding Languages

```
docs/
  en/  # English (original)
  es/  # Spanish
  fr/  # French
  ja/  # Japanese
```

### Translation Workflow

1. Copy English docs to new language folder
2. Translate content
3. Update links and references
4. Add language selector to navigation

## Version-Specific Documentation

### Multiple Versions

```
docs/
  v1.0/
  v2.0/
  latest/ -> v2.0/
```

### Version Banner

Add to top of docs:
```markdown
> ⚠️ **Note**: This documentation is for version 2.0.  
> For other versions, see [version selector](/versions).
```

## Integration with Tools

### ReadTheDocs

- Add `.readthedocs.yml`
- Configure build settings
- Set up versioning

### GitHub Pages

- Add `_config.yml`
- Set up deployment workflow
- Configure custom domain

### DocusaurusMkDocs/Sphinx

- Install and configure
- Convert markdown if needed
- Set up theme

## Quality Checks

### Before Publishing

- [ ] All placeholders replaced
- [ ] Links working
- [ ] Code examples tested
- [ ] Screenshots updated
- [ ] Contact info correct
- [ ] License information accurate
- [ ] Version numbers updated
- [ ] Spelling checked
- [ ] Grammar checked
- [ ] Consistent formatting

### Validation Commands

```bash
# Check for unreplaced placeholders
grep -r "<.*>" docs/

# Check for broken links
make docs-check

# Spell check
aspell check docs/**/*.md

# Build docs
make docs
```

## Maintaining Documentation

### Regular Reviews

Schedule reviews:
- **Monthly**: Check for outdated content
- **With releases**: Update version-specific content
- **Quarterly**: Major documentation review
- **Annually**: Complete documentation audit

### Feedback Loop

Collect feedback:
- User surveys
- Issue templates for documentation
- Analytics on popular pages
- Support ticket analysis

### Documentation Debt

Track and address:
- Missing documentation
- Outdated content
- Broken examples
- Unclear explanations

## Getting Help

If you need help customizing:

1. **Check Examples**: Look at similar projects' documentation
2. **Ask Community**: Post in discussions or chat
3. **Create Issue**: Request specific guidance
4. **Hire Consultant**: For large projects

## Recommended Projects to Study

Well-documented projects to learn from:

- **Django**: https://docs.djangoproject.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Kubernetes**: https://kubernetes.io/docs/
- **Ansible**: https://docs.ansible.com/
- **Vue.js**: https://vuejs.org/guide/

## Next Steps

1. **Copy this template** to your project
2. **Run find-and-replace** for all placeholders
3. **Customize content** for your project
4. **Remove this guide** (it's just for setup)
5. **Start writing** your documentation!

Good luck with your documentation! 📚



