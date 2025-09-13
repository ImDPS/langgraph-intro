"""
Graph Importer for LangGraph Studio

This module handles importing graphs from code into LangGraph Studio
for visualization, debugging, and interactive development.
"""

import ast
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Type, Callable


class GraphImporter:
    """
    Handles importing graphs from Python code into LangGraph Studio.
    
    Provides methods for:
    - Parsing Python graph definitions
    - Extracting graph structure and metadata
    - Converting to Studio-compatible format
    - Validating graph imports
    """
    
    def __init__(self, project_root: str = None):
        """
        Initialize the graph importer.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.imported_graphs = {}
        
    def import_graph_from_module(self, module_path: str, graph_name: str = None) -> Dict[str, Any]:
        """
        Import a graph from a Python module.
        
        Args:
            module_path: Path to the Python module (e.g., "src.module.graph")
            graph_name: Name of the graph function to import (optional)
            
        Returns:
            dict: Graph metadata and structure
        """
        try:
            print(f"📥 Importing graph from module: {module_path}")
            
            # Import the module
            module = importlib.import_module(module_path)
            
            # Find graph functions
            graph_functions = self._find_graph_functions(module)
            
            if not graph_functions:
                raise ValueError(f"No graph functions found in module {module_path}")
            
            # If specific graph name provided, use it
            if graph_name and graph_name in graph_functions:
                selected_graph = graph_functions[graph_name]
            else:
                # Use the first graph function found
                selected_graph = list(graph_functions.values())[0]
                graph_name = list(graph_functions.keys())[0]
            
            # Extract graph metadata
            graph_metadata = self._extract_graph_metadata(selected_graph, graph_name)
            
            # Store imported graph
            self.imported_graphs[graph_name] = graph_metadata
            
            print(f"✅ Graph '{graph_name}' imported successfully")
            return graph_metadata
            
        except Exception as e:
            print(f"❌ Failed to import graph: {e}")
            return {}
    
    def _find_graph_functions(self, module) -> Dict[str, Callable]:
        """
        Find graph creation functions in a module.
        
        Args:
            module: The imported module
            
        Returns:
            dict: Dictionary of graph function names to functions
        """
        graph_functions = {}
        
        for name, obj in inspect.getmembers(module):
            if (inspect.isfunction(obj) and 
                (name.startswith('create_') or name.endswith('_graph') or 'graph' in name.lower())):
                graph_functions[name] = obj
        
        return graph_functions
    
    def _extract_graph_metadata(self, graph_function: Callable, graph_name: str) -> Dict[str, Any]:
        """
        Extract metadata from a graph function.
        
        Args:
            graph_function: The graph creation function
            graph_name: Name of the graph
            
        Returns:
            dict: Graph metadata
        """
        try:
            # Get function source code
            source = inspect.getsource(graph_function)
            
            # Parse the source code
            tree = ast.parse(source)
            
            # Extract information from AST
            metadata = {
                "name": graph_name,
                "function_name": graph_function.__name__,
                "module": graph_function.__module__,
                "description": self._extract_docstring(graph_function),
                "source_code": source,
                "nodes": self._extract_nodes_from_ast(tree),
                "edges": self._extract_edges_from_ast(tree),
                "state_schema": self._extract_state_schema_from_ast(tree),
                "entry_point": self._extract_entry_point_from_ast(tree),
                "finish_points": self._extract_finish_points_from_ast(tree)
            }
            
            return metadata
            
        except Exception as e:
            print(f"⚠️  Could not extract metadata from {graph_name}: {e}")
            return {
                "name": graph_name,
                "function_name": graph_function.__name__,
                "module": graph_function.__module__,
                "description": "Graph imported from code",
                "error": str(e)
            }
    
    def _extract_docstring(self, func: Callable) -> str:
        """Extract docstring from function."""
        return func.__doc__ or "No description available"
    
    def _extract_nodes_from_ast(self, tree: ast.AST) -> List[str]:
        """Extract node names from AST."""
        nodes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (hasattr(node.func, 'attr') and 
                    node.func.attr == 'add_node' and 
                    len(node.args) > 0 and 
                    isinstance(node.args[0], ast.Constant)):
                    nodes.append(node.args[0].value)
        
        return nodes
    
    def _extract_edges_from_ast(self, tree: ast.AST) -> List[Dict[str, str]]:
        """Extract edge information from AST."""
        edges = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (hasattr(node.func, 'attr') and 
                    node.func.attr == 'add_edge' and 
                    len(node.args) >= 2):
                    from_node = node.args[0].value if isinstance(node.args[0], ast.Constant) else "unknown"
                    to_node = node.args[1].value if isinstance(node.args[1], ast.Constant) else "unknown"
                    edges.append({"from": from_node, "to": to_node})
        
        return edges
    
    def _extract_state_schema_from_ast(self, tree: ast.AST) -> str:
        """Extract state schema class name from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "State" in node.name or "state" in node.name.lower():
                    return node.name
        
        return "UnknownState"
    
    def _extract_entry_point_from_ast(self, tree: ast.AST) -> str:
        """Extract entry point from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (hasattr(node.func, 'attr') and 
                    node.func.attr == 'set_entry_point' and 
                    len(node.args) > 0 and 
                    isinstance(node.args[0], ast.Constant)):
                    return node.args[0].value
        
        return "unknown"
    
    def _extract_finish_points_from_ast(self, tree: ast.AST) -> List[str]:
        """Extract finish points from AST."""
        finish_points = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (hasattr(node.func, 'attr') and 
                    node.func.attr == 'set_finish_point' and 
                    len(node.args) > 0 and 
                    isinstance(node.args[0], ast.Constant)):
                    finish_points.append(node.args[0].value)
        
        return finish_points
    
    def import_from_file(self, file_path: str, graph_name: str = None) -> Dict[str, Any]:
        """
        Import a graph from a Python file.
        
        Args:
            file_path: Path to the Python file
            graph_name: Name of the graph to import (optional)
            
        Returns:
            dict: Graph metadata
        """
        try:
            file_path = Path(file_path)
            
            # Convert file path to module path
            relative_path = file_path.relative_to(self.project_root)
            module_path = str(relative_path.with_suffix('')).replace('/', '.')
            
            print(f"📁 Importing from file: {file_path}")
            print(f"🔗 Module path: {module_path}")
            
            return self.import_graph_from_module(module_path, graph_name)
            
        except Exception as e:
            print(f"❌ Failed to import from file: {e}")
            return {}
    
    def import_simple_graph(self) -> Dict[str, Any]:
        """
        Import the simple graph from lesson 2.
        
        Returns:
            dict: Simple graph metadata
        """
        try:
            module_path = "src.modules.introduction.lessons.lesson_2_simple_graph.simple_graph"
            return self.import_graph_from_module(module_path, "create_simple_graph")
            
        except Exception as e:
            print(f"❌ Failed to import simple graph: {e}")
            return {}
    
    def list_imported_graphs(self) -> List[str]:
        """
        List all imported graphs.
        
        Returns:
            list: List of imported graph names
        """
        return list(self.imported_graphs.keys())
    
    def get_graph_metadata(self, graph_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific imported graph.
        
        Args:
            graph_name: Name of the graph
            
        Returns:
            dict: Graph metadata
        """
        return self.imported_graphs.get(graph_name, {})
    
    def export_to_studio_format(self, graph_name: str) -> Dict[str, Any]:
        """
        Export graph metadata to Studio-compatible format.
        
        Args:
            graph_name: Name of the graph to export
            
        Returns:
            dict: Studio-compatible graph definition
        """
        try:
            if graph_name not in self.imported_graphs:
                raise ValueError(f"Graph '{graph_name}' not found in imported graphs")
            
            metadata = self.imported_graphs[graph_name]
            
            # Convert to Studio format
            studio_format = {
                "name": metadata.get("name", graph_name),
                "description": metadata.get("description", "Imported graph"),
                "state_schema": metadata.get("state_schema", "UnknownState"),
                "entry_point": metadata.get("entry_point", "unknown"),
                "finish_points": metadata.get("finish_points", []),
                "nodes": metadata.get("nodes", []),
                "edges": metadata.get("edges", []),
                "source_module": metadata.get("module", ""),
                "function_name": metadata.get("function_name", ""),
                "import_timestamp": __import__('datetime').datetime.now().isoformat()
            }
            
            return studio_format
            
        except Exception as e:
            print(f"❌ Failed to export to Studio format: {e}")
            return {}
    
    def create_import_demo(self) -> bool:
        """
        Create a demo of the graph import functionality.
        
        Returns:
            bool: True if demo successful, False otherwise
        """
        try:
            print("🎬 Graph Import Demo")
            print("=" * 40)
            
            # Import simple graph
            print("\n1️⃣ Importing Simple Graph...")
            simple_graph = self.import_simple_graph()
            
            if simple_graph:
                print("✅ Simple graph imported successfully")
                print(f"   📊 Graph name: {simple_graph.get('name', 'N/A')}")
                print(f"   🔧 Function: {simple_graph.get('function_name', 'N/A')}")
                print(f"   📝 Description: {simple_graph.get('description', 'N/A')[:50]}...")
                print(f"   🔗 Nodes: {simple_graph.get('nodes', [])}")
                print(f"   🎯 Entry point: {simple_graph.get('entry_point', 'N/A')}")
                print(f"   🏁 Finish points: {simple_graph.get('finish_points', [])}")
            else:
                print("❌ Failed to import simple graph")
                return False
            
            # Export to Studio format
            print("\n2️⃣ Exporting to Studio Format...")
            studio_format = self.export_to_studio_format("create_simple_graph")
            
            if studio_format:
                print("✅ Graph exported to Studio format")
                print(f"   📋 Studio name: {studio_format.get('name', 'N/A')}")
                print(f"   🏗️  State schema: {studio_format.get('state_schema', 'N/A')}")
                print(f"   📊 Nodes: {studio_format.get('nodes', [])}")
                print(f"   🔗 Edges: {studio_format.get('edges', [])}")
            else:
                print("❌ Failed to export to Studio format")
                return False
            
            # List imported graphs
            print("\n3️⃣ Listing Imported Graphs...")
            imported = self.list_imported_graphs()
            print(f"📚 Total imported graphs: {len(imported)}")
            for graph in imported:
                print(f"   📊 {graph}")
            
            print("\n🎉 Graph Import Demo Complete!")
            print("💡 In Studio, you would see:")
            print("   🎨 Visual graph representation")
            print("   🔍 Interactive node inspection")
            print("   📊 Real-time state monitoring")
            print("   🧪 Live graph testing")
            
            return True
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return False


def main():
    """Main function to run graph import demo."""
    print("📥 Graph Importer Demo")
    print("=" * 25)
    
    # Initialize importer
    importer = GraphImporter()
    
    # Run demo
    success = importer.create_import_demo()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("🔗 Next steps:")
        print("   1. Import your graphs into Studio")
        print("   2. Visualize and debug your graphs")
        print("   3. Test graph execution interactively")
    else:
        print("\n❌ Demo failed. Please check the errors above.")


if __name__ == "__main__":
    main()
