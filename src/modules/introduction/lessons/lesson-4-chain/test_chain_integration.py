"""
Test suite for Lesson 4: Chain Integration with LangChain

This module provides comprehensive tests for all chain integration functionality.
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph

from chain_integration import (
    ChainIntegration,
    ChainState,
    create_basic_chain_graph,
    create_tool_calling_graph,
    create_multi_chain_workflow,
    multiply,
    add
)


class TestChainIntegration:
    """Test the main ChainIntegration class."""
    
    def setup_method(self):
        """Setup test environment."""
        # Mock the Google API key
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
        
        # Mock the LLM
        self.mock_llm = Mock()
        self.mock_llm.invoke.return_value = AIMessage(content="Test response")
        
        # Create integration instance with mocked LLM
        with patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI') as mock_chat:
            mock_chat.return_value = self.mock_llm
            self.integration = ChainIntegration()
    
    def test_initialization(self):
        """Test ChainIntegration initialization."""
        assert self.integration.model_name == "gemini-2.0-flash-lite"
        assert self.integration.llm is not None
        assert len(self.integration.tools) == 2
    
    def test_setup_llm_missing_api_key(self):
        """Test LLM setup with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable is required"):
                ChainIntegration()
    
    def test_setup_tools(self):
        """Test tool setup."""
        tools = self.integration._setup_tools()
        assert len(tools) == 2
        assert tools[0]["name"] == "multiply"
        assert tools[1]["name"] == "add"
    
    def test_get_tool_functions(self):
        """Test getting tool functions."""
        functions = self.integration._get_tool_functions()
        assert len(functions) == 2
        assert callable(functions[0])  # multiply
        assert callable(functions[1])  # add
    
    def test_execute_tool_call_multiply(self):
        """Test executing multiply tool call."""
        tool_call = {
            "name": "multiply",
            "args": {"a": 5, "b": 3}
        }
        result = self.integration._execute_tool_call(tool_call)
        assert result == 15
    
    def test_execute_tool_call_add(self):
        """Test executing add tool call."""
        tool_call = {
            "name": "add",
            "args": {"a": 5, "b": 3}
        }
        result = self.integration._execute_tool_call(tool_call)
        assert result == 8
    
    def test_execute_tool_call_unknown(self):
        """Test executing unknown tool call."""
        tool_call = {
            "name": "unknown_tool",
            "args": {}
        }
        result = self.integration._execute_tool_call(tool_call)
        assert "Unknown tool" in result


class TestBasicChainIntegration:
    """Test basic chain integration functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
        
        # Mock the LLM
        self.mock_llm = Mock()
        self.mock_llm.invoke.return_value = AIMessage(content="Test response")
        
        # Create integration instance
        with patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI') as mock_chat:
            mock_chat.return_value = self.mock_llm
            self.integration = ChainIntegration()
    
    def test_create_basic_chain_graph(self):
        """Test creating basic chain graph."""
        graph = self.integration.create_basic_chain_graph()
        assert isinstance(graph, StateGraph)
        assert graph is not None
    
    def test_basic_llm_node_success(self):
        """Test basic LLM node with successful execution."""
        # Create the graph to get access to the node function
        graph = self.integration.create_basic_chain_graph()
        
        # Test state
        state = {
            "messages": [HumanMessage(content="Hello")]
        }
        
        # Mock the LLM response
        self.mock_llm.invoke.return_value = AIMessage(content="Hello! How can I help?")
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0].content == "Hello! How can I help?"
    
    def test_basic_llm_node_empty_messages(self):
        """Test basic LLM node with empty messages."""
        graph = self.integration.create_basic_chain_graph()
        
        # Test state with empty messages
        state = {"messages": []}
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "Hello! How can I help you today?" in result["messages"][0].content
    
    def test_basic_llm_node_error_handling(self):
        """Test basic LLM node error handling."""
        graph = self.integration.create_basic_chain_graph()
        
        # Mock LLM to raise an exception
        self.mock_llm.invoke.side_effect = Exception("LLM error")
        
        # Test state
        state = {
            "messages": [HumanMessage(content="Hello")]
        }
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "I encountered an error" in result["messages"][0].content


class TestToolCalling:
    """Test tool calling functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
        
        # Mock the LLM with tool calls
        self.mock_llm = Mock()
        self.mock_llm_with_tools = Mock()
        
        # Create integration instance
        with patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI') as mock_chat:
            mock_chat.return_value = self.mock_llm
            self.integration = ChainIntegration()
    
    def test_create_tool_calling_graph(self):
        """Test creating tool calling graph."""
        graph = self.integration.create_tool_calling_graph()
        assert isinstance(graph, StateGraph)
        assert graph is not None
    
    def test_tool_calling_node_with_tool_calls(self):
        """Test tool calling node with actual tool calls."""
        # Mock tool call response
        mock_tool_call = {
            "name": "multiply",
            "args": {"a": 5, "b": 3}
        }
        
        mock_response = Mock()
        mock_response.tool_calls = [mock_tool_call]
        mock_response.content = "I'll calculate that for you."
        
        # Mock the LLM with tools
        self.mock_llm.bind_tools.return_value = self.mock_llm_with_tools
        self.mock_llm_with_tools.invoke.return_value = mock_response
        
        # Create graph
        graph = self.integration.create_tool_calling_graph()
        
        # Test state
        state = {
            "messages": [HumanMessage(content="What is 5 times 3?")]
        }
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 2  # Original response + tool response
    
    def test_tool_calling_node_without_tool_calls(self):
        """Test tool calling node without tool calls."""
        # Mock response without tool calls
        mock_response = Mock()
        mock_response.tool_calls = []
        mock_response.content = "I don't need to use any tools for this."
        
        # Mock the LLM with tools
        self.mock_llm.bind_tools.return_value = self.mock_llm_with_tools
        self.mock_llm_with_tools.invoke.return_value = mock_response
        
        # Create graph
        graph = self.integration.create_tool_calling_graph()
        
        # Test state
        state = {
            "messages": [HumanMessage(content="Hello!")]
        }
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 1  # Only the response


class TestMultiChainWorkflow:
    """Test multi-chain workflow functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
        
        # Mock the LLM
        self.mock_llm = Mock()
        self.mock_llm.invoke.return_value = AIMessage(content="Test response")
        
        # Create integration instance
        with patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI') as mock_chat:
            mock_chat.return_value = self.mock_llm
            self.integration = ChainIntegration()
    
    def test_create_multi_chain_workflow(self):
        """Test creating multi-chain workflow."""
        graph = self.integration.create_multi_chain_workflow()
        assert isinstance(graph, StateGraph)
        assert graph is not None
    
    def test_multi_chain_workflow_execution(self):
        """Test multi-chain workflow execution."""
        # Mock different responses for different nodes
        responses = [
            AIMessage(content="Analysis: This is a complex request that requires careful consideration."),
            AIMessage(content="Recommendations: Based on the analysis, I recommend the following steps."),
            AIMessage(content="Summary: Here's a concise summary of the analysis and recommendations.")
        ]
        
        self.mock_llm.invoke.side_effect = responses
        
        # Create graph
        graph = self.integration.create_multi_chain_workflow()
        
        # Test state
        state = {
            "messages": [HumanMessage(content="I need help with project management")]
        }
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 4  # Original + 3 node responses
        assert "Summary:" in result["messages"][-1].content
    
    def test_analysis_node_error_handling(self):
        """Test analysis node error handling."""
        # Mock LLM to raise an exception
        self.mock_llm.invoke.side_effect = Exception("Analysis error")
        
        # Create graph
        graph = self.integration.create_multi_chain_workflow()
        
        # Test state
        state = {
            "messages": [HumanMessage(content="Test message")]
        }
        
        # Execute the graph
        result = graph.invoke(state)
        
        assert "messages" in result
        assert "Analysis error" in result["messages"][-1].content


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def setup_method(self):
        """Setup test environment."""
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
    
    @patch('lesson_4_chain.chain_integration.ChainIntegration')
    def test_create_basic_chain_graph_function(self, mock_integration):
        """Test create_basic_chain_graph convenience function."""
        mock_graph = Mock()
        mock_integration.return_value.create_basic_chain_graph.return_value = mock_graph
        
        graph = create_basic_chain_graph()
        
        assert graph == mock_graph
        mock_integration.assert_called_once()
        mock_integration.return_value.create_basic_chain_graph.assert_called_once()
    
    @patch('lesson_4_chain.chain_integration.ChainIntegration')
    def test_create_tool_calling_graph_function(self, mock_integration):
        """Test create_tool_calling_graph convenience function."""
        mock_graph = Mock()
        mock_integration.return_value.create_tool_calling_graph.return_value = mock_graph
        
        graph = create_tool_calling_graph()
        
        assert graph == mock_graph
        mock_integration.assert_called_once()
        mock_integration.return_value.create_tool_calling_graph.assert_called_once()
    
    @patch('lesson_4_chain.chain_integration.ChainIntegration')
    def test_create_multi_chain_workflow_function(self, mock_integration):
        """Test create_multi_chain_workflow convenience function."""
        mock_graph = Mock()
        mock_integration.return_value.create_multi_chain_workflow.return_value = mock_graph
        
        graph = create_multi_chain_workflow()
        
        assert graph == mock_graph
        mock_integration.assert_called_once()
        mock_integration.return_value.create_multi_chain_workflow.assert_called_once()


class TestToolFunctions:
    """Test tool functions."""
    
    def test_multiply_function(self):
        """Test multiply function."""
        assert multiply(5, 3) == 15
        assert multiply(0, 10) == 0
        assert multiply(-2, 4) == -8
    
    def test_add_function(self):
        """Test add function."""
        assert add(5, 3) == 8
        assert add(0, 10) == 10
        assert add(-2, 4) == 2


class TestIntegrationTests:
    """Integration tests for the complete workflow."""
    
    def setup_method(self):
        """Setup test environment."""
        os.environ["GOOGLE_API_KEY"] = "test_api_key"
    
    @patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI')
    def test_complete_basic_chain_workflow(self, mock_chat):
        """Test complete basic chain workflow."""
        # Mock LLM
        mock_llm = Mock()
        mock_llm.invoke.return_value = AIMessage(content="Hello! How can I help you?")
        mock_chat.return_value = mock_llm
        
        # Create and test graph
        graph = create_basic_chain_graph()
        result = graph.invoke({
            "messages": [HumanMessage(content="Hello!")]
        })
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "Hello! How can I help you?" in result["messages"][0].content
    
    @patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI')
    def test_complete_tool_calling_workflow(self, mock_chat):
        """Test complete tool calling workflow."""
        # Mock LLM with tool calls
        mock_llm = Mock()
        mock_llm_with_tools = Mock()
        
        mock_tool_call = {
            "name": "multiply",
            "args": {"a": 5, "b": 3}
        }
        
        mock_response = Mock()
        mock_response.tool_calls = [mock_tool_call]
        mock_response.content = "I'll calculate that for you."
        
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        mock_llm_with_tools.invoke.return_value = mock_response
        mock_chat.return_value = mock_llm
        
        # Create and test graph
        graph = create_tool_calling_graph()
        result = graph.invoke({
            "messages": [HumanMessage(content="What is 5 times 3?")]
        })
        
        assert "messages" in result
        assert len(result["messages"]) == 2
    
    @patch('lesson_4_chain.chain_integration.ChatGoogleGenerativeAI')
    def test_complete_multi_chain_workflow(self, mock_chat):
        """Test complete multi-chain workflow."""
        # Mock LLM with different responses
        mock_llm = Mock()
        responses = [
            AIMessage(content="Analysis: This is a complex request."),
            AIMessage(content="Recommendations: Here are my recommendations."),
            AIMessage(content="Summary: Here's the summary.")
        ]
        mock_llm.invoke.side_effect = responses
        mock_chat.return_value = mock_llm
        
        # Create and test graph
        graph = create_multi_chain_workflow()
        result = graph.invoke({
            "messages": [HumanMessage(content="I need help with project management")]
        })
        
        assert "messages" in result
        assert len(result["messages"]) == 4  # Original + 3 responses


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
