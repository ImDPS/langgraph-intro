"""
Example Usage - Simple Graph Application

This file demonstrates how to import and use the simple graph application
created in simple_graph.py. It shows various ways to interact with the
compiled graph application.
"""

from simple_graph import create_simple_graph, GraphState


def basic_usage_example():
    """
    Demonstrate basic usage of the simple graph application.
    """
    print("🚀 Basic Usage Example")
    print("=" * 40)
    
    # Create the application
    app = create_simple_graph()
    
    # Define initial state
    initial_state: GraphState = {
        "message": "Hello, LangGraph!",
        "response": ""
    }
    
    print(f"📤 Input: {initial_state['message']}")
    
    # Invoke the application
    result = app.invoke(initial_state)
    
    print(f"📥 Output: {result['response']}")
    print()


def multiple_messages_example():
    """
    Demonstrate processing multiple messages with the same application.
    """
    print("🔄 Multiple Messages Example")
    print("=" * 40)
    
    # Create the application once
    app = create_simple_graph()
    
    # Process different types of messages
    messages = [
        "Hello there!",
        "Help me with something",
        "This is a regular message",
        "",  # Empty message
        "Hello, how are you today?"
    ]
    
    for i, message in enumerate(messages, 1):
        initial_state: GraphState = {
            "message": message,
            "response": ""
        }
        
        result = app.invoke(initial_state)
        
        print(f"Message {i}: '{message}'")
        print(f"Response: {result['response']}")
        print()


def streaming_example():
    """
    Demonstrate streaming functionality of the graph application.
    """
    print("🌊 Streaming Example")
    print("=" * 40)
    
    # Create the application
    app = create_simple_graph()
    
    # Define initial state
    initial_state: GraphState = {
        "message": "Hello, streaming world!",
        "response": ""
    }
    
    print(f"📤 Input: {initial_state['message']}")
    print("📥 Streaming response:")
    
    # Use streaming (though our simple graph doesn't have multiple steps)
    for chunk in app.stream(initial_state):
        # In our simple case, we'll get one chunk with the final result
        if "process_message" in chunk:
            response = chunk["process_message"]["response"]
            print(f"  → {response}")
    
    print()


def error_handling_example():
    """
    Demonstrate error handling with the graph application.
    """
    print("⚠️  Error Handling Example")
    print("=" * 40)
    
    # Create the application
    app = create_simple_graph()
    
    # Test with various edge cases
    test_cases = [
        {"message": None, "response": ""},  # Invalid type
        {"message": 123, "response": ""},   # Invalid type
        {"message": "Valid message"},       # Missing response field
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test case {i}: {test_case}")
        try:
            result = app.invoke(test_case)
            print(f"  ✅ Success: {result['response']}")
        except Exception as e:
            print(f"  ❌ Error: {type(e).__name__}: {e}")
        print()


def main():
    """
    Run all example demonstrations.
    """
    print("🎯 Simple Graph Application - Example Usage")
    print("=" * 60)
    print()
    
    # Run all examples
    basic_usage_example()
    multiple_messages_example()
    streaming_example()
    error_handling_example()
    
    print("🎉 All examples completed!")
    print("\n💡 Tips:")
    print("- The application is stateless between invocations")
    print("- You can reuse the same app instance for multiple messages")
    print("- The graph compiles once and can be used many times")
    print("- Error handling is important for production use")


if __name__ == "__main__":
    main() 