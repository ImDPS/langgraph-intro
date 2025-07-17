"""
Pytest Configuration

This file contains pytest configuration, fixtures, and setup for the test suite.
"""

import pytest
import os
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_environment():
    """Load environment variables for all tests."""
    load_dotenv()


@pytest.fixture(scope="session")
def test_state_schema():
    """Provide a test state schema for tests."""
    from typing import TypedDict
    
    class TestState(TypedDict):
        message: str
        response: str
    
    return TestState


@pytest.fixture(scope="session")
def sample_messages():
    """Provide sample messages for testing."""
    return [
        "",
        "Hello, world!",
        "Help me please",
        "This is a test message",
        "Hello, how are you today?"
    ]


@pytest.fixture(scope="session")
def expected_responses():
    """Provide expected responses for sample messages."""
    return [
        "No message provided.",
        "Hello! I received your message",
        "I'm here to help",
        "I processed your message",
        "Hello! I received your message"
    ]


@pytest.fixture(scope="function")
def clean_environment():
    """Ensure clean environment for each test."""
    # Save original environment
    original_env = dict(os.environ)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env) 