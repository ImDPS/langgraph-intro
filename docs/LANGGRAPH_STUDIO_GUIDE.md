# LangGraph Studio: Complete Setup and Integration Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation and Setup](#installation-and-setup)
4. [Project Configuration](#project-configuration)
5. [CLI Commands](#cli-commands)
6. [Graph Integration](#graph-integration)
7. [Studio Interface](#studio-interface)
8. [Development Workflow](#development-workflow)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [Advanced Features](#advanced-features)

## Overview

LangGraph Studio is a powerful visual development environment for building, debugging, and deploying AI agents using the LangGraph framework. It provides an intuitive interface for creating complex agent workflows, real-time debugging, and seamless integration with production deployment.

### Key Features
- **🎨 Visual Graph Editor**: Drag-and-drop interface for building agent workflows
- **🔍 Real-time Debugging**: Live state inspection and step-by-step execution
- **📊 Interactive Testing**: Test agents with real-time feedback
- **🔄 Seamless Integration**: Export to production-ready Python code
- **📈 Performance Monitoring**: Built-in analytics and monitoring
- **👥 Team Collaboration**: Share and collaborate on agent designs

## Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Operating System**: macOS, Linux, or Windows
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space

### Required Accounts
- **LangSmith Account**: Free account at [smith.langchain.com](https://smith.langchain.com)
- **API Keys**: Google Gemini API key (or other LLM provider)

### Development Tools
- **uv**: Modern Python package manager
- **Git**: Version control
- **Docker**: For containerized deployment (optional)

## Installation and Setup

### Step 1: Install LangGraph CLI

```bash
# Install LangGraph CLI with in-memory runtime
uv add "langgraph-cli[inmem]"

# Verify installation
uv run langgraph --version
```

### Step 2: Project Structure

Ensure your project has the following structure:

```
your-project/
├── langgraph.json          # Studio configuration
├── pyproject.toml          # Project dependencies
├── .env                    # Environment variables
├── src/                    # Source code
│   └── your_graphs/        # Graph implementations
└── tests/                  # Test files
```

### Step 3: Environment Configuration

Create a `.env` file with your API keys:

```bash
# Required API Keys
GOOGLE_API_KEY=your_google_gemini_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here

# Optional Configuration
LANGGRAPH_STUDIO_PORT=8000
LANGGRAPH_STUDIO_HOST=localhost
```

### Step 4: Install Dependencies

```bash
# Install all project dependencies
uv sync

# Verify LangGraph installation
uv run python -c "import langgraph; print('LangGraph installed successfully!')"
```

## Project Configuration

### langgraph.json Configuration

Create a `langgraph.json` file in your project root:

```json
{
  "dependencies": ["."],
  "graphs": {
    "simple_graph": "./src/graphs/simple_graph.py:create_simple_graph",
    "complex_agent": "./src/agents/complex_agent.py:create_agent"
  },
  "env": ".env"
}
```

#### Configuration Options

| Field | Description | Required |
|-------|-------------|----------|
| `dependencies` | List of dependency paths | Yes |
| `graphs` | Graph definitions with paths | Yes |
| `env` | Environment file path | Yes |
| `studio_settings` | Studio-specific settings | No |

#### Advanced Configuration

```json
{
  "dependencies": ["."],
  "graphs": {
    "my_graph": {
      "path": "./src/graphs/my_graph.py:create_graph",
      "description": "My custom graph",
      "tags": ["production", "demo"]
    }
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

### pyproject.toml Integration

Ensure your `pyproject.toml` includes the necessary dependencies:

```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "langgraph>=0.2.0",
    "langchain>=0.3.0",
    "langgraph-cli[inmem]>=0.4.2",
    "google-generativeai>=0.8.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]
```

## CLI Commands

### Basic Commands

#### Start Development Server
```bash
# Start with default settings
uv run langgraph dev

# Start with custom port
uv run langgraph dev --port 8000

# Start without opening browser
uv run langgraph dev --no-browser

# Start with custom configuration
uv run langgraph dev --config custom_config.json
```

#### Production Server
```bash
# Start production server
uv run langgraph up

# Start with custom settings
uv run langgraph up --port 8080 --host 0.0.0.0
```

#### Build and Deploy
```bash
# Build Docker image
uv run langgraph build

# Generate Dockerfile
uv run langgraph dockerfile

# Create new project from template
uv run langgraph new my-project
```

### Advanced CLI Options

#### Development Server Options
```bash
uv run langgraph dev \
  --port 8000 \
  --host localhost \
  --config langgraph.json \
  --no-browser \
  --no-reload \
  --debug-port 5678 \
  --tunnel \
  --allow-blocking
```

| Option | Description | Default |
|--------|-------------|---------|
| `--port` | Server port | 8000 |
| `--host` | Server host | 127.0.0.1 |
| `--config` | Configuration file | langgraph.json |
| `--no-browser` | Don't open browser | false |
| `--no-reload` | Disable auto-reload | false |
| `--debug-port` | Debug port | none |
| `--tunnel` | Public tunnel | false |
| `--allow-blocking` | Allow blocking I/O | false |

#### Server Management
```bash
# Check server status
curl http://localhost:8000/ok

# View API documentation
open http://localhost:8000/docs

# Check available graphs
curl http://localhost:8000/assistants
```

## Graph Integration

### Creating a Graph for Studio

#### Basic Graph Structure
```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    """State schema for the graph"""
    message: str
    response: str
    history: list[str]

def process_message(state: GraphState) -> GraphState:
    """Process incoming message"""
    message = state.get("message", "")
    response = f"Processed: {message}"
    
    return {
        "message": message,
        "response": response,
        "history": state.get("history", []) + [message]
    }

def create_my_graph():
    """Create the graph for Studio integration"""
    graph = StateGraph(GraphState)
    
    # Add nodes
    graph.add_node("process_message", process_message)
    
    # Set entry and finish points
    graph.set_entry_point("process_message")
    graph.set_finish_point("process_message")
    
    return graph.compile()
```

#### Advanced Graph with Conditional Logic
```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

class AdvancedState(TypedDict):
    input: str
    classification: str
    response: str
    confidence: float

def classify_input(state: AdvancedState) -> AdvancedState:
    """Classify the input"""
    input_text = state.get("input", "")
    
    # Simple classification logic
    if "help" in input_text.lower():
        classification = "help"
        confidence = 0.9
    elif "question" in input_text.lower():
        classification = "question"
        confidence = 0.8
    else:
        classification = "general"
        confidence = 0.6
    
    return {
        **state,
        "classification": classification,
        "confidence": confidence
    }

def handle_help(state: AdvancedState) -> AdvancedState:
    """Handle help requests"""
    return {
        **state,
        "response": "I'm here to help! What do you need assistance with?"
    }

def handle_question(state: AdvancedState) -> AdvancedState:
    """Handle questions"""
    return {
        **state,
        "response": "That's a great question! Let me think about that..."
    }

def handle_general(state: AdvancedState) -> AdvancedState:
    """Handle general input"""
    return {
        **state,
        "response": "I understand. How can I assist you further?"
    }

def route_classification(state: AdvancedState) -> str:
    """Route based on classification"""
    classification = state.get("classification", "general")
    return classification

def create_advanced_graph():
    """Create advanced graph with conditional routing"""
    graph = StateGraph(AdvancedState)
    
    # Add nodes
    graph.add_node("classify", classify_input)
    graph.add_node("help", handle_help)
    graph.add_node("question", handle_question)
    graph.add_node("general", handle_general)
    
    # Add edges
    graph.add_edge("classify", "route")
    graph.add_conditional_edges(
        "classify",
        route_classification,
        {
            "help": "help",
            "question": "question",
            "general": "general"
        }
    )
    
    # Set entry point
    graph.set_entry_point("classify")
    
    # Set finish points
    graph.set_finish_point("help")
    graph.set_finish_point("question")
    graph.set_finish_point("general")
    
    return graph.compile()
```

### Graph Registration

#### Method 1: Direct Registration in langgraph.json
```json
{
  "graphs": {
    "simple_graph": "./src/graphs/simple.py:create_simple_graph",
    "advanced_graph": "./src/graphs/advanced.py:create_advanced_graph"
  }
}
```

#### Method 2: Dynamic Registration
```python
# In your graph file
def register_graphs():
    """Register all graphs for Studio"""
    return {
        "simple_graph": create_simple_graph(),
        "advanced_graph": create_advanced_graph()
    }
```

### State Schema Best Practices

#### Use TypedDict for Type Safety
```python
from typing_extensions import TypedDict, NotRequired
from typing import List, Dict, Any, Optional

class ProductionState(TypedDict):
    """Production-ready state schema"""
    # Required fields
    input: str
    output: str
    
    # Optional fields
    metadata: NotRequired[Dict[str, Any]]
    history: NotRequired[List[str]]
    errors: NotRequired[List[str]]
    confidence: NotRequired[float]
```

#### State Validation
```python
def validate_state(state: ProductionState) -> bool:
    """Validate state before processing"""
    if not state.get("input"):
        return False
    
    if state.get("confidence", 0) < 0 or state.get("confidence", 0) > 1:
        return False
    
    return True

def safe_process(state: ProductionState) -> ProductionState:
    """Process with validation"""
    if not validate_state(state):
        return {
            **state,
            "output": "Invalid input",
            "errors": ["State validation failed"]
        }
    
    # Process normally
    return process_message(state)
```

## Studio Interface

### Accessing Studio

#### Local Development
1. Start the development server:
   ```bash
   uv run langgraph dev --port 8000
   ```

2. Open Studio in your browser:
   ```
   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000
   ```

3. Sign in to your LangSmith account

### Studio Interface Components

#### 1. Project Panel
- **Graph Selection**: Choose which graph to work with
- **Project Management**: Switch between different projects
- **Configuration**: View and edit project settings

#### 2. Graph Visualization
- **Node Display**: Visual representation of graph nodes
- **Edge Connections**: Shows data flow between nodes
- **State Flow**: Visualize how state moves through the graph
- **Interactive Editing**: Drag and drop to modify graph structure

#### 3. Input Panel
- **Test Input**: Enter test data for your graph
- **Parameter Configuration**: Set input parameters
- **Batch Testing**: Test multiple inputs at once
- **Input Validation**: Real-time input validation

#### 4. Execution Panel
- **Real-time Execution**: Watch your graph run step-by-step
- **Node Status**: See which nodes are active, completed, or failed
- **Streaming Output**: Real-time output from each node
- **Execution Timeline**: Visual timeline of execution

#### 5. State Inspector
- **Current State**: View the current state of your graph
- **State History**: See how state changes over time
- **Node Inputs/Outputs**: Inspect data at each node
- **State Comparison**: Compare states between different runs

#### 6. Debug Console
- **Error Messages**: View detailed error information
- **Log Output**: Real-time logging from your graph
- **Performance Metrics**: Execution time and resource usage
- **Debug Information**: Detailed debugging information

### Studio Features

#### Visual Graph Editing
```python
# Studio can automatically detect and visualize:
# - Node functions
# - State schemas
# - Edge connections
# - Conditional logic
# - Entry and finish points
```

#### Real-time Testing
```python
# Test your graph with different inputs:
test_inputs = [
    {"message": "Hello, world!"},
    {"message": "Help me please"},
    {"message": "What's the weather?"}
]

# Studio will show:
# - Execution flow
# - State changes
# - Output results
# - Performance metrics
```

#### Interactive Debugging
```python
# Set breakpoints in your code:
def debug_node(state: GraphState) -> GraphState:
    # Studio will pause here for inspection
    breakpoint()  # Interactive debugging
    
    # Continue execution
    return process_state(state)
```

## Development Workflow

### 1. Initial Setup
```bash
# Create new project
uv run langgraph new my-agent-project
cd my-agent-project

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Graph Development
```bash
# Start development server
uv run langgraph dev

# Open Studio interface
open https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000
```

### 3. Visual Development
1. **Create Graph**: Use Studio's visual editor
2. **Test Graph**: Use the input panel to test
3. **Debug Issues**: Use the state inspector
4. **Iterate**: Make changes and test again

### 4. Code Integration
```bash
# Export graph from Studio
# Studio will generate Python code

# Integrate with your project
git add exported_graph.py
git commit -m "Add Studio-exported graph"
```

### 5. Production Deployment
```bash
# Build for production
uv run langgraph build

# Deploy to cloud
uv run langgraph up --host 0.0.0.0 --port 8080
```

### 6. Continuous Integration
```yaml
# .github/workflows/studio.yml
name: Studio Integration
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: uv sync
      - run: uv run langgraph dev --no-browser &
      - run: sleep 10
      - run: curl http://localhost:8000/ok
      - run: uv run pytest
```

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
pkill -f "langgraph dev"

# Try different port
uv run langgraph dev --port 8001
```

#### 2. Graph Not Loading
```bash
# Check graph path in langgraph.json
cat langgraph.json

# Verify graph function exists
uv run python -c "from src.graphs.my_graph import create_graph; print('Graph loaded')"

# Check for import errors
uv run python -c "import src.graphs.my_graph"
```

#### 3. Studio Connection Issues
```bash
# Check server status
curl http://localhost:8000/ok

# Verify Studio URL
echo "https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000"

# Check network connectivity
ping smith.langchain.com
```

#### 4. TypedDict Errors
```python
# Use typing_extensions instead of typing
from typing_extensions import TypedDict  # ✅ Correct
# from typing import TypedDict  # ❌ Wrong for Python < 3.12
```

#### 5. Environment Variable Issues
```bash
# Check .env file
cat .env

# Verify environment loading
uv run python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"

# Test API key
uv run python -c "import google.generativeai as genai; genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))"
```

### Debug Mode

#### Enable Debug Logging
```bash
# Start with debug logging
uv run langgraph dev --server-log-level debug

# Enable remote debugging
uv run langgraph dev --debug-port 5678
```

#### Debug in VS Code
```json
// .vscode/launch.json
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
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

## Best Practices

### 1. Project Organization
```
project/
├── src/
│   ├── graphs/           # Graph implementations
│   ├── nodes/            # Reusable node functions
│   ├── schemas/          # State schemas
│   └── utils/            # Utility functions
├── tests/                # Test files
├── docs/                 # Documentation
├── langgraph.json        # Studio configuration
├── pyproject.toml        # Project configuration
└── .env                  # Environment variables
```

### 2. Graph Design
```python
# Use descriptive names
def process_user_query(state: UserQueryState) -> UserQueryState:
    """Process user query with clear documentation"""
    pass

# Keep nodes focused
def validate_input(state: State) -> State:
    """Single responsibility: validate input"""
    pass

def generate_response(state: State) -> State:
    """Single responsibility: generate response"""
    pass
```

### 3. State Management
```python
# Use immutable state updates
def update_state(state: State, **updates) -> State:
    """Create new state with updates"""
    return {**state, **updates}

# Validate state changes
def safe_update(state: State, **updates) -> State:
    """Update state with validation"""
    new_state = {**state, **updates}
    if validate_state(new_state):
        return new_state
    else:
        raise ValueError("Invalid state update")
```

### 4. Error Handling
```python
def robust_node(state: State) -> State:
    """Node with comprehensive error handling"""
    try:
        result = process_data(state)
        return update_state(state, result=result)
    except ValidationError as e:
        return update_state(state, error=f"Validation error: {e}")
    except ProcessingError as e:
        return update_state(state, error=f"Processing error: {e}")
    except Exception as e:
        return update_state(state, error=f"Unexpected error: {e}")
```

### 5. Testing
```python
# Test individual nodes
def test_process_message():
    state = {"message": "Hello", "response": ""}
    result = process_message(state)
    assert result["response"] == "Processed: Hello"

# Test complete graphs
def test_complete_graph():
    app = create_my_graph()
    result = app.invoke({"message": "Test"})
    assert "response" in result
```

## Advanced Features

### 1. Custom Studio Extensions
```python
# Create custom Studio components
class CustomNodeInspector:
    """Custom node inspector for Studio"""
    
    def inspect_node(self, node_name: str, state: dict) -> dict:
        """Custom inspection logic"""
        return {
            "node": node_name,
            "state": state,
            "metrics": self.calculate_metrics(state)
        }
```

### 2. Multi-Graph Projects
```json
{
  "graphs": {
    "chatbot": "./src/chatbot.py:create_chatbot",
    "analyzer": "./src/analyzer.py:create_analyzer",
    "pipeline": "./src/pipeline.py:create_pipeline"
  }
}
```

### 3. Graph Composition
```python
def create_composite_graph():
    """Create graph from multiple sub-graphs"""
    main_graph = StateGraph(CompositeState)
    
    # Add sub-graphs as nodes
    main_graph.add_node("chatbot", create_chatbot())
    main_graph.add_node("analyzer", create_analyzer())
    
    # Connect sub-graphs
    main_graph.add_edge("chatbot", "analyzer")
    
    return main_graph.compile()
```

### 4. Performance Optimization
```python
# Use async nodes for I/O operations
async def async_node(state: State) -> State:
    """Async node for better performance"""
    result = await async_operation(state["input"])
    return update_state(state, result=result)

# Implement caching
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_operation(input_data: str) -> str:
    """Cached operation for repeated calls"""
    return expensive_operation(input_data)
```

### 5. Monitoring and Observability
```python
import logging
from datetime import datetime

def monitored_node(state: State) -> State:
    """Node with comprehensive monitoring"""
    start_time = datetime.now()
    
    try:
        result = process_data(state)
        
        # Log success
        logging.info(f"Node completed in {datetime.now() - start_time}")
        
        return update_state(state, result=result)
        
    except Exception as e:
        # Log error
        logging.error(f"Node failed: {e}")
        raise
```

## Conclusion

LangGraph Studio provides a powerful, visual development environment for building sophisticated AI agents. By following this guide, you can:

- Set up a complete development environment
- Create and visualize complex agent workflows
- Debug and test agents in real-time
- Deploy production-ready applications
- Collaborate effectively with your team

The combination of visual development, real-time debugging, and seamless code integration makes LangGraph Studio an essential tool for modern AI agent development.

For more information, visit:
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Platform](https://smith.langchain.com)
- [Studio Interface](https://smith.langchain.com/studio)

---

*Last Updated: September 2024*
*Version: 1.0*
