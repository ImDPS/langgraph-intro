"""
Basic Test Suite for LangGraph Introduction Course

This module contains basic tests for environment setup, imports, and core functionality.
"""

import pytest
import os
from typing import TypedDict
from dotenv import load_dotenv


class TestState(TypedDict):
    """Test state for basic functionality tests."""
    message: str
    response: str


def test_environment_setup():
    """Test that environment is properly configured with required variables."""
    load_dotenv()
    
    # Check for required environment variables
    required_vars = [
        'GOOGLE_API_KEY',
        'LANGCHAIN_TRACING_V2',
        'LANGCHAIN_ENDPOINT',
        'LANGCHAIN_API_KEY'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        assert value is not None, f"Missing environment variable: {var}"
        if var == 'GOOGLE_API_KEY':
            assert value != 'your_gemini_api_key_here', f"Please set actual value for {var}"


def test_langgraph_import():
    """Test that LangGraph can be imported and basic functionality works."""
    try:
        from langgraph.graph import StateGraph
        assert StateGraph is not None
        
        # Test basic graph creation
        graph = StateGraph(TestState)
        assert graph is not None
        assert hasattr(graph, 'add_node')
        assert hasattr(graph, 'add_edge')
        assert hasattr(graph, 'set_entry_point')
        assert hasattr(graph, 'set_finish_point')
        assert hasattr(graph, 'compile')
        
    except ImportError as e:
        pytest.fail(f"Failed to import LangGraph: {e}")


def test_langchain_import():
    """Test that LangChain can be imported."""
    try:
        import langchain
        assert langchain.__version__ is not None
    except ImportError as e:
        pytest.fail(f"Failed to import LangChain: {e}")


def test_google_generativeai_import():
    """Test that Google Generative AI can be imported."""
    try:
        import google.generativeai as genai
        assert genai is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Google Generative AI: {e}")


def test_project_structure():
    """Test that project structure is correct for Module 1 lessons."""
    required_files = [
        'src/__init__.py',
        'src/lessons/__init__.py',
        'src/graphs/__init__.py',
        'src/nodes/__init__.py',
        'src/utils/__init__.py',
        'tests/__init__.py',
        'README.md',
        'pyproject.toml',
        'env.example'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing required file: {file_path}"


def test_simple_graph_creation():
    """Test creating a simple graph with basic functionality."""
    from langgraph.graph import StateGraph
    
    # Create graph
    graph = StateGraph(TestState)
    
    # Define a simple node function
    def echo_node(state: TestState) -> TestState:
        return {
            "message": state["message"],
            "response": f"Echo: {state['message']}"
        }
    
    # Add node to graph
    graph.add_node("echo", echo_node)
    graph.set_entry_point("echo")
    graph.set_finish_point("echo")
    
    # Compile graph
    app = graph.compile()
    
    # Test execution
    initial_state: TestState = {
        "message": "Hello, LangGraph!",
        "response": ""
    }
    
    result = app.invoke(initial_state)
    
    assert result["message"] == "Hello, LangGraph!"
    assert result["response"] == "Echo: Hello, LangGraph!"


if __name__ == "__main__":
    pytest.main([__file__]) 