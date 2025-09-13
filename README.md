# LangGraph Introduction Course

A comprehensive introduction to LangGraph, teaching you how to build AI applications with stateful workflows, agents, and complex reasoning patterns through hands-on, task-based learning.

## 🎯 Course Overview

This course covers the fundamentals of LangGraph through 8 progressive tasks:

1. **Task 1: Environment Setup** - Set up your LangGraph development environment
2. **Task 2: Lesson 1 - Motivation** - Understanding why LangGraph matters
3. **Task 3: Lesson 2 - Simple Graph** - Building your first LangGraph application
4. **Task 4: Lesson 3 - LangGraph Studio** - Visualizing and debugging graphs
5. **Task 5: Lesson 4 - Chain** - Creating sequential workflows with LangChain
6. **Task 6: Lesson 5 - Router** - Building conditional logic flows
7. **Task 7: Lesson 6 - Agent** - Implementing autonomous agents
8. **Task 8: Lesson 7 - Agent Memory** - Adding persistence to agents

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key
- LangChain API key (optional, for tracing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd langgraph-intro
   ```

2. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

5. **Verify installation:**
   ```bash
   uv run python -c "import langgraph; print('✅ LangGraph installed successfully!')"
   ```

6. **Start LangGraph Studio (Optional):**
   ```bash
   # Start the local development server
   uv run langgraph dev --port 8000 --no-browser --config langgraph.json
   
   # Open LangGraph Studio in your browser
   # https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000
   ```

## 📚 Learning Path

### Task-Based Approach

Each task is designed to be:
- **Atomic**: Complete and testable on its own
- **Progressive**: Builds upon previous tasks
- **Hands-on**: Includes working code examples
- **Tested**: Comprehensive test coverage

### Getting Started

1. **Begin with Task 1**: Environment Setup
   ```bash
   # Follow the instructions in:
   plan/modules/introduction/tasks/task-1-environment-setup.md
   ```

2. **Progress through tasks sequentially**:
   - Each task includes detailed instructions
   - Complete all tests before moving to the next
   - Review the knowledge base for additional context

3. **Access task materials**:
   ```bash
   # Task instructions
   plan/modules/introduction/tasks/
   
   # Implementation code
   src/modules/introduction/lessons/
   
   # Knowledge base
   knowledge-base/
   ```

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_basic.py

# Run tests for a specific lesson
uv run pytest src/modules/introduction/lessons/lesson_2_simple_graph/
```

## 🏗️ Project Structure

```
langgraph-intro/
├── src/
│   ├── modules/              # Course modules
│   │   ├── introduction/     # Module 1: Introduction
│   │   │   ├── lessons/      # Lesson implementations
│   │   │   ├── graphs/       # Reusable graph patterns
│   │   │   └── nodes/        # Reusable node functions
│   │   ├── state-memory/     # Module 2: State & Memory
│   │   ├── long-term-memory/ # Module 3: Long-term Memory
│   │   ├── building-assistant/ # Module 4: Building Assistant
│   │   ├── ux-human-loop/    # Module 5: UX & Human-in-the-loop
│   │   └── deployment/       # Module 6: Deployment
│   └── utils/                # Shared utilities
├── tests/                    # Test suite
├── plan/                     # Course planning and task definitions
│   └── modules/
│       └── introduction/
│           └── tasks/        # Detailed task instructions
├── knowledge-base/           # Documentation and resources
│   ├── concepts/             # Core concepts
│   ├── examples/             # Code examples
│   ├── reference/            # API reference
│   └── use-cases/            # Real-world applications
├── pyproject.toml           # Project configuration (uv)
├── uv.lock                  # Dependency lock file
└── env.example              # Environment variables template
```

## 🔧 Development

### Using uv

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Run commands in the virtual environment
uv run python script.py
uv run pytest
uv run black src/
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Type checking
uv run mypy src/

# Run all quality checks
uv run black src/ tests/ && uv run isort src/ tests/ && uv run mypy src/
```

### LangGraph Studio

Visual development and debugging for your graphs:

```bash
# Start the development server
uv run langgraph dev --port 8000 --no-browser --config langgraph.json

# Access Studio interface
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000
```

**Available Graphs:**
- `simple_graph` - Basic LangGraph example
- `basic_chain_graph` - Simple LLM integration
- `tool_calling_graph` - Function calling capabilities
- `multi_chain_workflow` - Complex analysis pipeline

### Environment Variables

Required environment variables (see `env.example`):

- `GOOGLE_API_KEY` - Your Google Gemini API key
- `LANGCHAIN_TRACING_V2` - Enable LangChain tracing (optional)
- `LANGCHAIN_ENDPOINT` - LangChain API endpoint (optional)
- `LANGCHAIN_API_KEY` - Your LangChain API key (optional)

## 📖 Documentation

### Course Materials
- [Task Instructions](plan/modules/introduction/tasks/)
- [Module Overview](plan/modules/introduction/README.md)
- [Knowledge Base](knowledge-base/)

### External Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [uv Documentation](https://docs.astral.sh/uv/)

## 🎓 Learning Modules

### Module 1: Introduction (Current)
- **Duration**: 8 days
- **Focus**: Core LangGraph concepts and basic applications
- **Status**: In Progress

### Upcoming Modules
- **Module 2**: State and Memory Management
- **Module 3**: Long-term Memory Systems
- **Module 4**: Building Intelligent Assistants
- **Module 5**: UX and Human-in-the-loop
- **Module 6**: Deployment and Production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Last Updated: 2025-01-27*  
*Course: LangGraph Introduction*  
*Package Manager: uv*
