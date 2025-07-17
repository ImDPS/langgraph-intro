# LangGraph Introduction Course

A comprehensive introduction to LangGraph, teaching you how to build AI applications with stateful workflows, agents, and complex reasoning patterns.

## 🎯 Course Overview

This course covers the fundamentals of LangGraph through 7 hands-on lessons:

1. **Lesson 1: Motivation** - Understanding why LangGraph matters
2. **Lesson 2: Simple Graph** - Building your first LangGraph application
3. **Lesson 3: LangGraph Studio** - Visualizing and debugging graphs
4. **Lesson 4: Chain** - Creating sequential workflows
5. **Lesson 5: Router** - Building conditional logic flows
6. **Lesson 6: Agent** - Implementing autonomous agents
7. **Lesson 7: Agent Memory** - Adding persistence to agents

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API key
- LangChain API key (optional, for tracing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd langgraph-intro
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

4. **Verify installation:**
   ```bash
   python -c "import langgraph; print('✅ LangGraph installed successfully!')"
   ```

## 📚 Lessons

### Lesson 2: Simple Graph

Start with the simple graph implementation:

```bash
cd src
python simple_graph.py  # Run tests
python example_usage.py  # See examples
```

**Key Concepts:**
- State management with TypedDict
- Node functions
- Graph compilation
- Basic application workflow

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_basic.py
```

## 🏗️ Project Structure

```
langgraph-intro/
├── src/
│   ├── lessons/           # Lesson implementations
│   ├── graphs/           # Reusable graph patterns
│   ├── nodes/            # Reusable node functions
│   ├── utils/            # Utility functions
│   └── simple_graph.py   # Lesson 2 implementation
├── tests/                # Test suite
├── plan/                 # Course planning materials
├── knowledge-base/       # Documentation and resources
└── docs/                 # Additional documentation
```

## 🔧 Development

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && isort src/ tests/ && mypy src/
```

### Environment Variables

Required environment variables (see `env.example`):

- `GOOGLE_API_KEY` - Your Google Gemini API key
- `LANGCHAIN_TRACING_V2` - Enable LangChain tracing
- `LANGCHAIN_ENDPOINT` - LangChain API endpoint
- `LANGCHAIN_API_KEY` - Your LangChain API key

## 📖 Documentation

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Course Materials](plan/modules/introduction/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Last Updated: 2025-07-17*  
*Course: LangGraph Introduction*
