"""
Integration Test for Complete Environment Setup

This module contains integration tests that verify the complete environment
setup for Module 1 lessons is working correctly.
"""

import pytest
import os
from typing import TypedDict
from dotenv import load_dotenv


class TestState(TypedDict):
    """Test state for integration tests."""
    message: str
    response: str


def test_complete_setup():
    """Integration test for complete environment setup for Module 1."""
    
    # Test environment variables
    load_dotenv()
    assert os.getenv('GOOGLE_API_KEY') is not None
    assert os.getenv('LANGCHAIN_TRACING_V2') is not None
    assert os.getenv('LANGCHAIN_ENDPOINT') is not None
    assert os.getenv('LANGCHAIN_API_KEY') is not None
    
    # Test LangGraph functionality
    from langgraph.graph import StateGraph
    
    graph = StateGraph(TestState)
    
    def echo_node(state: TestState) -> TestState:
        return {
            "message": state["message"], 
            "response": f"Echo: {state['message']}"
        }
    
    graph.add_node("echo", echo_node)
    graph.set_entry_point("echo")
    graph.set_finish_point("echo")
    
    app = graph.compile()
    
    # Test execution
    result = app.invoke({"message": "Hello, LangGraph!"})
    assert result["response"] == "Echo: Hello, LangGraph!"
    
    # Test Module 1 lesson structure
    lesson_dirs = [
        'src/modules/introduction/lessons/lesson-1-motivation',
        'src/modules/introduction/lessons/lesson_2_simple_graph',
        'src/modules/introduction/lessons/lesson-3-langgraph-studio',
        'src/modules/introduction/lessons/lesson-4-chain',
        'src/modules/introduction/lessons/lesson-5-router',
        'src/modules/introduction/lessons/lesson-6-agent',
        'src/modules/introduction/lessons/lesson-7-agent-memory'
    ]
    
    for lesson_dir in lesson_dirs:
        assert os.path.exists(lesson_dir), f"Missing lesson directory: {lesson_dir}"
    
    print("✅ Complete environment setup for Module 1 successful")


def test_simple_graph_application():
    """Test the simple graph application from Lesson 2."""
    from src.modules.introduction.lessons.lesson_2_simple_graph.simple_graph import create_simple_graph, GraphState
    
    # Create the application
    app = create_simple_graph()
    
    # Test basic functionality
    initial_state: GraphState = {
        "message": "Hello, integration test!",
        "response": ""
    }
    
    result = app.invoke(initial_state)
    
    assert "message" in result
    assert "response" in result
    assert result["message"] == "Hello, integration test!"
    assert len(result["response"]) > 0
    
    # Test different message types
    test_cases = [
        ("", "No message provided"),
        ("Hello there!", "Hello! I received your message"),
        ("Help me", "I'm here to help"),
        ("Random message", "I processed your message")
    ]
    
    for message, expected_contains in test_cases:
        test_state: GraphState = {"message": message, "response": ""}
        result = app.invoke(test_state)
        assert expected_contains in result["response"], \
            f"Expected '{expected_contains}' in response for message '{message}'"
    
    print("✅ Simple graph application integration test passed")


if __name__ == "__main__":
    test_complete_setup()
    test_simple_graph_application() 