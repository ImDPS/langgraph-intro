"""
Exported graph from LangGraph Studio: simple_graph
Generated on: 2025-09-13T12:38:56.547667
"""

from typing import TypedDict
from langgraph.graph import StateGraph


class GraphState(TypedDict):
    """State schema for simple_graph"""
    message: str
    response: str


def process_message(state: GraphState) -> GraphState:
    """Process message node - exported from Studio"""
    message = state.get("message", "")
    response = f"Processed in Studio: {message}"
    return {"message": message, "response": response}


def create_simple_graph():
    """Create the simple_graph graph - exported from Studio"""
    graph = StateGraph(GraphState)
    graph.add_node("process_message", process_message)
    graph.set_entry_point("process_message")
    graph.set_finish_point("process_message")
    return graph.compile()


if __name__ == "__main__":
    app = create_simple_graph()
    result = app.invoke({"message": "Hello from Studio!", "response": ""})
    print(result)
