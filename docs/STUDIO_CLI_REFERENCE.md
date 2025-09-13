# LangGraph Studio CLI Reference

## Quick Start Commands

### Development Server
```bash
# Start development server (default port 8000)
uv run langgraph dev

# Start with custom port
uv run langgraph dev --port 8001

# Start without opening browser
uv run langgraph dev --no-browser

# Start with custom config
uv run langgraph dev --config my_config.json
```

### Production Server
```bash
# Start production server
uv run langgraph up

# Start with custom settings
uv run langgraph up --port 8080 --host 0.0.0.0
```

## Complete CLI Reference

### `langgraph dev` - Development Server

Start a development server with hot reloading and debugging support.

#### Basic Usage
```bash
uv run langgraph dev [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | INTEGER | 8000 | Port number to bind the development server to |
| `--host` | TEXT | 127.0.0.1 | Network interface to bind the development server to |
| `--config` | PATH | langgraph.json | Path to configuration file |
| `--no-browser` | FLAG | False | Skip automatically opening the browser |
| `--no-reload` | FLAG | False | Disable automatic reloading when code changes |
| `--tunnel` | FLAG | False | Expose the local server via a public tunnel |
| `--allow-blocking` | FLAG | False | Don't raise errors for synchronous I/O blocking operations |
| `--wait-for-client` | FLAG | False | Wait for a debugger client to connect |
| `--debug-port` | INTEGER | None | Enable remote debugging by listening on specified port |
| `--server-log-level` | TEXT | info | Set the log level for the API server |
| `--n-jobs-per-worker` | INTEGER | 10 | Maximum number of concurrent jobs each worker process can handle |
| `--studio-url` | TEXT | https://smith.langchain.com | URL of the LangGraph Studio instance to connect to |

#### Examples

```bash
# Basic development server
uv run langgraph dev

# Custom port and host
uv run langgraph dev --port 9000 --host 0.0.0.0

# With remote debugging
uv run langgraph dev --debug-port 5678

# With public tunnel (for remote access)
uv run langgraph dev --tunnel

# Disable auto-reload for debugging
uv run langgraph dev --no-reload

# Custom configuration file
uv run langgraph dev --config production.json

# Verbose logging
uv run langgraph dev --server-log-level debug
```

### `langgraph up` - Production Server

Launch a production-ready LangGraph API server.

#### Basic Usage
```bash
uv run langgraph up [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | INTEGER | 8000 | Port number to bind the server to |
| `--host` | TEXT | 127.0.0.1 | Network interface to bind the server to |
| `--config` | PATH | langgraph.json | Path to configuration file |

#### Examples

```bash
# Start production server
uv run langgraph up

# Custom port and host
uv run langgraph up --port 8080 --host 0.0.0.0

# With custom config
uv run langgraph up --config production.json
```

### `langgraph build` - Build Docker Image

Build a Docker image for the LangGraph API server.

#### Basic Usage
```bash
uv run langgraph build [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--config` | PATH | langgraph.json | Path to configuration file |
| `--tag` | TEXT | None | Docker image tag |
| `--platform` | TEXT | linux/amd64 | Target platform for the build |

#### Examples

```bash
# Build with default settings
uv run langgraph build

# Build with custom tag
uv run langgraph build --tag my-langgraph-app:latest

# Build for specific platform
uv run langgraph build --platform linux/arm64
```

### `langgraph dockerfile` - Generate Dockerfile

Generate a Dockerfile for the LangGraph API server.

#### Basic Usage
```bash
uv run langgraph dockerfile [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--config` | PATH | langgraph.json | Path to configuration file |
| `--output` | PATH | Dockerfile | Output path for the Dockerfile |

#### Examples

```bash
# Generate default Dockerfile
uv run langgraph dockerfile

# Generate with custom name
uv run langgraph dockerfile --output MyDockerfile

# Generate for specific config
uv run langgraph dockerfile --config production.json
```

### `langgraph new` - Create New Project

Create a new LangGraph project from a template.

#### Basic Usage
```bash
uv run langgraph new [OPTIONS] PROJECT_NAME
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--template` | TEXT | basic | Template to use for the project |
| `--path` | PATH | . | Path where to create the project |

#### Examples

```bash
# Create new project
uv run langgraph new my-agent-project

# Create with specific template
uv run langgraph new my-project --template advanced

# Create in specific directory
uv run langgraph new my-project --path /path/to/projects
```

## Configuration Files

### langgraph.json

Main configuration file for LangGraph projects.

```json
{
  "dependencies": ["."],
  "graphs": {
    "my_graph": "./src/graphs/my_graph.py:create_graph"
  },
  "env": ".env",
  "studio_settings": {
    "port": 8000,
    "host": "localhost",
    "auto_reload": true,
    "debug_mode": true
  }
}
```

#### Configuration Options

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dependencies` | array | Yes | List of dependency paths |
| `graphs` | object | Yes | Graph definitions |
| `env` | string | Yes | Environment file path |
| `studio_settings` | object | No | Studio-specific settings |

### Environment Variables

Required environment variables in `.env` file:

```bash
# Required
GOOGLE_API_KEY=your_google_gemini_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key

# Optional
LANGGRAPH_STUDIO_PORT=8000
LANGGRAPH_STUDIO_HOST=localhost
```

## Common Workflows

### 1. Development Workflow

```bash
# 1. Start development server
uv run langgraph dev

# 2. Open Studio interface
open https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000

# 3. Make changes to your code
# 4. Server auto-reloads
# 5. Test in Studio interface
```

### 2. Production Deployment

```bash
# 1. Build Docker image
uv run langgraph build --tag my-app:latest

# 2. Run production server
uv run langgraph up --port 8080 --host 0.0.0.0

# 3. Or use Docker
docker run -p 8080:8080 my-app:latest
```

### 3. Debugging Workflow

```bash
# 1. Start with debug port
uv run langgraph dev --debug-port 5678

# 2. Connect debugger (VS Code, PyCharm, etc.)
# 3. Set breakpoints in your code
# 4. Test in Studio interface
# 5. Debugger will pause at breakpoints
```

### 4. Remote Development

```bash
# 1. Start with tunnel
uv run langgraph dev --tunnel

# 2. Share the tunnel URL with team
# 3. Team can access Studio interface remotely
# 4. Collaborate on graph development
```

## Troubleshooting Commands

### Check Server Status
```bash
# Check if server is running
curl http://localhost:8000/ok

# Check API documentation
open http://localhost:8000/docs

# Check available graphs
curl http://localhost:8000/assistants
```

### Debug Server Issues
```bash
# Check server logs
uv run langgraph dev --server-log-level debug

# Check for port conflicts
lsof -i :8000

# Kill existing processes
pkill -f "langgraph dev"
```

### Verify Configuration
```bash
# Check configuration file
cat langgraph.json

# Validate graph imports
uv run python -c "from src.graphs.my_graph import create_graph; print('Graph loaded')"

# Check environment variables
uv run python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

## Integration with Development Tools

### VS Code Integration

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug LangGraph",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            }
        }
    ]
}
```

### Docker Integration

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install uv && uv sync

EXPOSE 8000
CMD ["uv", "run", "langgraph", "up", "--host", "0.0.0.0"]
```

### CI/CD Integration

Create `.github/workflows/studio.yml`:
```yaml
name: LangGraph Studio CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install uv
      - run: uv sync
      - run: uv run langgraph dev --no-browser &
      - run: sleep 10
      - run: curl http://localhost:8000/ok
      - run: uv run pytest
```

## Performance Optimization

### Server Tuning
```bash
# Increase worker processes
uv run langgraph dev --n-jobs-per-worker 20

# Use specific host for better performance
uv run langgraph dev --host 127.0.0.1

# Disable auto-reload in production
uv run langgraph up --no-reload
```

### Resource Monitoring
```bash
# Monitor server resources
htop

# Check memory usage
ps aux | grep langgraph

# Monitor network connections
netstat -tulpn | grep 8000
```

---

*This reference covers the most commonly used LangGraph Studio CLI commands. For the complete API reference, visit the [official documentation](https://langchain-ai.github.io/langgraph/).*
