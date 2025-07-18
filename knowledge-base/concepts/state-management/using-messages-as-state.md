# Using Messages as State

## Overview

Using messages as state is a fundamental pattern in LangGraph for building conversational AI applications. This approach allows you to maintain conversation history and context throughout the execution of your graph.

## Key Concepts

### 1. Chat Messages as State

In conversational applications, the primary state is often the conversation history - a list of messages exchanged between the user and the system. LangGraph provides built-in support for this pattern.

### 2. State Structure

A typical state structure using messages might look like:

```python
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class ConversationState(TypedDict):
    messages: List[BaseMessage]
    # Other state fields as needed
```

### 3. Built-in MessagesState

LangGraph provides a pre-built state class specifically for message-based conversations:

```python
from langgraph.graph import MessagesState
```

This `MessagesState` class automatically handles:
- Message accumulation
- Proper state updates
- Type safety for message handling

## Implementation Patterns

### Basic Message State Usage

```python
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# Define your graph with MessagesState
workflow = StateGraph(MessagesState)

# Add nodes that work with messages
def chat_node(state: MessagesState):
    # Access current messages
    messages = state["messages"]
    
    # Process and generate response
    response = "Hello! I received your message."
    
    # Return new message to append
    return {"messages": [AIMessage(content=response)]}

workflow.add_node("chat", chat_node)
```

### State Updates and Reducers

When working with messages, you need to handle state updates properly. Each node can override the previous state, so you need to append new messages rather than replace them.

#### The Problem

```python
# ❌ This would override previous messages
def bad_node(state):
    return {"messages": [new_message]}  # Loses previous messages
```

#### The Solution with Reducers

```python
# ✅ Using a reducer to append messages
def good_node(state):
    return {"messages": state["messages"] + [new_message]}
```

## Best Practices

### 1. Use MessagesState for Chat Applications

For most conversational applications, use the built-in `MessagesState`:

```python
from langgraph.graph import MessagesState

workflow = StateGraph(MessagesState)
```

### 2. Implement Proper Reducers

Always use reducers or append operations when updating message state:

```python
def append_message(state, new_message):
    return {"messages": state["messages"] + [new_message]}
```

### 3. Handle Message Types Properly

Use appropriate message types for different roles:

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# User input
human_msg = HumanMessage(content="Hello")

# AI response
ai_msg = AIMessage(content="Hi there!")

# System instructions
system_msg = SystemMessage(content="You are a helpful assistant.")
```

### 4. Consider Message History Length

For long conversations, consider implementing message history management:

```python
def limit_history(state, max_messages=10):
    messages = state["messages"]
    if len(messages) > max_messages:
        # Keep system messages and recent conversation
        system_messages = [msg for msg in messages if isinstance(msg, SystemMessage)]
        recent_messages = messages[-max_messages:]
        return {"messages": system_messages + recent_messages}
    return state
```

## Common Use Cases

### 1. Simple Chat Bot

```python
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

def chat_bot(state: MessagesState):
    # Get the last user message
    last_message = state["messages"][-1]
    
    # Generate response (simplified)
    response = f"I received: {last_message.content}"
    
    return {"messages": [AIMessage(content=response)]}

# Build graph
workflow = StateGraph(MessagesState)
workflow.add_node("chat", chat_bot)
workflow.set_entry_point("chat")
workflow.set_finish_point("chat")

app = workflow.compile()
```

### 2. Multi-Turn Conversations

```python
def conversation_manager(state: MessagesState):
    messages = state["messages"]
    
    # Analyze conversation context
    if len(messages) > 5:
        # Long conversation - summarize context
        summary = "This is a long conversation..."
        return {"messages": [AIMessage(content=summary)]}
    
    # Continue normal conversation
    return {"messages": [AIMessage(content="Continuing conversation...")]}
```

## Integration with Other Concepts

### Chat Models

Messages as state work seamlessly with chat models:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

def llm_node(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### Tool Binding

When using tools, messages can include tool calls and results:

```python
from langchain_core.messages import ToolMessage

def tool_node(state: MessagesState):
    # Execute tool and add result to messages
    tool_result = ToolMessage(
        content="Tool execution result",
        tool_call_id="call_123"
    )
    return {"messages": [tool_result]}
```

## Troubleshooting

### Common Issues

1. **Message Loss**: Ensure you're appending messages, not replacing them
2. **Type Errors**: Use proper message types (HumanMessage, AIMessage, etc.)
3. **State Override**: Implement reducers for proper state updates

### Debugging Tips

```python
def debug_node(state: MessagesState):
    print(f"Current message count: {len(state['messages'])}")
    print(f"Last message: {state['messages'][-1] if state['messages'] else 'None'}")
    return state
```

## Related Concepts

- [Reducers](./reducers.md) - Understanding state update patterns
- [MessagesState](./messages-state.md) - Built-in state management
- [Chat Models](../fundamentals/chat-models.md) - Working with conversational models
- [Tool Integration](../fundamentals/tools.md) - Using tools with message state 