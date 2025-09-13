"""
Example Usage for Lesson 4: Chain Integration with LangChain

This module provides practical examples of how to use the chain integration functionality.
"""

import os
from langchain_core.messages import HumanMessage, AIMessage

from .chain_integration import (
    create_basic_chain_graph,
    create_tool_calling_graph,
    create_multi_chain_workflow,
    ChainIntegration
)


def example_basic_chain():
    """Example of using basic chain integration."""
    print("=" * 60)
    print("Example 1: Basic Chain Integration")
    print("=" * 60)
    
    try:
        # Create basic chain graph
        graph = create_basic_chain_graph()
        
        # Test with different types of messages
        test_messages = [
            "Hello! What can you help me with?",
            "Tell me about artificial intelligence",
            "What are the benefits of using LangGraph?",
            "How do I get started with AI development?"
        ]
        
        for message in test_messages:
            print(f"\nUser: {message}")
            
            result = graph.invoke({
                "messages": [HumanMessage(content=message)]
            })
            
            response = result["messages"][-1].content
            print(f"Assistant: {response[:200]}{'...' if len(response) > 200 else ''}")
            
    except Exception as e:
        print(f"Error in basic chain example: {e}")


def example_tool_calling():
    """Example of using tool calling functionality."""
    print("\n" + "=" * 60)
    print("Example 2: Tool Calling Integration")
    print("=" * 60)
    
    try:
        # Create tool calling graph
        graph = create_tool_calling_graph()
        
        # Test with mathematical operations
        test_messages = [
            "What is 23 multiplied by 45?",
            "Add 15 and 27 together",
            "Calculate 100 times 50",
            "What's the sum of 12 and 8?"
        ]
        
        for message in test_messages:
            print(f"\nUser: {message}")
            
            result = graph.invoke({
                "messages": [HumanMessage(content=message)]
            })
            
            # Print all messages in the result
            for i, msg in enumerate(result["messages"]):
                if isinstance(msg, AIMessage):
                    print(f"Assistant: {msg.content}")
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        print(f"  Tool calls: {msg.tool_calls}")
            
    except Exception as e:
        print(f"Error in tool calling example: {e}")


def example_multi_chain_workflow():
    """Example of using multi-chain workflow."""
    print("\n" + "=" * 60)
    print("Example 3: Multi-Chain Workflow")
    print("=" * 60)
    
    try:
        # Create multi-chain workflow
        graph = create_multi_chain_workflow()
        
        # Test with complex requests
        test_messages = [
            "I need help with project management strategies for a software development team",
            "How can I improve my team's productivity and collaboration?",
            "What are the best practices for managing remote teams?"
        ]
        
        for message in test_messages:
            print(f"\nUser: {message}")
            
            result = graph.invoke({
                "messages": [HumanMessage(content=message)]
            })
            
            # Print the workflow results
            print("\nWorkflow Results:")
            for i, msg in enumerate(result["messages"]):
                if isinstance(msg, AIMessage):
                    if i == 1:  # Analysis
                        print(f"📊 Analysis: {msg.content[:150]}...")
                    elif i == 2:  # Recommendations
                        print(f"💡 Recommendations: {msg.content[:150]}...")
                    elif i == 3:  # Summary
                        print(f"📝 Summary: {msg.content[:150]}...")
            
    except Exception as e:
        print(f"Error in multi-chain workflow example: {e}")


def example_custom_chain_integration():
    """Example of creating custom chain integration."""
    print("\n" + "=" * 60)
    print("Example 4: Custom Chain Integration")
    print("=" * 60)
    
    try:
        # Create custom integration
        integration = ChainIntegration(model_name="gemini-2.0-flash-lite")
        
        # Create a custom graph with specific configuration
        graph = integration.create_basic_chain_graph()
        
        # Test with custom messages
        custom_messages = [
            "Create a project plan for building a web application",
            "Design a database schema for an e-commerce platform",
            "Write a technical specification for a mobile app"
        ]
        
        for message in custom_messages:
            print(f"\nUser: {message}")
            
            result = graph.invoke({
                "messages": [HumanMessage(content=message)]
            })
            
            response = result["messages"][-1].content
            print(f"Assistant: {response[:200]}...")
            
    except Exception as e:
        print(f"Error in custom chain integration example: {e}")


def example_error_handling():
    """Example of error handling in chain integration."""
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    try:
        # Test with invalid API key
        original_key = os.environ.get("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = "invalid_key"
        
        try:
            graph = create_basic_chain_graph()
            result = graph.invoke({
                "messages": [HumanMessage(content="Test message")]
            })
            print("Unexpected: Graph should have failed with invalid API key")
        except Exception as e:
            print(f"Expected error with invalid API key: {e}")
        
        # Restore original key
        if original_key:
            os.environ["GOOGLE_API_KEY"] = original_key
        else:
            del os.environ["GOOGLE_API_KEY"]
            
    except Exception as e:
        print(f"Error in error handling example: {e}")


def example_conversation_flow():
    """Example of conversation flow with multiple interactions."""
    print("\n" + "=" * 60)
    print("Example 6: Conversation Flow")
    print("=" * 60)
    
    try:
        # Create basic chain graph
        graph = create_basic_chain_graph()
        
        # Simulate a conversation
        conversation = [
            "Hello! I'm new to AI development.",
            "What programming languages should I learn?",
            "How do I get started with machine learning?",
            "What are some good resources for beginners?"
        ]
        
        # Keep track of conversation history
        messages = []
        
        for user_message in conversation:
            print(f"\nUser: {user_message}")
            
            # Add user message to conversation
            messages.append(HumanMessage(content=user_message))
            
            # Get response from graph
            result = graph.invoke({"messages": messages})
            
            # Add assistant response to conversation
            assistant_response = result["messages"][-1]
            messages.append(assistant_response)
            
            print(f"Assistant: {assistant_response.content[:200]}...")
            
    except Exception as e:
        print(f"Error in conversation flow example: {e}")


def run_all_examples():
    """Run all examples."""
    print("Lesson 4: Chain Integration with LangChain - Examples")
    print("=" * 80)
    
    # Check if API key is available
    if not os.environ.get("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables")
        print("   Some examples may not work properly")
        print("   Set your API key: export GOOGLE_API_KEY='your_api_key_here'")
        print()
    
    # Run examples
    example_basic_chain()
    example_tool_calling()
    example_multi_chain_workflow()
    example_custom_chain_integration()
    example_error_handling()
    example_conversation_flow()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_examples()
