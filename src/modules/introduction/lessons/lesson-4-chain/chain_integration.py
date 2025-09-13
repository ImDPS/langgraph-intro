"""
Lesson 4: Chain Integration with LangChain

This module demonstrates how to integrate LangChain chains into LangGraph applications.
It covers basic chain integration, tool calling, and multi-chain workflows.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, AnyMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChainState(MessagesState):
    """
    State schema for chain-based graphs.
    
    Inherits from MessagesState which provides:
    - messages: List of conversation messages
    - Automatic message appending via add_messages reducer
    """
    pass


class ChainIntegration:
    """
    Main class for LangChain integration with LangGraph.
    
    This class provides methods to create various types of chain-based graphs
    and demonstrates different integration patterns.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash-lite"):
        """
        Initialize the chain integration.
        
        Args:
            model_name: The Gemini model to use
        """
        self.model_name = model_name
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        
    def _setup_llm(self) -> ChatGoogleGenerativeAI:
        """Setup the Gemini LLM."""
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.7,
            max_output_tokens=1024
        )
    
    def _setup_tools(self) -> List[Dict[str, Any]]:
        """Setup available tools for the LLM."""
        return [
            {
                "name": "multiply",
                "description": "Multiply two numbers together",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "The first number to multiply"},
                        "b": {"type": "integer", "description": "The second number to multiply"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "add",
                "description": "Add two numbers together",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "The first number to add"},
                        "b": {"type": "integer", "description": "The second number to add"}
                    },
                    "required": ["a", "b"]
                }
            }
        ]
    
    def create_basic_chain_graph(self) -> StateGraph:
        """
        Create a basic chain graph that demonstrates simple LLM integration.
        
        Returns:
            Compiled StateGraph with basic chain functionality
        """
        logger.info("Creating basic chain graph")
        
        def basic_llm_node(state: ChainState) -> Dict[str, List[AnyMessage]]:
            """
            Basic LLM node that processes messages and returns responses.
            
            Args:
                state: Current graph state with messages
                
            Returns:
                Updated state with LLM response
            """
            try:
                # Get the last user message
                last_message = state["messages"][-1] if state["messages"] else None
                
                if not last_message:
                    response = AIMessage(content="Hello! How can I help you today?")
                else:
                    # Process with LLM
                    response = self.llm.invoke(state["messages"])
                
                logger.info(f"LLM response generated: {response.content[:100]}...")
                return {"messages": [response]}
                
            except Exception as e:
                logger.error(f"Error in basic_llm_node: {e}")
                error_response = AIMessage(content=f"I encountered an error: {str(e)}")
                return {"messages": [error_response]}
        
        # Build the graph
        builder = StateGraph(ChainState)
        builder.add_node("basic_llm", basic_llm_node)
        builder.add_edge(START, "basic_llm")
        builder.add_edge("basic_llm", END)
        
        return builder.compile()
    
    def create_tool_calling_graph(self) -> StateGraph:
        """
        Create a graph with tool calling capabilities.
        
        Returns:
            Compiled StateGraph with tool calling functionality
        """
        logger.info("Creating tool calling graph")
        
        # Bind tools to LLM
        llm_with_tools = self.llm.bind_tools(self._get_tool_functions())
        
        def tool_calling_node(state: ChainState) -> Dict[str, List[AnyMessage]]:
            """
            Tool calling node that can execute functions based on LLM decisions.
            
            Args:
                state: Current graph state with messages
                
            Returns:
                Updated state with tool calls and responses
            """
            try:
                # Get LLM response with potential tool calls
                response = llm_with_tools.invoke(state["messages"])
                
                # Check if the response contains tool calls
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    logger.info(f"Tool calls detected: {len(response.tool_calls)}")
                    
                    # Execute tool calls
                    tool_results = []
                    for tool_call in response.tool_calls:
                        result = self._execute_tool_call(tool_call)
                        tool_results.append(result)
                    
                    # Create tool response message
                    tool_response = AIMessage(
                        content=f"Tool execution results: {tool_results}",
                        tool_calls=response.tool_calls
                    )
                    
                    return {"messages": [response, tool_response]}
                else:
                    return {"messages": [response]}
                    
            except Exception as e:
                logger.error(f"Error in tool_calling_node: {e}")
                error_response = AIMessage(content=f"I encountered an error: {str(e)}")
                return {"messages": [error_response]}
        
        # Build the graph
        builder = StateGraph(ChainState)
        builder.add_node("tool_calling_llm", tool_calling_node)
        builder.add_edge(START, "tool_calling_llm")
        builder.add_edge("tool_calling_llm", END)
        
        return builder.compile()
    
    def create_multi_chain_workflow(self) -> StateGraph:
        """
        Create a multi-chain workflow with specialized nodes.
        
        Returns:
            Compiled StateGraph with multiple specialized chains
        """
        logger.info("Creating multi-chain workflow")
        
        def analysis_node(state: ChainState) -> Dict[str, List[AnyMessage]]:
            """
            Analysis node that provides detailed analysis of user input.
            
            Args:
                state: Current graph state with messages
                
            Returns:
                Updated state with analysis response
            """
            try:
                # Create analysis prompt
                analysis_prompt = SystemMessage(content="""
                You are an expert analyst. Provide a detailed analysis of the user's request.
                Break down the request into key components and provide insights.
                Be thorough and professional in your analysis.
                """)
                
                # Combine system prompt with user messages
                messages = [analysis_prompt] + state["messages"]
                response = self.llm.invoke(messages)
                
                logger.info("Analysis node completed")
                return {"messages": [response]}
                
            except Exception as e:
                logger.error(f"Error in analysis_node: {e}")
                error_response = AIMessage(content=f"Analysis error: {str(e)}")
                return {"messages": [error_response]}
        
        def recommendation_node(state: ChainState) -> Dict[str, List[AnyMessage]]:
            """
            Recommendation node that provides actionable recommendations.
            
            Args:
                state: Current graph state with messages
                
            Returns:
                Updated state with recommendations
            """
            try:
                # Create recommendation prompt
                recommendation_prompt = SystemMessage(content="""
                You are a strategic advisor. Based on the previous analysis,
                provide specific, actionable recommendations.
                Focus on practical next steps and implementation strategies.
                """)
                
                # Combine system prompt with user messages
                messages = [recommendation_prompt] + state["messages"]
                response = self.llm.invoke(messages)
                
                logger.info("Recommendation node completed")
                return {"messages": [response]}
                
            except Exception as e:
                logger.error(f"Error in recommendation_node: {e}")
                error_response = AIMessage(content=f"Recommendation error: {str(e)}")
                return {"messages": [error_response]}
        
        def summary_node(state: ChainState) -> Dict[str, List[AnyMessage]]:
            """
            Summary node that provides a concise summary of the workflow.
            
            Args:
                state: Current graph state with messages
                
            Returns:
                Updated state with summary
            """
            try:
                # Create summary prompt
                summary_prompt = SystemMessage(content="""
                You are a communication expert. Provide a clear, concise summary
                of the analysis and recommendations provided.
                Make it easy to understand and actionable.
                """)
                
                # Combine system prompt with user messages
                messages = [summary_prompt] + state["messages"]
                response = self.llm.invoke(messages)
                
                logger.info("Summary node completed")
                return {"messages": [response]}
                
            except Exception as e:
                logger.error(f"Error in summary_node: {e}")
                error_response = AIMessage(content=f"Summary error: {str(e)}")
                return {"messages": [error_response]}
        
        # Build the multi-chain workflow
        builder = StateGraph(ChainState)
        builder.add_node("analysis", analysis_node)
        builder.add_node("recommendations", recommendation_node)
        builder.add_node("summary", summary_node)
        
        # Define the workflow
        builder.add_edge(START, "analysis")
        builder.add_edge("analysis", "recommendations")
        builder.add_edge("recommendations", "summary")
        builder.add_edge("summary", END)
        
        return builder.compile()
    
    def _get_tool_functions(self) -> List[Any]:
        """Get tool functions for LLM binding."""
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers together."""
            return a * b
        
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        return [multiply, add]
    
    def _execute_tool_call(self, tool_call: Any) -> Any:
        """
        Execute a tool call and return the result.
        
        Args:
            tool_call: The tool call to execute
            
        Returns:
            Result of the tool execution
        """
        try:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name == "multiply":
                return multiply(tool_args["a"], tool_args["b"])
            elif tool_name == "add":
                return add(tool_args["a"], tool_args["b"])
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            logger.error(f"Error executing tool call: {e}")
            return f"Tool execution error: {str(e)}"


# Convenience functions for easy access
def create_basic_chain_graph() -> StateGraph:
    """Create a basic chain graph."""
    integration = ChainIntegration()
    return integration.create_basic_chain_graph()


def create_tool_calling_graph() -> StateGraph:
    """Create a tool calling graph."""
    integration = ChainIntegration()
    return integration.create_tool_calling_graph()


def create_multi_chain_workflow() -> StateGraph:
    """Create a multi-chain workflow."""
    integration = ChainIntegration()
    return integration.create_multi_chain_workflow()


# Tool functions for LLM binding
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


if __name__ == "__main__":
    # Example usage
    print("Lesson 4: Chain Integration with LangChain")
    print("=" * 50)
    
    # Test basic chain
    print("\n1. Testing Basic Chain Graph:")
    try:
        basic_graph = create_basic_chain_graph()
        result = basic_graph.invoke({
            "messages": [HumanMessage(content="Hello! What can you help me with?")]
        })
        print(f"Response: {result['messages'][-1].content}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test tool calling
    print("\n2. Testing Tool Calling Graph:")
    try:
        tool_graph = create_tool_calling_graph()
        result = tool_graph.invoke({
            "messages": [HumanMessage(content="What is 23 multiplied by 45?")]
        })
        print(f"Response: {result['messages'][-1].content}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test multi-chain workflow
    print("\n3. Testing Multi-Chain Workflow:")
    try:
        workflow_graph = create_multi_chain_workflow()
        result = workflow_graph.invoke({
            "messages": [HumanMessage(content="I need help with project management strategies")]
        })
        print(f"Final response: {result['messages'][-1].content[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
