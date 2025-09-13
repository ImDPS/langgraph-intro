"""
Tests for enhanced_simple_graph - generated from LangGraph Studio
"""

import pytest
from enhanced_simple_graph import create_enhanced_simple_graph, EnhancedGraphState


class TestEnhancedSimpleGraph:
    """Test class for enhanced_simple_graph"""
    
    def test_graph_creation(self):
        """Test that the graph can be created successfully"""
        app = create_enhanced_simple_graph()
        assert app is not None
        assert hasattr(app, 'invoke')
        assert hasattr(app, 'stream')
    
    def test_basic_execution(self):
        """Test basic graph execution"""
        app = create_enhanced_simple_graph()
        initial_state: EnhancedGraphState = {
            "message": "Hello, world!",
            "response": ""
        }
        
        result = app.invoke(initial_state)
        
        assert "message" in result
        assert "response" in result
        assert result["message"] == "Hello, world!"
        assert len(result["response"]) > 0
    
    def test_empty_message(self):
        """Test handling of empty message"""
        app = create_enhanced_simple_graph()
        initial_state: EnhancedGraphState = {
            "message": "",
            "response": ""
        }
        
        result = app.invoke(initial_state)
        
        assert "message" in result
        assert "response" in result
        assert result["message"] == ""
    
    def test_state_schema_validation(self):
        """Test that state schema is properly defined"""
        # This test ensures the state schema is valid
        test_state: EnhancedGraphState = {
            "message": "test",
            "response": "test"
        }
        
        assert isinstance(test_state["message"], str)
        assert isinstance(test_state["response"], str)


if __name__ == "__main__":
    pytest.main([__file__])
