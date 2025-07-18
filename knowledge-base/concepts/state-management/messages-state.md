# MessagesState

## Overview

`MessagesState` is a built-in state class in LangGraph specifically designed for conversational AI applications. It provides a standardized way to manage message-based state with proper type safety and built-in support for message accumulation.

## What is MessagesState?

`MessagesState` is a pre-built state class that automatically handles the common pattern of managing conversation history as a list of messages. It's designed to work seamlessly with LangChain's message types and LangGraph's state management system.

## Import and Usage

```python
from langgraph.graph import MessagesState

# Use MessagesState in your graph
workflow = StateGraph(MessagesState)
```

## Key Features

### 1. Automatic Message Management

`MessagesState` automatically handles:
- Message type validation
- State structure consistency
- Integration with LangChain message types

### 2. Built-in Type Safety

The state is properly typed for TypeScript-like development experience:

```python
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

# MessagesState is essentially this:
class MessagesState(TypedDict):
    messages: List[BaseMessage]
```

### 3. Seamless Integration

Works out of the box with:
- LangChain message types (HumanMessage, AIMessage, etc.)
- Built-in reducers (add_messages)
- Chat models
- Tool integration

## Basic Usage

### Creating a Graph with MessagesState

```python
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# Define your graph
workflow = StateGraph(MessagesState)

# Add nodes that work with messages
def chat_node(state: MessagesState):
    # Access messages
    messages = state["messages"]
    
    # Process and return new message
    response = "Hello! I received your message."
    return {"messages": [AIMessage(content=response)]}

workflow.add_node("chat", chat_node)
```

### Using with Built-in Reducers

```python
from langgraph.graph import add_messages

# Add reducer for proper message accumulation
workflow.add_node("chat", chat_node, reducer=add_messages)
```

## State Structure

### Default State

When you create a graph with `MessagesState`, the initial state structure is:

```python
{
    "messages": []
}
```

### State After Messages

After adding messages, the state becomes:

```python
{
    "messages": [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there!"),
        HumanMessage(content="How are you?"),
        AIMessage(content="I'm doing well, thanks!")
    ]
}
```

## Working with Messages

### Accessing Messages

```python
def process_messages(state: MessagesState):
    messages = state["messages"]
    
    # Get the last message
    last_message = messages[-1] if messages else None
    
    # Get all human messages
    human_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    
    # Get conversation length
    conversation_length = len(messages)
    
    return {"messages": [AIMessage(content=f"Processed {conversation_length} messages")]}
```

### Adding New Messages

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def add_system_message(state: MessagesState):
    system_msg = SystemMessage(content="You are a helpful assistant.")
    return {"messages": [system_msg]}

def respond_to_user(state: MessagesState):
    # Get the last user message
    last_message = state["messages"][-1]
    
    # Generate response
    response = f"I received: {last_message.content}"
    return {"messages": [AIMessage(content=response)]}
```

## Integration Examples

### With Chat Models

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

def llm_node(state: MessagesState):
    # Pass all messages to the LLM
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### With Tools

```python
from langchain_core.messages import ToolMessage

def tool_node(state: MessagesState):
    # Execute tool and add result
    tool_result = ToolMessage(
        content="Tool executed successfully",
        tool_call_id="call_123"
    )
    return {"messages": [tool_result]}
```

### With Conditional Logic

```python
def smart_responder(state: MessagesState):
    messages = state["messages"]
    
    if len(messages) == 0:
        return {"messages": [AIMessage(content="Hello! How can I help you?")]}
    
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        # Respond to user
        response = f"I understand you said: {last_message.content}"
        return {"messages": [AIMessage(content=response)]}
    
    # No response needed for non-human messages
    return {"messages": []}
```

## Advanced Patterns

### Message History Management

```python
def manage_history(state: MessagesState, max_messages=10):
    messages = state["messages"]
    
    if len(messages) > max_messages:
        # Keep system messages and recent conversation
        system_messages = [msg for msg in messages if isinstance(msg, SystemMessage)]
        recent_messages = messages[-max_messages:]
        
        return {"messages": system_messages + recent_messages}
    
    return state
```

### Conversation Summarization

```python
def summarize_conversation(state: MessagesState):
    messages = state["messages"]
    
    if len(messages) > 5:
        # Create summary of conversation
        summary = "This conversation has been going on for a while..."
        summary_msg = AIMessage(content=summary)
        
        return {"messages": [summary_msg]}
    
    return {"messages": []}
```

### Multi-Modal Messages

```python
from langchain_core.messages import HumanMessage, AIMessage

def handle_multimodal(state: MessagesState):
    messages = state["messages"]
    
    # Check for messages with images
    for message in messages:
        if hasattr(message, 'content') and isinstance(message.content, list):
            # Handle multi-modal content
            for content_item in message.content:
                if content_item.get('type') == 'image_url':
                    # Process image
                    pass
    
    return {"messages": [AIMessage(content="Processed multi-modal content")]}
```

## Best Practices

### 1. Use MessagesState for Chat Applications

```python
# ✅ Good: Use MessagesState for conversations
workflow = StateGraph(MessagesState)

# ❌ Avoid: Custom state for simple message handling
class CustomState(TypedDict):
    messages: List[BaseMessage]
```

### 2. Leverage Built-in Reducers

```python
# ✅ Good: Use add_messages reducer
workflow.add_node("chat", chat_node, reducer=add_messages)

# ❌ Avoid: Manual message accumulation
def manual_node(state):
    return {"messages": state["messages"] + [new_message]}
```

### 3. Handle Message Types Properly

```python
# ✅ Good: Check message types
def good_node(state: MessagesState):
    messages = state["messages"]
    human_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    
    if human_messages:
        last_human = human_messages[-1]
        # Process human message
        pass

# ❌ Avoid: Assuming message types
def bad_node(state: MessagesState):
    last_message = state["messages"][-1]  # Could be any message type
    # Process without checking type
```

### 4. Consider Performance for Long Conversations

```python
def efficient_node(state: MessagesState):
    messages = state["messages"]
    
    # Only process recent messages for efficiency
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    
    # Process recent messages
    return {"messages": [AIMessage(content="Processed recent messages")]}
```

## Troubleshooting

### Common Issues

1. **Type Errors**: Ensure you're using proper LangChain message types
2. **State Override**: Use reducers to properly accumulate messages
3. **Empty Messages**: Always check if messages list is empty before accessing

### Debugging Tips

```python
def debug_messages(state: MessagesState):
    messages = state["messages"]
    
    print(f"Total messages: {len(messages)}")
    for i, msg in enumerate(messages):
        print(f"Message {i}: {type(msg).__name__} - {msg.content[:50]}...")
    
    return state
```

## Related Concepts

- [Using Messages as State](./using-messages-as-state.md) - How to use messages as state
- [Reducers](./reducers.md) - Understanding state update patterns
- [State Management Overview](./README.md) - General state management concepts
- [Chat Models](../fundamentals/chat-models.md) - Working with conversational models 