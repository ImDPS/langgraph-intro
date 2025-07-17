# Simple Graph Application - Lesson 2

This directory contains the implementation of Task 3: Lesson 2 - Simple Graph from the LangGraph Introduction course. This lesson demonstrates the fundamental concepts of LangGraph including state management, node functions, graph structure, and compilation.

## 📁 Files

- `simple_graph.py` - Main application with state schema, node function, and graph definition
- `example_usage.py` - Examples demonstrating how to use the application
- `README.md` - This file with usage instructions

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+** - Required for the project
2. **Dependencies** - Install required packages

### Installation

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Verify installation:**
   ```bash
   python -c "import langgraph; print('LangGraph installed successfully!')"
   ```

### Running the Application

#### Option 1: Run Tests
```bash
cd src
python simple_graph.py
```

This will run all tests and verify that the application is working correctly.

#### Option 2: Run Examples
```bash
cd src
python example_usage.py
```

This will demonstrate various ways to use the simple graph application.

#### Option 3: Interactive Usage
```python
from simple_graph import create_simple_graph, GraphState

# Create the application
app = create_simple_graph()

# Define initial state
initial_state: GraphState = {
    "message": "Hello, LangGraph!",
    "response": ""
}

# Process the message
result = app.invoke(initial_state)
print(result["response"])
```

## 🏗️ Architecture

### State Schema
The application uses a simple state schema defined with `TypedDict`:

```python
class GraphState(TypedDict):
    message: str    # Input message from user
    response: str   # Generated response
```

### Node Function
The `process_message` function processes input messages and generates responses:

- **Input**: GraphState with message and empty response
- **Processing**: Simple logic based on message content
- **Output**: Updated GraphState with populated response

### Graph Structure
The graph consists of:
- **Single Node**: `process_message` - handles message processing
- **Entry Point**: `process_message` - where execution starts
- **Finish Point**: `process_message` - where execution ends

### Compilation
The graph is compiled into a runnable LangChain application with:
- `.invoke()` method for single execution
- `.stream()` method for streaming execution
- Standard LangChain Runnable interface

## 🧪 Testing

The application includes comprehensive tests for:

1. **State Schema Tests** - Verify state structure and validation
2. **Node Function Tests** - Test message processing logic
3. **Graph Structure Tests** - Verify graph compilation and basic functionality
4. **Complete Application Tests** - End-to-end workflow testing

Run tests with:
```bash
python simple_graph.py
```

## 📚 Learning Objectives

By completing this lesson, you will understand:

- ✅ How to create a basic StateGraph
- ✅ How to define state schema using TypedDict
- ✅ How to implement node functions
- ✅ How to set entry and finish points
- ✅ How to compile and run LangGraph applications
- ✅ The relationship between state, nodes, and graphs

## 🔧 Key Concepts

### State Management
- State flows through the graph as a dictionary
- Each node receives and returns state updates
- State schema ensures type safety and structure

### Node Functions
- Pure functions that process state
- Must return updated state dictionary
- Can contain any Python logic (LLM calls, API calls, etc.)

### Graph Compilation
- Converts graph definition to runnable application
- Provides standard LangChain interfaces
- Enables streaming and batching capabilities

## 🚀 Next Steps

After completing this lesson, you can:

1. **Proceed to Lesson 3** - LangGraph Studio integration
2. **Experiment with the code** - Try different node functions
3. **Enhance the state** - Add more fields to the state schema
4. **Add more nodes** - Create multi-node graphs

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: `langgraph.graph` not found
   - **Solution**: Install dependencies with `pip install -e .`

2. **Type Errors**: GraphState type issues
   - **Solution**: Ensure you're using proper type annotations

3. **Compilation Errors**: Graph structure issues
   - **Solution**: Verify entry and finish points are set correctly

### Getting Help

- Check the test output for specific error messages
- Verify all dependencies are installed correctly
- Ensure Python version is 3.11 or higher

## 📖 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Course Materials](../plan/modules/introduction/)

---

*Last Updated: 2025-07-17*  
*Course: LangGraph Introduction* 