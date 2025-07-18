# State Components

## Overview

State components in LangGraph handle data flow and persistence throughout graph execution. This section covers the technical components and patterns for state management.

## Key Components

### Built-in State Classes

- **MessagesState** - Pre-built state for conversational applications
- **TypedDict States** - Custom state definitions with type safety
- **Dynamic States** - Runtime state management

### State Management Patterns

- **Reducers** - Functions for combining state updates
- **State Persistence** - Long-term state storage
- **State Validation** - Type checking and validation

## Documentation

For comprehensive information about state management concepts and patterns, see:

- [State Management Concepts](../../concepts/state-management/) - Core concepts and theory
- [Using Messages as State](../../concepts/state-management/using-messages-as-state.md) - Message-based state patterns
- [Reducers](../../concepts/state-management/reducers.md) - State update functions
- [MessagesState](../../concepts/state-management/messages-state.md) - Built-in state class

## Quick Reference

### Basic State Usage

```python
from langgraph.graph import StateGraph, MessagesState

# Use built-in MessagesState
workflow = StateGraph(MessagesState)

# Custom state definition
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class CustomState(TypedDict):
    messages: List[BaseMessage]
    metadata: dict
    counter: int

workflow = StateGraph(CustomState)
```

### State Updates with Reducers

```python
from langgraph.graph import add_messages

# Built-in reducer for messages
workflow.add_node("chat", chat_node, reducer=add_messages)

# Custom reducer
def custom_reducer(old_state, new_state):
    return {
        **old_state,
        "messages": old_state["messages"] + new_state["messages"],
        "counter": old_state.get("counter", 0) + 1
    }
```

## Related Sections

- [Nodes](../nodes/) - Node components that work with state
- [Graphs](../graphs/) - Graph structures and state flow
- [Edges](../edges/) - Edge routing and state transitions 