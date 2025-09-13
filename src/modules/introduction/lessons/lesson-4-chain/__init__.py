"""
Lesson 4: Chain Integration with LangChain

This module provides chain integration functionality for LangGraph applications.
"""

from chain_integration import (
    ChainIntegration,
    ChainState,
    create_basic_chain_graph,
    create_tool_calling_graph,
    create_multi_chain_workflow,
    multiply,
    add
)

__all__ = [
    "ChainIntegration",
    "ChainState", 
    "create_basic_chain_graph",
    "create_tool_calling_graph",
    "create_multi_chain_workflow",
    "multiply",
    "add"
]