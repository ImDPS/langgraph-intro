# Conditional Edges Component

## Overview

Conditional edges are a core component in LangGraph that enable dynamic routing and decision-making within graphs. They allow execution to follow different paths based on the current state, making graphs intelligent and adaptive.

## Technical Implementation

### Basic Structure

```python
from langgraph.graph import StateGraph
from typing import Literal

# Define routing function
def route_function(state: State) -> Literal["path_a", "path_b"]:
    condition = state.get("condition")
    return "path_a" if condition else "path_b"

# Add conditional edges to graph
workflow = StateGraph(State)
workflow.add_conditional_edges(
    "source_node",           # Source node
    route_function,          # Routing function
    {
        "path_a": "node_a",  # Route mapping
        "path_b": "node_b"
    }
)
```

### Routing Function Signature

```python
from typing import Literal, Union

# Simple routing function
def simple_router(state: State) -> Literal["option_a", "option_b"]:
    pass

# Dynamic routing function
def dynamic_router(state: State) -> str:
    pass

# Union type for multiple possible routes
def union_router(state: State) -> Union[Literal["a"], Literal["b"], Literal["c"]]:
    pass
```

## Component Features

### 1. Type Safety

Conditional edges support type-safe routing with Literal types:

```python
from typing import Literal

def type_safe_router(state: State) -> Literal["high", "medium", "low"]:
    priority = state.get("priority", "medium")
    
    if priority == "high":
        return "high"
    elif priority == "low":
        return "low"
    else:
        return "medium"

# LangGraph validates that all routes are handled
workflow.add_conditional_edges("route", type_safe_router, {
    "high": "high_priority_node",
    "medium": "medium_priority_node", 
    "low": "low_priority_node"
})
```

### 2. Dynamic Routing

Support for runtime-determined routes:

```python
def dynamic_router(state: State) -> str:
    # Route can be determined at runtime
    available_nodes = state.get("available_nodes", ["default"])
    return available_nodes[0]

# Handle dynamic routes
workflow.add_conditional_edges("route", dynamic_router, {
    "node_a": "process_a",
    "node_b": "process_b",
    "default": "default_process"
})
```

### 3. Error Handling

Built-in error handling for routing failures:

```python
def robust_router(state: State) -> str:
    try:
        condition = state.get("condition")
        if condition == "valid":
            return "valid_path"
        else:
            return "invalid_path"
    except Exception:
        return "error_path"

workflow.add_conditional_edges("route", robust_router, {
    "valid_path": "process_valid",
    "invalid_path": "handle_invalid",
    "error_path": "handle_error"
})
```

## Configuration Options

### 1. Route Mapping

```python
# Simple mapping
routes = {
    "option_a": "node_a",
    "option_b": "node_b"
}

# With fallback
routes = {
    "option_a": "node_a",
    "option_b": "node_b",
    "__fallback__": "default_node"  # Fallback route
}

workflow.add_conditional_edges("route", router_function, routes)
```

### 2. Conditional Edge Configuration

```python
# Basic configuration
workflow.add_conditional_edges("source", router, routes)

# With additional options
workflow.add_conditional_edges(
    "source",
    router,
    routes,
    # Additional configuration options can be added here
)
```

## Advanced Patterns

### 1. Multi-Level Routing

```python
def multi_level_router(state: State) -> str:
    level_1 = state.get("level_1")
    level_2 = state.get("level_2")
    
    if level_1 == "category_a":
        if level_2 == "subcategory_1":
            return "route_a1"
        else:
            return "route_a2"
    else:
        if level_2 == "subcategory_1":
            return "route_b1"
        else:
            return "route_b2"

workflow.add_conditional_edges("route", multi_level_router, {
    "route_a1": "process_a1",
    "route_a2": "process_a2",
    "route_b1": "process_b1",
    "route_b2": "process_b2"
})
```

### 2. State-Dependent Routing

```python
def state_dependent_router(state: State) -> str:
    # Route based on multiple state conditions
    error_count = state.get("error_count", 0)
    retry_count = state.get("retry_count", 0)
    priority = state.get("priority", "normal")
    
    if error_count > 3:
        return "escalate"
    elif retry_count > 0:
        return "retry"
    elif priority == "high":
        return "priority"
    else:
        return "normal"

workflow.add_conditional_edges("route", state_dependent_router, {
    "escalate": "escalation_node",
    "retry": "retry_node",
    "priority": "priority_node",
    "normal": "normal_node"
})
```

### 3. Performance-Based Routing

```python
def performance_router(state: State) -> str:
    response_time = state.get("response_time", 0)
    queue_size = state.get("queue_size", 0)
    
    if response_time > 5000:
        return "optimize"
    elif queue_size > 100:
        return "scale"
    else:
        return "normal"

workflow.add_conditional_edges("route", performance_router, {
    "optimize": "optimization_node",
    "scale": "scaling_node",
    "normal": "normal_node"
})
```

## Integration Examples

### 1. With State Management

```python
from langgraph.graph import MessagesState

def message_router(state: MessagesState) -> str:
    messages = state.get("messages", [])
    
    if not messages:
        return "welcome"
    
    last_message = messages[-1]
    content = last_message.content.lower()
    
    if "help" in content:
        return "help"
    elif "order" in content:
        return "order"
    else:
        return "general"

workflow = StateGraph(MessagesState)
workflow.add_conditional_edges("route", message_router, {
    "welcome": "welcome_node",
    "help": "help_node",
    "order": "order_node",
    "general": "general_node"
})
```

### 2. With Error Handling

```python
def error_aware_router(state: State) -> str:
    # Check for errors in state
    errors = state.get("errors", [])
    
    if errors:
        error_type = errors[-1].get("type")
        if error_type == "validation":
            return "fix_validation"
        elif error_type == "network":
            return "retry_network"
        else:
            return "handle_general_error"
    
    return "continue_normal"

workflow.add_conditional_edges("route", error_aware_router, {
    "fix_validation": "validation_node",
    "retry_network": "retry_node",
    "handle_general_error": "error_node",
    "continue_normal": "normal_node"
})
```

### 3. With Memory Systems

```python
def memory_aware_router(state: State) -> str:
    # Route based on memory state
    memory_usage = state.get("memory_usage", 0)
    conversation_length = state.get("conversation_length", 0)
    
    if memory_usage > 80:
        return "cleanup_memory"
    elif conversation_length > 50:
        return "summarize"
    else:
        return "continue"

workflow.add_conditional_edges("route", memory_aware_router, {
    "cleanup_memory": "memory_cleanup_node",
    "summarize": "summarization_node",
    "continue": "continuation_node"
})
```

## Best Practices

### 1. Keep Routing Functions Pure

```python
# ✅ Good: Pure function, no side effects
def pure_router(state: State) -> str:
    return "route_a" if state.get("condition") else "route_b"

# ❌ Avoid: Side effects in routing functions
def impure_router(state: State) -> str:
    # Don't modify state or perform I/O here
    state["modified"] = True  # Side effect
    return "route_a"
```

### 2. Handle All Possible Routes

```python
# ✅ Good: Handle all possible return values
def complete_router(state: State) -> Literal["a", "b", "c"]:
    value = state.get("value")
    if value == "A":
        return "a"
    elif value == "B":
        return "b"
    else:
        return "c"

# Ensure all routes are mapped
workflow.add_conditional_edges("route", complete_router, {
    "a": "process_a",
    "b": "process_b", 
    "c": "process_c"
})
```

### 3. Use Descriptive Route Names

```python
# ✅ Good: Clear, descriptive names
def descriptive_router(state: State) -> Literal["high_priority", "normal_priority", "low_priority"]:
    priority = state.get("priority", "normal")
    if priority == "high":
        return "high_priority"
    elif priority == "low":
        return "low_priority"
    else:
        return "normal_priority"

# ❌ Avoid: Unclear names
def unclear_router(state: State) -> Literal["a", "b", "c"]:
    # Unclear what these routes represent
    pass
```

## Troubleshooting

### Common Issues

1. **Missing Route Mapping**
   ```python
   # Error: Route not found
   def router(state: State) -> Literal["a", "b"]:
       return "a"
   
   # Missing mapping for "b"
   workflow.add_conditional_edges("route", router, {"a": "node_a"})
   ```

2. **Type Mismatch**
   ```python
   # Error: Return type doesn't match route keys
   def router(state: State) -> Literal["a", "b"]:
       return "a"
   
   # Route keys don't match return type
   workflow.add_conditional_edges("route", router, {"x": "node_x", "y": "node_y"})
   ```

3. **State Access Errors**
   ```python
   # Error: Accessing non-existent state keys
   def router(state: State) -> str:
       return "a" if state["missing_key"] else "b"  # KeyError
   ```

### Debugging Tips

```python
def debug_router(state: State) -> str:
    # Add logging to understand routing decisions
    print(f"Router input state: {state}")
    
    result = route_logic(state)
    print(f"Router decision: {result}")
    
    return result
```

## Related Components

- [Simple Edges](./simple-edges.md) - Basic edge connections
- [Dynamic Edges](./dynamic-edges.md) - Runtime edge creation
- [Parallel Edges](./parallel-edges.md) - Concurrent execution paths
- [State Components](../state/) - State management for routing decisions 