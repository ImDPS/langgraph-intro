# Reducers in LangGraph

## Overview

Reducers are functions that handle state updates in LangGraph, particularly important when working with message-based state. They solve the problem of state override by properly merging new state with existing state.

## The Problem Reducers Solve

### State Override Issue

In LangGraph, each node can return a new state that completely replaces the previous state. This becomes problematic when you want to accumulate data, such as messages in a conversation:

```python
# ❌ Problem: Each node overrides the previous state
def node1(state):
    return {"messages": [message1]}  # Only message1

def node2(state):
    return {"messages": [message2]}  # Only message2 - message1 is lost!
```

### The Solution: Reducers

Reducers allow you to specify how to combine new state with existing state, rather than replacing it entirely.

## Types of Reducers

### 1. Built-in Reducers

LangGraph provides several built-in reducers for common operations:

```python
from langgraph.graph import add_messages, add_messages_interactive

# Add messages to existing conversation
workflow.add_node("chat", chat_node, reducer=add_messages)

# Add messages with interactive capabilities
workflow.add_node("chat", chat_node, reducer=add_messages_interactive)
```

### 2. Custom Reducers

You can create custom reducers for specific state update patterns:

```python
def custom_message_reducer(old_state, new_state):
    """Custom reducer that appends new messages to existing ones"""
    old_messages = old_state.get("messages", [])
    new_messages = new_state.get("messages", [])
    
    return {
        **old_state,
        "messages": old_messages + new_messages
    }

# Use custom reducer
workflow.add_node("chat", chat_node, reducer=custom_message_reducer)
```

## Common Reducer Patterns

### 1. Message Accumulation

The most common pattern is accumulating messages:

```python
def message_accumulator(old_state, new_state):
    """Accumulate messages while preserving other state"""
    return {
        **old_state,
        "messages": old_state.get("messages", []) + new_state.get("messages", [])
    }
```

### 2. List Concatenation

For any list-based state:

```python
def list_concatenator(old_state, new_state):
    """Concatenate lists in state"""
    result = {}
    for key in new_state:
        if isinstance(new_state[key], list):
            result[key] = old_state.get(key, []) + new_state[key]
        else:
            result[key] = new_state[key]
    return {**old_state, **result}
```

### 3. Dictionary Merging

For complex state objects:

```python
def dict_merger(old_state, new_state):
    """Deep merge dictionaries"""
    result = old_state.copy()
    for key, value in new_state.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = dict_merger(result[key], value)
        else:
            result[key] = value
    return result
```

## Using Reducers with MessagesState

When using the built-in `MessagesState`, you can leverage the `add_messages` reducer:

```python
from langgraph.graph import StateGraph, MessagesState, add_messages
from langchain_core.messages import HumanMessage, AIMessage

def chat_node(state: MessagesState):
    # Process the conversation
    response = "Hello! I received your message."
    return {"messages": [AIMessage(content=response)]}

# Build graph with reducer
workflow = StateGraph(MessagesState)
workflow.add_node("chat", chat_node, reducer=add_messages)
workflow.set_entry_point("chat")
workflow.set_finish_point("chat")

app = workflow.compile()

# Usage
result = app.invoke({"messages": [HumanMessage(content="Hi!")]})
# Messages will be accumulated: [HumanMessage, AIMessage]
```

## Advanced Reducer Patterns

### 1. Conditional Reducers

Reducers that apply different logic based on conditions:

```python
def conditional_reducer(old_state, new_state):
    """Apply different logic based on state conditions"""
    if len(old_state.get("messages", [])) > 10:
        # Long conversation - keep only recent messages
        recent_messages = old_state["messages"][-5:]
        return {
            **old_state,
            "messages": recent_messages + new_state.get("messages", [])
        }
    else:
        # Normal accumulation
        return {
            **old_state,
            "messages": old_state.get("messages", []) + new_state.get("messages", [])
        }
```

### 2. Multi-Key Reducers

Reducers that handle multiple state keys:

```python
def multi_key_reducer(old_state, new_state):
    """Handle multiple state keys with different logic"""
    result = old_state.copy()
    
    # Handle messages
    if "messages" in new_state:
        result["messages"] = old_state.get("messages", []) + new_state["messages"]
    
    # Handle counters
    if "counter" in new_state:
        result["counter"] = old_state.get("counter", 0) + new_state["counter"]
    
    # Handle flags (override)
    if "flags" in new_state:
        result["flags"] = new_state["flags"]
    
    return result
```

## Best Practices

### 1. Use Built-in Reducers When Possible

```python
# ✅ Good: Use built-in add_messages
workflow.add_node("chat", chat_node, reducer=add_messages)

# ❌ Avoid: Manual message handling unless necessary
def manual_reducer(old_state, new_state):
    return {
        **old_state,
        "messages": old_state.get("messages", []) + new_state.get("messages", [])
    }
```

### 2. Preserve State Immutability

```python
# ✅ Good: Create new state objects
def good_reducer(old_state, new_state):
    return {**old_state, **new_state}

# ❌ Avoid: Modifying existing state
def bad_reducer(old_state, new_state):
    old_state.update(new_state)  # Mutates original state
    return old_state
```

### 3. Handle Edge Cases

```python
def robust_reducer(old_state, new_state):
    """Handle edge cases in state updates"""
    # Ensure old_state is not None
    old_state = old_state or {}
    
    # Ensure new_state is not None
    new_state = new_state or {}
    
    # Handle missing keys gracefully
    return {
        **old_state,
        **new_state,
        "messages": old_state.get("messages", []) + new_state.get("messages", [])
    }
```

## Debugging Reducers

### Debugging Tips

```python
def debug_reducer(old_state, new_state):
    """Debug reducer with logging"""
    print(f"Old state keys: {list(old_state.keys())}")
    print(f"New state keys: {list(new_state.keys())}")
    
    result = {
        **old_state,
        "messages": old_state.get("messages", []) + new_state.get("messages", [])
    }
    
    print(f"Result state keys: {list(result.keys())}")
    return result
```

### Common Issues

1. **State Loss**: Ensure you're not accidentally overriding important state
2. **Type Errors**: Handle cases where expected keys don't exist
3. **Performance**: Avoid deep copying large state objects unnecessarily

## Integration Examples

### With Chat Models

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

def llm_node(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

workflow.add_node("llm", llm_node, reducer=add_messages)
```

### With Tools

```python
def tool_node(state: MessagesState):
    # Execute tool and return result
    tool_result = ToolMessage(content="Tool executed successfully")
    return {"messages": [tool_result]}

workflow.add_node("tool", tool_node, reducer=add_messages)
```

## Related Concepts

- [Using Messages as State](./using-messages-as-state.md) - How to use messages as state
- [MessagesState](./messages-state.md) - Built-in state management
- [State Management Overview](./README.md) - General state management concepts 