# What is LangGraph?

[Home](../../../) > [Concepts](../../) > [Fundamentals](../) > What is LangGraph?

## Overview

LangGraph is built for developers who want to build powerful, adaptable AI agents. Developers choose LangGraph for:

- **Reliability and controllability.** Steer agent actions with moderation checks and human-in-the-loop approvals. LangGraph persists context for long-running workflows, keeping your agents on course.
- **Low-level and extensible.** Build custom agents with fully descriptive, low-level primitives free from rigid abstractions that limit customization. Design scalable multi-agent systems, with each agent serving a specific role tailored to your use case.
- **First-class streaming support.** With token-by-token streaming and streaming of intermediate steps, LangGraph gives users clear visibility into agent reasoning and actions as they unfold in real time.

## Definition

LangGraph is a framework for building stateful, multi-actor applications with LLMs. It extends the LangChain ecosystem by providing a way to coordinate multiple chains (or actors) in a cyclic graph structure, enabling complex workflows that can maintain state and handle multiple interactions.

## Key Characteristics

- **Reliability and controllability**: Steer agent actions with moderation checks and human-in-the-loop approvals
- **Low-level and extensible**: Build custom agents with fully descriptive, low-level primitives
- **First-class streaming support**: Token-by-token streaming and streaming of intermediate steps
- **Stateful**: Applications maintain state across interactions
- **Multi-actor**: Multiple components can interact and coordinate
- **Cyclic**: Graphs can have cycles, enabling iterative processes

## When to Use

LangGraph is ideal when you need to:
- Build conversational agents that maintain context
- Create multi-step workflows with decision points
- Coordinate multiple AI agents or tools
- Build applications that require iterative processing
- Create complex state management systems
- Build reliable and controllable AI agents
- Design scalable multi-agent systems
- Implement real-time streaming of agent actions and reasoning

## How It Works

1. **Define State Schema**: Define the structure of your application's state
2. **Create Nodes**: Define functions that process the state
3. **Build Graph**: Connect nodes with edges to create the workflow
4. **Add Conditional Edges**: Define routing logic based on state
5. **Compile and Run**: Execute the graph with initial state

## Example

```python
from langgraph import StateGraph, END
from typing import TypedDict, Annotated

# Define state schema
class AgentState(TypedDict):
    messages: list[str]
    current_step: str

# Define nodes
def process_message(state: AgentState) -> AgentState:
    # Process the current message
    return {"messages": state["messages"], "current_step": "processed"}

def decide_next_step(state: AgentState) -> AgentState:
    # Decide what to do next
    return {"messages": state["messages"], "current_step": "decided"}

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("process", process_message)
workflow.add_node("decide", decide_next_step)

# Add edges
workflow.add_edge("process", "decide")
workflow.add_conditional_edges(
    "decide",
    lambda state: "end" if state["current_step"] == "finished" else "process"
)

# Compile
app = workflow.compile()
```

## Related Concepts

- [State Management](../state-management/state-schema.md) - How to define and manage state
- [Graph Structure](../fundamentals/graph-structure.md) - Understanding nodes and edges
- [Conditional Routing](../fundamentals/conditional-edges.md) - How to route based on state
- [Multi-Actor Systems](../fundamentals/multi-actor.md) - Coordinating multiple components

## Further Reading

- [Official LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Why LangGraph](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)
- [Getting Started Tutorial](../../../learnings/tutorials/getting-started.md)
- [Simple Chatbot Example](../../../learnings/examples/simple-chatbot.md)
- [State Management Guide](../../../concepts/state-management/overview.md)
- [LangGraph vs LangChain](../../../faqs/general/langgraph-vs-langchain.md)

---

*Last Updated: 2024-01-15*
*Contributor: LangGraph Team* 