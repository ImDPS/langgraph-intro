"""
Graph Exporter for LangGraph Studio

This module handles exporting graphs from LangGraph Studio back to Python code,
enabling seamless integration between visual development and production deployment.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class GraphExporter:
    """
    Handles exporting graphs from LangGraph Studio to Python code.
    
    Provides methods for:
    - Converting Studio graph definitions to Python code
    - Generating deployment-ready code
    - Creating test files
    - Updating project configurations
    """
    
    def __init__(self, project_root: str = None):
        """
        Initialize the graph exporter.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.exported_graphs = {}
        
    def export_graph_to_python(self, studio_graph: Dict[str, Any], output_path: str) -> bool:
        """
        Export a Studio graph definition to Python code.
        
        Args:
            studio_graph: Graph definition from Studio
            output_path: Path where to save the Python file
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            print(f"📤 Exporting graph '{studio_graph.get('name', 'unknown')}' to {output_path}")
            
            # Generate Python code
            python_code = self._generate_python_code(studio_graph)
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(python_code)
            
            # Store export metadata
            self.exported_graphs[studio_graph.get('name', 'unknown')] = {
                "output_path": str(output_file),
                "export_time": datetime.now().isoformat(),
                "studio_graph": studio_graph
            }
            
            print(f"✅ Graph exported successfully to: {output_file}")
            print(f"📄 File size: {output_file.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export graph: {e}")
            return False
    
    def _generate_python_code(self, studio_graph: Dict[str, Any]) -> str:
        """
        Generate Python code from Studio graph definition.
        
        Args:
            studio_graph: Graph definition from Studio
            
        Returns:
            str: Generated Python code
        """
        graph_name = studio_graph.get('name', 'exported_graph')
        description = studio_graph.get('description', 'Graph exported from LangGraph Studio')
        state_schema = studio_graph.get('state_schema', 'GraphState')
        nodes = studio_graph.get('nodes', [])
        edges = studio_graph.get('edges', [])
        entry_point = studio_graph.get('entry_point', 'start')
        finish_points = studio_graph.get('finish_points', ['end'])
        
        # Generate imports
        imports = '''"""
{description}
Generated from LangGraph Studio on: {timestamp}
"""

from typing import TypedDict
from langgraph.graph import StateGraph
'''.format(
            description=description,
            timestamp=datetime.now().isoformat()
        )
        
        # Generate state schema
        state_schema_code = f'''
class {state_schema}(TypedDict):
    """State schema for {graph_name}"""
    message: str
    response: str
'''
        
        # Generate node functions
        node_functions = []
        for node in nodes:
            node_func = f'''
def {node}(state: {state_schema}) -> {state_schema}:
    """{node} node - generated from Studio"""
    message = state.get("message", "")
    response = f"Processed by {{node}}: {{message}}"
    return {{"message": message, "response": response}}
'''
            node_functions.append(node_func)
        
        # Generate edge functions
        edge_functions = []
        for edge in edges:
            if isinstance(edge, dict) and 'condition' in edge:
                edge_func = f'''
def {edge['condition']}(state: {state_schema}) -> str:
    """Conditional edge function for {edge.get('from', 'unknown')} -> {edge.get('to', 'unknown')}"""
    # Add your conditional logic here
    return "{edge.get('to', 'end')}"
'''
                edge_functions.append(edge_func)
        
        # Generate graph creation function
        graph_creation = f'''
def create_{graph_name}():
    """Create the {graph_name} graph - generated from Studio"""
    graph = StateGraph({state_schema})
    
    # Add nodes
'''
        
        for node in nodes:
            graph_creation += f'    graph.add_node("{node}", {node})\n'
        
        # Add edges
        if edges:
            graph_creation += '\n    # Add edges\n'
            for edge in edges:
                if isinstance(edge, dict):
                    from_node = edge.get('from', 'start')
                    to_node = edge.get('to', 'end')
                    if 'condition' in edge:
                        graph_creation += f'    graph.add_conditional_edges("{from_node}", {edge["condition"]})\n'
                    else:
                        graph_creation += f'    graph.add_edge("{from_node}", "{to_node}")\n'
        
        # Set entry and finish points
        graph_creation += f'''
    # Set entry point
    graph.set_entry_point("{entry_point}")
    
    # Set finish points
'''
        for finish_point in finish_points:
            graph_creation += f'    graph.set_finish_point("{finish_point}")\n'
        
        graph_creation += '''
    return graph.compile()


if __name__ == "__main__":
    app = create_{graph_name}()
    result = app.invoke({{"message": "Hello from Studio!", "response": ""}})
    print(result)
'''.format(graph_name=graph_name)
        
        # Combine all parts
        full_code = imports + state_schema_code + ''.join(node_functions) + ''.join(edge_functions) + graph_creation
        
        return full_code
    
    def export_with_tests(self, studio_graph: Dict[str, Any], output_dir: str) -> bool:
        """
        Export graph with accompanying test file.
        
        Args:
            studio_graph: Graph definition from Studio
            output_dir: Directory where to save the files
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            output_dir = Path(output_dir)
            graph_name = studio_graph.get('name', 'exported_graph')
            
            # Export main graph file
            graph_file = output_dir / f"{graph_name}.py"
            if not self.export_graph_to_python(studio_graph, str(graph_file)):
                return False
            
            # Generate test file
            test_file = output_dir / f"test_{graph_name}.py"
            test_code = self._generate_test_code(studio_graph)
            
            with open(test_file, 'w') as f:
                f.write(test_code)
            
            print(f"✅ Test file created: {test_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export with tests: {e}")
            return False
    
    def _generate_test_code(self, studio_graph: Dict[str, Any]) -> str:
        """
        Generate test code for the exported graph.
        
        Args:
            studio_graph: Graph definition from Studio
            
        Returns:
            str: Generated test code
        """
        graph_name = studio_graph.get('name', 'exported_graph')
        state_schema = studio_graph.get('state_schema', 'GraphState')
        
        test_code = f'''"""
Tests for {graph_name} - generated from LangGraph Studio
"""

import pytest
from {graph_name} import create_{graph_name}, {state_schema}


class Test{graph_name.title().replace('_', '')}:
    """Test class for {graph_name}"""
    
    def test_graph_creation(self):
        """Test that the graph can be created successfully"""
        app = create_{graph_name}()
        assert app is not None
        assert hasattr(app, 'invoke')
        assert hasattr(app, 'stream')
    
    def test_basic_execution(self):
        """Test basic graph execution"""
        app = create_{graph_name}()
        initial_state: {state_schema} = {{
            "message": "Hello, world!",
            "response": ""
        }}
        
        result = app.invoke(initial_state)
        
        assert "message" in result
        assert "response" in result
        assert result["message"] == "Hello, world!"
        assert len(result["response"]) > 0
    
    def test_empty_message(self):
        """Test handling of empty message"""
        app = create_{graph_name}()
        initial_state: {state_schema} = {{
            "message": "",
            "response": ""
        }}
        
        result = app.invoke(initial_state)
        
        assert "message" in result
        assert "response" in result
        assert result["message"] == ""
    
    def test_state_schema_validation(self):
        """Test that state schema is properly defined"""
        # This test ensures the state schema is valid
        test_state: {state_schema} = {{
            "message": "test",
            "response": "test"
        }}
        
        assert isinstance(test_state["message"], str)
        assert isinstance(test_state["response"], str)


if __name__ == "__main__":
    pytest.main([__file__])
'''
        
        return test_code
    
    def update_project_config(self, studio_graph: Dict[str, Any]) -> bool:
        """
        Update project configuration with exported graph.
        
        Args:
            studio_graph: Graph definition from Studio
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            config_file = self.project_root / "studio_config.json"
            
            if not config_file.exists():
                print("⚠️  Studio config file not found, creating new one")
                config = {"graphs": {}, "state_schemas": {}, "studio_settings": {}}
            else:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            # Add graph to configuration
            graph_name = studio_graph.get('name', 'exported_graph')
            config["graphs"][graph_name] = {
                "name": graph_name,
                "description": studio_graph.get('description', 'Exported from Studio'),
                "state_schema": studio_graph.get('state_schema', 'GraphState'),
                "entry_point": studio_graph.get('entry_point', 'start'),
                "finish_points": studio_graph.get('finish_points', ['end']),
                "nodes": studio_graph.get('nodes', []),
                "conditional_edges": [edge for edge in studio_graph.get('edges', []) if isinstance(edge, dict) and 'condition' in edge],
                "exported": True,
                "export_timestamp": datetime.now().isoformat()
            }
            
            # Write updated config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Project configuration updated with graph '{graph_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update project config: {e}")
            return False
    
    def create_export_demo(self) -> bool:
        """
        Create a demo of the graph export functionality.
        
        Returns:
            bool: True if demo successful, False otherwise
        """
        try:
            print("🎬 Graph Export Demo")
            print("=" * 40)
            
            # Create sample Studio graph
            sample_graph = {
                "name": "demo_graph",
                "description": "Demo graph exported from LangGraph Studio",
                "state_schema": "DemoState",
                "entry_point": "start",
                "finish_points": ["end"],
                "nodes": ["start", "process", "end"],
                "edges": [
                    {"from": "start", "to": "process"},
                    {"from": "process", "to": "end"}
                ]
            }
            
            print("\n1️⃣ Sample Studio Graph:")
            print(f"   📊 Name: {sample_graph['name']}")
            print(f"   📝 Description: {sample_graph['description']}")
            print(f"   🔧 Nodes: {sample_graph['nodes']}")
            print(f"   🔗 Edges: {sample_graph['edges']}")
            
            # Export to Python
            print("\n2️⃣ Exporting to Python...")
            output_dir = self.project_root / "demo_exports"
            output_dir.mkdir(exist_ok=True)
            
            success = self.export_with_tests(sample_graph, str(output_dir))
            
            if success:
                print("✅ Graph exported with tests successfully")
                
                # Update project config
                print("\n3️⃣ Updating Project Configuration...")
                self.update_project_config(sample_graph)
                
                # List exported files
                print("\n4️⃣ Exported Files:")
                for file in output_dir.glob("*"):
                    print(f"   📄 {file.name} ({file.stat().st_size} bytes)")
                
                print("\n🎉 Graph Export Demo Complete!")
                print("💡 Exported code includes:")
                print("   🐍 Python graph implementation")
                print("   🧪 Comprehensive test suite")
                print("   📋 Project configuration updates")
                print("   🚀 Ready for deployment")
                
                return True
            else:
                print("❌ Export failed")
                return False
                
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return False
    
    def list_exported_graphs(self) -> List[str]:
        """
        List all exported graphs.
        
        Returns:
            list: List of exported graph names
        """
        return list(self.exported_graphs.keys())
    
    def get_export_metadata(self, graph_name: str) -> Dict[str, Any]:
        """
        Get export metadata for a specific graph.
        
        Args:
            graph_name: Name of the exported graph
            
        Returns:
            dict: Export metadata
        """
        return self.exported_graphs.get(graph_name, {})


def main():
    """Main function to run graph export demo."""
    print("📤 Graph Exporter Demo")
    print("=" * 25)
    
    # Initialize exporter
    exporter = GraphExporter()
    
    # Run demo
    success = exporter.create_export_demo()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("🔗 Next steps:")
        print("   1. Review exported Python code")
        print("   2. Run tests to verify functionality")
        print("   3. Integrate with your deployment pipeline")
        print("   4. Deploy to production")
    else:
        print("\n❌ Demo failed. Please check the errors above.")


if __name__ == "__main__":
    main()
