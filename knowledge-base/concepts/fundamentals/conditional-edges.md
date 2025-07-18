# Conditional Edges

## Overview

Conditional edges are the core mechanism in LangGraph for implementing dynamic routing and decision-making logic. They allow your graph to take different paths based on the current state, enabling intelligent, adaptive workflows that can respond to changing conditions.

## What are Conditional Edges?

Conditional edges are connections between nodes that include logic to determine which path to take based on the current state. Unlike simple edges that always follow the same path, conditional edges can route execution to different nodes depending on conditions you define.

## Key Concepts

### 1. Routing Logic

Conditional edges use routing functions that examine the current state and return the name of the next node to execute:

```python
from typing import Literal

def route_based_on_priority(state: State) -> Literal["high_priority", "normal_priority", "low_priority"]:
    priority = state.get("priority", "normal")
    
    if priority == "high":
        return "high_priority"
    elif priority == "low":
        return "low_priority"
    else:
        return "normal_priority"
```

### 2. Decision Points

Conditional edges create decision points in your graph where the execution can branch:

```python
# Add conditional edges to a node
workflow.add_conditional_edges(
    "analyze_request",  # Source node
    route_based_on_priority,  # Routing function
    {
        "high_priority": "immediate_processing",
        "normal_priority": "standard_processing", 
        "low_priority": "batch_processing"
    }
)
```

### 3. Multiple Execution Paths

Your graph can have multiple possible execution paths that converge or diverge based on conditions:

```python
# Multiple paths that can converge
workflow.add_conditional_edges("start", route_function, {
    "path_a": "process_a",
    "path_b": "process_b"
})

# Both paths can converge to the same node
workflow.add_edge("process_a", "finalize")
workflow.add_edge("process_b", "finalize")
```

## Implementation Patterns

### 1. Simple If/Else Routing

The most basic pattern for binary decisions:

```python
def simple_router(state: State) -> Literal["yes", "no"]:
    condition = state.get("condition", False)
    return "yes" if condition else "no"

workflow.add_conditional_edges("check", simple_router, {
    "yes": "process_yes",
    "no": "process_no"
})
```

### 2. Multi-Way Routing

For decisions with more than two possible outcomes:

```python
def multi_way_router(state: State) -> Literal["option_a", "option_b", "option_c"]:
    value = state.get("value", 0)
    
    if value < 10:
        return "option_a"
    elif value < 50:
        return "option_b"
    else:
        return "option_c"

workflow.add_conditional_edges("analyze", multi_way_router, {
    "option_a": "process_a",
    "option_b": "process_b", 
    "option_c": "process_c"
})
```

### 3. State-Based Routing

Using complex state conditions for routing decisions:

```python
def state_based_router(state: State) -> Literal["continue", "retry", "error"]:
    # Check multiple state conditions
    if state.get("error_count", 0) > 3:
        return "error"
    elif state.get("retry_count", 0) > 0:
        return "retry"
    else:
        return "continue"

workflow.add_conditional_edges("process", state_based_router, {
    "continue": "next_step",
    "retry": "retry_step",
    "error": "error_handler"
})
```

### 4. Dynamic Routing

Routing that can change based on runtime conditions:

```python
def dynamic_router(state: State) -> str:
    # Dynamic routing based on available resources
    available_workers = state.get("available_workers", 0)
    queue_size = state.get("queue_size", 0)
    
    if available_workers > 0 and queue_size > 10:
        return "parallel_processing"
    elif queue_size > 5:
        return "batch_processing"
    else:
        return "single_processing"

workflow.add_conditional_edges("route", dynamic_router, {
    "parallel_processing": "parallel_node",
    "batch_processing": "batch_node",
    "single_processing": "single_node"
})
```

## Advanced Patterns

### 1. Nested Routing

Complex routing with nested decision logic:

```python
def nested_router(state: State) -> str:
    request_type = state.get("request_type")
    priority = state.get("priority")
    
    if request_type == "urgent":
        if priority == "high":
            return "immediate_urgent"
        else:
            return "fast_urgent"
    else:
        if priority == "high":
            return "priority_normal"
        else:
            return "standard_normal"

workflow.add_conditional_edges("route", nested_router, {
    "immediate_urgent": "immediate_node",
    "fast_urgent": "fast_node",
    "priority_normal": "priority_node",
    "standard_normal": "standard_node"
})
```

### 2. Error Handling Routing

Routing that handles different types of errors:

```python
def error_router(state: State) -> str:
    error_type = state.get("error_type")
    retry_count = state.get("retry_count", 0)
    
    if retry_count >= 3:
        return "max_retries"
    elif error_type == "network":
        return "retry_network"
    elif error_type == "validation":
        return "fix_validation"
    else:
        return "general_error"

workflow.add_conditional_edges("handle_error", error_router, {
    "max_retries": "escalate",
    "retry_network": "retry",
    "fix_validation": "validate",
    "general_error": "log_error"
})
```

### 3. Performance-Based Routing

Routing based on performance metrics:

```python
def performance_router(state: State) -> str:
    response_time = state.get("response_time", 0)
    cpu_usage = state.get("cpu_usage", 0)
    
    if response_time > 5000 or cpu_usage > 80:
        return "optimize"
    elif response_time > 2000:
        return "monitor"
    else:
        return "normal"

workflow.add_conditional_edges("check_performance", performance_router, {
    "optimize": "optimization_node",
    "monitor": "monitoring_node",
    "normal": "continue_node"
})
```

## Best Practices

### 1. Keep Routing Functions Simple

```python
# ✅ Good: Simple, focused routing logic
def route_by_type(state: State) -> Literal["type_a", "type_b"]:
    return "type_a" if state.get("type") == "A" else "type_b"

# ❌ Avoid: Complex logic in routing functions
def complex_router(state: State) -> str:
    # Don't put complex business logic here
    # Keep routing functions focused on routing decisions
    pass
```

### 2. Use Descriptive Node Names

```python
# ✅ Good: Clear, descriptive names
workflow.add_conditional_edges("analyze_request", route_request, {
    "high_priority": "process_immediately",
    "normal_priority": "process_standard",
    "low_priority": "process_batch"
})

# ❌ Avoid: Unclear names
workflow.add_conditional_edges("process", route, {
    "a": "node1",
    "b": "node2",
    "c": "node3"
})
```

### 3. Handle Edge Cases

```python
def robust_router(state: State) -> str:
    # Always provide a default case
    try:
        condition = state.get("condition")
        if condition == "option_a":
            return "process_a"
        elif condition == "option_b":
            return "process_b"
        else:
            return "default_process"  # Default case
    except Exception:
        return "error_handler"  # Error case
```

### 4. Document Routing Logic

```python
def documented_router(state: State) -> Literal["path_a", "path_b", "path_c"]:
    """
    Routes requests based on priority and type.
    
    Args:
        state: Current graph state
        
    Returns:
        Next node to execute
        
    Logic:
        - High priority requests go to path_a
        - Type 'B' requests go to path_b  
        - All others go to path_c
    """
    priority = state.get("priority", "normal")
    request_type = state.get("type", "A")
    
    if priority == "high":
        return "path_a"
    elif request_type == "B":
        return "path_b"
    else:
        return "path_c"
```

## Common Use Cases

### 1. Request Classification

```python
def classify_request(state: State) -> Literal["spam", "urgent", "normal"]:
    content = state.get("content", "")
    
    # Simple spam detection
    spam_indicators = ["buy now", "limited time", "act fast"]
    if any(indicator in content.lower() for indicator in spam_indicators):
        return "spam"
    
    # Urgency detection
    urgent_words = ["urgent", "emergency", "asap"]
    if any(word in content.lower() for word in urgent_words):
        return "urgent"
    
    return "normal"
```

### 2. Workflow Orchestration

```python
def orchestrate_workflow(state: State) -> str:
    current_step = state.get("current_step")
    completed_steps = state.get("completed_steps", [])
    
    if current_step == "start":
        return "validation"
    elif current_step == "validation" and "validation" in completed_steps:
        return "processing"
    elif current_step == "processing" and "processing" in completed_steps:
        return "finalization"
    else:
        return "error_handler"
```

### 3. Resource Allocation

```python
def allocate_resources(state: State) -> str:
    available_cpu = state.get("available_cpu", 100)
    task_complexity = state.get("task_complexity", "medium")
    
    if task_complexity == "high" and available_cpu > 50:
        return "dedicated_resources"
    elif task_complexity == "medium":
        return "shared_resources"
    else:
        return "queue_for_later"
```

## Debugging Conditional Edges

### 1. Add Logging

```python
def debug_router(state: State) -> str:
    print(f"Current state: {state}")
    
    decision = route_logic(state)
    print(f"Routing decision: {decision}")
    
    return decision
```

### 2. Test All Paths

```python
# Test all possible routing outcomes
test_states = [
    {"condition": "A"},
    {"condition": "B"},
    {"condition": "C"}
]

for test_state in test_states:
    result = router_function(test_state)
    print(f"State: {test_state} -> Route: {result}")
```

### 3. Validate Routing Logic

```python
def validate_router(state: State) -> str:
    # Validate input state
    if "required_field" not in state:
        raise ValueError("Missing required field")
    
    # Perform routing
    result = route_logic(state)
    
    # Validate output
    valid_routes = ["route_a", "route_b", "route_c"]
    if result not in valid_routes:
        raise ValueError(f"Invalid route: {result}")
    
    return result
```

## Related Concepts

- [State Management](../state-management/) - How state influences routing decisions
- [Graph Structure](./graph-structure.md) - Understanding nodes and edges
- [Multi-Actor Systems](./multi-actor.md) - Coordinating multiple components
- [Error Handling](../patterns/error-handling.md) - Handling routing failures 