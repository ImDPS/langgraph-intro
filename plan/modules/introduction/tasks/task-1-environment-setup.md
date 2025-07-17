# Task 1: Environment Setup

## 📋 Overview

Set up a complete LangGraph development environment with all necessary dependencies, tools, and configurations to support **Module 1: Introduction** lessons.

## 🎯 Learning Objectives

- ✅ Install and configure LangGraph with Gemini LLM support
- ✅ Set up development environment for Module 1 lessons
- ✅ Verify installation with basic test
- ✅ Configure project structure for 7 introduction lessons

---

## 📋 Atomic Subtasks

### Subtask 1.1: Install Dependencies
**Duration:** 30 minutes  
**Prerequisites:** None  
**Deliverable:** All dependencies installed and verified

#### Steps:

1. **Install Python 3.8+** if not already installed
2. **Install uv package manager**
3. **Create new project** with `uv init`
4. **Add LangGraph dependencies** with Gemini support:
   ```bash
   uv add langgraph langchain google-generativeai python-dotenv
   ```
5. **Verify installation** with import test

#### Test Criteria:

- [ ] `python -c "import langgraph"` runs without error
- [ ] `python -c "import langchain"` runs without error
- [ ] `python -c "import google.generativeai"` runs without error
- [ ] All dependencies listed in `pyproject.toml`
- [ ] Virtual environment activated

#### Code to Test:

```python
# test_installation.py
import langgraph
import langchain
import google.generativeai as genai
import os

def test_imports():
    """Test that all required packages can be imported successfully"""
    assert langgraph.__version__ is not None
    assert langchain.__version__ is not None
    print("✅ All imports successful")

if __name__ == "__main__":
    test_imports()
```

---

### Subtask 1.2: Configure Environment Variables
**Duration:** 15 minutes  
**Prerequisites:** Subtask 1.1  
**Deliverable:** Environment variables configured

#### Steps:

1. **Create `.env` file** in project root
2. **Add required environment variables**:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```
3. **Create `.env.example`** for documentation
4. **Add `.env` to `.gitignore`**

#### Test Criteria:

- [ ] Environment variables load correctly
- [ ] API keys are valid (test with simple API call)
- [ ] `.env.example` exists and is documented
- [ ] `.env` is in `.gitignore`

#### Code to Test:

```python
# test_env.py
import os
from dotenv import load_dotenv

def test_environment():
    """Test that all required environment variables are configured"""
    load_dotenv()
    
    required_vars = [
        'GOOGLE_API_KEY',
        'LANGCHAIN_TRACING_V2',
        'LANGCHAIN_ENDPOINT',
        'LANGCHAIN_API_KEY'
    ]
    
    for var in required_vars:
        assert os.getenv(var) is not None, f"Missing {var}"
    
    print("✅ Environment variables configured")

if __name__ == "__main__":
    test_environment()
```

---

### Subtask 1.3: Set Up Project Structure
**Duration:** 30 minutes  
**Prerequisites:** Subtask 1.2  
**Deliverable:** Organized project structure for Module 1 lessons

#### Steps:

1. **Create project directory structure** for Module 1 lessons:

```
langgraph-intro/
├── src/
│   ├── __init__.py
│   ├── lessons/
│   │   ├── lesson-1-motivation/
│   │   ├── lesson-2-simple-graph/
│   │   ├── lesson-3-langgraph-studio/
│   │   ├── lesson-4-chain/
│   │   ├── lesson-5-router/
│   │   ├── lesson-6-agent/
│   │   └── lesson-7-agent-memory/
│   ├── graphs/
│   ├── nodes/
│   └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_lessons/
│   ├── test_graphs/
│   └── test_nodes/
├── examples/
├── docs/
└── requirements.txt
```

2. **Create `__init__.py` files** in all directories
3. **Set up basic configuration files**
4. **Create initial `README.md`** with Module 1 overview

#### Test Criteria:

- [ ] All directories exist
- [ ] All `__init__.py` files created
- [ ] Project structure follows Python conventions
- [ ] `README.md` contains basic project information

#### Code to Test:

```python
# test_structure.py
import os

def test_project_structure():
    """Test that the project structure is correctly set up"""
    required_dirs = [
        'src',
        'src/lessons',
        'src/lessons/lesson-1-motivation',
        'src/lessons/lesson-2-simple-graph',
        'src/lessons/lesson-3-langgraph-studio',
        'src/lessons/lesson-4-chain',
        'src/lessons/lesson-5-router',
        'src/lessons/lesson-6-agent',
        'src/lessons/lesson-7-agent-memory',
        'src/graphs',
        'src/nodes',
        'src/utils',
        'tests',
        'tests/test_lessons',
        'tests/test_graphs',
        'tests/test_nodes',
        'examples',
        'docs'
    ]
    
    required_files = [
        'src/__init__.py',
        'src/lessons/__init__.py',
        'tests/__init__.py',
        'README.md',
        'pyproject.toml'
    ]
    
    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"Missing directory: {dir_path}"
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing file: {file_path}"
    
    print("✅ Project structure complete")

if __name__ == "__main__":
    test_project_structure()
```

---

### Subtask 1.4: Configure Development Tools
**Duration:** 30 minutes  
**Prerequisites:** Subtask 1.3  
**Deliverable:** Development tools configured

#### Steps:

1. **Install development dependencies**:
   ```bash
   uv add --dev pytest pytest-cov black isort mypy
   ```
2. **Configure pytest** in `pyproject.toml`
3. **Set up pre-commit hooks** (optional)
4. **Configure IDE settings** (VS Code, PyCharm, etc.)
5. **Create basic test configuration**

#### Test Criteria:

- [ ] pytest runs without error
- [ ] black formats code correctly
- [ ] isort sorts imports correctly
- [ ] mypy runs without critical errors

#### Code to Test:

```python
# test_dev_tools.py
import subprocess
import sys

def test_dev_tools():
    """Test that all development tools are properly configured"""
    # Test pytest
    result = subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, "pytest not working"
    
    # Test black
    result = subprocess.run([sys.executable, "-m", "black", "--version"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, "black not working"
    
    # Test isort
    result = subprocess.run([sys.executable, "-m", "isort", "--version"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, "isort not working"
    
    print("✅ Development tools configured")

if __name__ == "__main__":
    test_dev_tools()
```

---

### Subtask 1.5: Create Basic Test Suite
**Duration:** 45 minutes  
**Prerequisites:** Subtask 1.4  
**Deliverable:** Basic test suite with examples for Module 1 lessons

#### Steps:

1. **Create `tests/test_basic.py`** with basic tests
2. **Create `tests/conftest.py`** for test configuration
3. **Add test for environment setup** with Gemini
4. **Add test for basic LangGraph import**
5. **Create test for simple graph creation**
6. **Create test structure** for Module 1 lessons

#### Test Criteria:

- [ ] All tests pass
- [ ] Test coverage > 80%
- [ ] Tests are well-documented
- [ ] Test suite can be run with pytest

#### Code to Test:

```python
# tests/test_basic.py
import pytest
from langgraph.graph import StateGraph
from typing import TypedDict

class TestState(TypedDict):
    value: int

def test_langgraph_import():
    """Test that LangGraph can be imported and basic functionality works"""
    assert StateGraph is not None
    
    # Test basic graph creation
    graph = StateGraph(TestState)
    assert graph is not None
    assert hasattr(graph, 'add_node')
    assert hasattr(graph, 'add_edge')

def test_environment_setup():
    """Test that environment is properly configured with Gemini"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    assert os.getenv('GOOGLE_API_KEY') is not None

def test_project_structure():
    """Test that project structure is correct for Module 1 lessons"""
    import os
    
    required_files = [
        'src/__init__.py',
        'src/lessons/__init__.py',
        'tests/__init__.py',
        'README.md',
        'pyproject.toml'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing {file_path}"

if __name__ == "__main__":
    pytest.main([__file__])
```

---

## 🧪 Integration Test

**Test Name:** Complete Environment Setup for Module 1  
**Duration:** 15 minutes  
**Prerequisites:** All subtasks completed

### Steps:

1. Run all individual tests
2. Test complete workflow with Gemini
3. Verify all tools work together
4. Test basic LangGraph functionality
5. Verify Module 1 lesson structure is ready

### Test Code:

```python
# integration_test.py
import pytest
from langgraph.graph import StateGraph
from typing import TypedDict
import os
from dotenv import load_dotenv

class TestState(TypedDict):
    message: str
    response: str

def test_complete_setup():
    """Integration test for complete environment setup for Module 1"""
    
    # Test environment
    load_dotenv()
    assert os.getenv('GOOGLE_API_KEY') is not None
    
    # Test LangGraph functionality
    graph = StateGraph(TestState)
    
    def echo_node(state: TestState) -> TestState:
        return {"message": state["message"], "response": f"Echo: {state['message']}"}
    
    graph.add_node("echo", echo_node)
    graph.set_entry_point("echo")
    graph.set_finish_point("echo")
    
    app = graph.compile()
    
    # Test execution
    result = app.invoke({"message": "Hello, LangGraph!"})
    assert result["response"] == "Echo: Hello, LangGraph!"
    
    # Test Module 1 lesson structure
    import os
    lesson_dirs = [
        'src/lessons/lesson-1-motivation',
        'src/lessons/lesson-2-simple-graph',
        'src/lessons/lesson-3-langgraph-studio',
        'src/lessons/lesson-4-chain',
        'src/lessons/lesson-5-router',
        'src/lessons/lesson-6-agent',
        'src/lessons/lesson-7-agent-memory'
    ]
    for lesson_dir in lesson_dirs:
        assert os.path.exists(lesson_dir), f"Missing lesson directory: {lesson_dir}"
    
    print("✅ Complete environment setup for Module 1 successful")

if __name__ == "__main__":
    test_complete_setup()
```

---

## 📊 Success Criteria

- [ ] All subtasks completed
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Project structure created
- [ ] Development tools working
- [ ] Basic test suite functional
- [ ] Integration test passes

---

## 🚀 Next Steps

After completing this task, you can proceed to:

- **Task 2:** Lesson 1 - Motivation
- **Alternative:** Review LangGraph documentation
- **Optional:** Set up additional development tools

---

## 📝 Notes

- 🔐 Keep your API keys secure
- 📚 Document any environment-specific setup
- 🌍 Consider using different environments for development/testing/production
- 💾 Regular backups of your configuration
- 🤖 This setup uses Gemini as the primary LLM for all Module 1 lessons
- 📖 Each lesson builds upon the previous one, so complete them in order

---

**Last Updated:** 2025-07-17  
**Task Lead:** LangGraph Team