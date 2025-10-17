# Configuration Guide

Complete guide to configuring the application.

## Configuration Overview

The application can be configured through:

1. **Configuration Files** (YAML/JSON)
2. **Environment Variables**
3. **Command-Line Arguments**

**Priority Order** (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Configuration file
4. Default values

## Configuration File

### Location

Default locations (checked in order):
1. `./config/config.yml`
2. `~/.myapp/config.yml`
3. `/etc/myapp/config.yml`

Specify custom location:
```bash
./myapp --config /path/to/config.yml
```

### Format

Configuration uses YAML format:

```yaml
# config.yml
---
# Application settings
app:
  name: myapp
  version: 1.0.0
  environment: production  # development, staging, production
  debug: false
  
# Server settings
server:
  host: 0.0.0.0
  port: 8000
  workers: 4
  timeout: 30
  
  # SSL/TLS configuration
  ssl:
    enabled: true
    cert_file: /path/to/cert.pem
    key_file: /path/to/key.pem
    
# Database configuration
database:
  # Connection URL format:
  # postgresql://user:password@host:port/database
  url: postgresql://myapp:password@localhost:5432/myapp_prod
  
  # Connection pool
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
  pool_recycle: 3600
  
  # Query settings
  echo: false  # Log SQL queries
  echo_pool: false  # Log connection pool events
  
# Cache configuration
cache:
  enabled: true
  backend: redis  # redis, memcached, memory
  
  # Redis settings
  redis:
    host: localhost
    port: 6379
    db: 0
    password: null
    ssl: false
    max_connections: 50
    
  # Cache TTL (seconds)
  default_timeout: 3600
  
# Logging configuration
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: json  # text, json
  
  # Log outputs
  outputs:
    - type: console
      level: INFO
    - type: file
      level: DEBUG
      path: /var/log/myapp/app.log
      max_size: 100MB
      backup_count: 10
      
# Security settings
security:
  # JWT configuration
  jwt:
    secret_key: ${JWT_SECRET_KEY}  # Use env var
    algorithm: HS256
    access_token_expire: 3600  # seconds
    refresh_token_expire: 604800  # 7 days
    
  # CORS settings
  cors:
    enabled: true
    origins:
      - https://example.com
      - https://app.example.com
    allow_credentials: true
    max_age: 3600
    
  # Rate limiting
  rate_limit:
    enabled: true
    default: 100/hour
    endpoints:
      /api/auth/login: 5/minute
      /api/users: 1000/hour
      
# Feature flags
features:
  new_ui: true
  beta_features: false
  advanced_analytics: true
  
# External services
services:
  # Email service
  email:
    enabled: true
    backend: smtp  # smtp, sendgrid, ses
    from_address: noreply@example.com
    
    smtp:
      host: smtp.example.com
      port: 587
      username: ${SMTP_USERNAME}
      password: ${SMTP_PASSWORD}
      use_tls: true
      
  # Storage service
  storage:
    backend: s3  # s3, local, gcs, azure
    
    s3:
      bucket: myapp-storage
      region: us-east-1
      access_key_id: ${AWS_ACCESS_KEY_ID}
      secret_access_key: ${AWS_SECRET_ACCESS_KEY}
      
  # Monitoring
  monitoring:
    enabled: true
    sentry:
      dsn: ${SENTRY_DSN}
      environment: production
      sample_rate: 1.0
      
    metrics:
      enabled: true
      port: 9090
      path: /metrics
```

## Environment Variables

### Setting Environment Variables

**Linux/macOS**:
```bash
export DATABASE_URL=postgresql://user:pass@localhost/db
export DEBUG=true
export LOG_LEVEL=DEBUG
```

**Windows**:
```powershell
$env:DATABASE_URL="postgresql://user:pass@localhost/db"
$env:DEBUG="true"
$env:LOG_LEVEL="DEBUG"
```

**Using .env File**:
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=true
LOG_LEVEL=DEBUG
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key-here
```

Load .env file:
```bash
# Using direnv
echo "dotenv" >> .envrc
direnv allow

# Using python-dotenv (automatically loaded by app)
pip install python-dotenv
```

### Environment Variable Reference

#### Application

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_ENV` | string | `production` | Environment (development, staging, production) |
| `DEBUG` | boolean | `false` | Enable debug mode |
| `LOG_LEVEL` | string | `INFO` | Logging level |

#### Server

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HOST` | string | `0.0.0.0` | Server host |
| `PORT` | integer | `8000` | Server port |
| `WORKERS` | integer | `4` | Number of worker processes |

#### Database

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | Required | Database connection URL |
| `DB_POOL_SIZE` | integer | `10` | Connection pool size |
| `DB_ECHO` | boolean | `false` | Log SQL queries |

#### Cache

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `REDIS_URL` | string | `redis://localhost:6379/0` | Redis connection URL |
| `CACHE_ENABLED` | boolean | `true` | Enable caching |
| `CACHE_TTL` | integer | `3600` | Default cache TTL (seconds) |

#### Security

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `JWT_SECRET_KEY` | string | Required | JWT signing secret |
| `JWT_ALGORITHM` | string | `HS256` | JWT algorithm |
| `ALLOWED_ORIGINS` | string | `*` | CORS allowed origins (comma-separated) |

#### External Services

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SMTP_HOST` | string | - | SMTP server host |
| `SMTP_PORT` | integer | `587` | SMTP server port |
| `SMTP_USERNAME` | string | - | SMTP username |
| `SMTP_PASSWORD` | string | - | SMTP password |
| `AWS_ACCESS_KEY_ID` | string | - | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | string | - | AWS secret key |
| `SENTRY_DSN` | string | - | Sentry DSN for error tracking |

### Variable Substitution in Config Files

Use `${VARIABLE_NAME}` syntax in config files:

```yaml
database:
  url: ${DATABASE_URL}
  
security:
  jwt:
    secret_key: ${JWT_SECRET_KEY}
    
services:
  email:
    smtp:
      username: ${SMTP_USERNAME}
      password: ${SMTP_PASSWORD}
```

## Command-Line Arguments

### Basic Usage

```bash
./myapp [OPTIONS] COMMAND [ARGS]
```

### Global Options

```bash
# Configuration file
./myapp --config config.yml

# Environment
./myapp --env production

# Debug mode
./myapp --debug

# Log level
./myapp --log-level DEBUG

# Verbose output
./myapp -v
./myapp -vv  # More verbose
./myapp -vvv # Most verbose
```

### Examples

```bash
# Start with custom config
./myapp --config config/production.yml run

# Override port
./myapp --port 8080 run

# Debug mode with verbose logging
./myapp --debug --log-level DEBUG run

# Multiple options
./myapp \
  --config config/custom.yml \
  --env staging \
  --port 9000 \
  --workers 8 \
  run
```

## Configuration by Environment

### Development

```yaml
# config/development.yml
app:
  environment: development
  debug: true
  
server:
  host: localhost
  port: 8000
  workers: 1
  reload: true  # Auto-reload on code changes
  
database:
  url: postgresql://dev:dev@localhost/myapp_dev
  echo: true  # Log SQL queries
  
cache:
  backend: memory  # Simpler cache for development
  
logging:
  level: DEBUG
  format: text
```

Usage:
```bash
./myapp --config config/development.yml run
# or
APP_ENV=development ./myapp run
```

### Staging

```yaml
# config/staging.yml
app:
  environment: staging
  debug: false
  
server:
  host: 0.0.0.0
  port: 8000
  workers: 4
  
database:
  url: ${DATABASE_URL}
  pool_size: 5
  
cache:
  enabled: true
  backend: redis
  
logging:
  level: INFO
  outputs:
    - type: console
    - type: file
      path: /var/log/myapp/staging.log
      
services:
  monitoring:
    enabled: true
    sentry:
      environment: staging
      sample_rate: 0.5
```

### Production

```yaml
# config/production.yml
app:
  environment: production
  debug: false
  
server:
  host: 0.0.0.0
  port: 8000
  workers: 8
  timeout: 60
  
database:
  url: ${DATABASE_URL}
  pool_size: 20
  max_overflow: 40
  
cache:
  enabled: true
  backend: redis
  redis:
    host: ${REDIS_HOST}
    port: ${REDIS_PORT}
    password: ${REDIS_PASSWORD}
    ssl: true
    
logging:
  level: WARNING
  format: json
  outputs:
    - type: file
      path: /var/log/myapp/production.log
      max_size: 500MB
      backup_count: 30
      
security:
  jwt:
    secret_key: ${JWT_SECRET_KEY}
  cors:
    origins:
      - https://app.example.com
      - https://www.example.com
  rate_limit:
    enabled: true
    
services:
  monitoring:
    enabled: true
    sentry:
      dsn: ${SENTRY_DSN}
      environment: production
      sample_rate: 1.0
```

## Validating Configuration

### Validate Config File

```bash
# Check configuration syntax
./myapp config validate

# Show effective configuration
./myapp config show

# Show configuration with resolved variables
./myapp config show --resolve
```

### Configuration Schema

The application validates configuration against a schema:

```python
from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(8000, ge=1024, le=65535)
    workers: int = Field(4, ge=1, le=32)

class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = Field(10, ge=1, le=100)
    
class Config(BaseModel):
    server: ServerConfig
    database: DatabaseConfig
```

## Best Practices

### Security

1. **Never commit secrets**:
   ```yaml
   # Bad
   database:
     url: postgresql://user:password123@localhost/db
   
   # Good
   database:
     url: ${DATABASE_URL}
   ```

2. **Use secret management**:
   ```bash
   # AWS Secrets Manager
   export DATABASE_URL=$(aws secretsmanager get-secret-value \
     --secret-id prod/database/url --query SecretString --output text)
   
   # HashiCorp Vault
   export JWT_SECRET_KEY=$(vault kv get -field=secret auth/jwt)
   ```

3. **Restrict config file permissions**:
   ```bash
   chmod 600 config/production.yml
   chown myapp:myapp config/production.yml
   ```

### Organization

1. **Separate configs by environment**
2. **Use configuration templates**
3. **Document all options**
4. **Version control configs** (except secrets)
5. **Validate on startup**

### Performance

1. **Cache configuration values**
2. **Lazy load when possible**
3. **Use connection pooling**
4. **Set appropriate timeouts**

## Troubleshooting

### Configuration Not Loading

```bash
# Check file exists
ls -la config/config.yml

# Validate syntax
python -c "import yaml; yaml.safe_load(open('config/config.yml'))"

# Check file permissions
chmod 644 config/config.yml

# Enable config debug
DEBUG_CONFIG=true ./myapp run
```

### Environment Variables Not Working

```bash
# Check variable is set
echo $DATABASE_URL

# Check spelling and case (variables are case-sensitive)
env | grep -i database

# Check for extra spaces
echo "[$DATABASE_URL]"  # Should not have spaces

# Export in same shell session
export DATABASE_URL=value
./myapp run  # Same session
```

### Configuration Conflicts

```bash
# See effective configuration
./myapp config show --verbose

# See configuration sources
./myapp config show --show-source
```

## Advanced Topics

### Dynamic Configuration

Reload configuration without restart:

```python
# Send SIGHUP to reload config
kill -HUP <pid>

# Or via API
curl -X POST http://localhost:8000/admin/reload-config
```

### Configuration Profiles

```yaml
# config.yml with profiles
---
_default: &default
  app:
    name: myapp
  server:
    host: 0.0.0.0
    
development:
  <<: *default
  app:
    debug: true
    
production:
  <<: *default
  app:
    debug: false
```

Usage:
```bash
./myapp --profile production run
```

## References

- [Environment Variables Guide](https://12factor.net/config)
- [YAML Syntax](https://yaml.org/)
- [Security Best Practices](security.md)

## Need Help?

- [Configuration Examples](../examples/configs/)
- [FAQ](FAQ.md#configuration)
- [Troubleshooting](troubleshooting.md)
- [GitHub Issues](issues-url)



