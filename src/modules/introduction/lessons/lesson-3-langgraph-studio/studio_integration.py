"""
LangGraph Studio Integration

This module provides integration with LangGraph Studio for visual graph development,
debugging, and monitoring. It enables seamless workflow between visual development
and production-ready code deployment.
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional, Any
from pathlib import Path


class StudioIntegration:
    """
    Main class for integrating with LangGraph Studio.
    
    Provides methods for:
    - Connecting to Studio
    - Importing/exporting graphs
    - Managing Studio configurations
    - Bridging visual and code development
    """
    
    def __init__(self, project_root: str = None):
        """
        Initialize Studio integration.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.studio_config_path = self.project_root / "studio_config.json"
        self.studio_available = self._check_studio_availability()
        
    def _check_studio_availability(self) -> bool:
        """
        Check if LangGraph Studio is available and properly configured.
        
        Returns:
            bool: True if Studio is available, False otherwise
        """
        try:
            # Check if langgraph-studio is installed
            result = subprocess.run(
                ["uv", "run", "python", "-c", "import langgraph_studio; print('Studio available')"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_studio_status(self) -> Dict[str, Any]:
        """
        Get the current status of Studio integration.
        
        Returns:
            dict: Status information including availability, configuration, etc.
        """
        status = {
            "studio_available": self.studio_available,
            "config_exists": self.studio_config_path.exists(),
            "project_root": str(self.project_root),
            "config_path": str(self.studio_config_path)
        }
        
        if self.studio_config_path.exists():
            try:
                with open(self.studio_config_path, 'r') as f:
                    config = json.load(f)
                status["config_valid"] = True
                status["graphs_configured"] = len(config.get("graphs", {}))
            except Exception as e:
                status["config_valid"] = False
                status["config_error"] = str(e)
        
        return status
    
    def start_studio_server(self, port: int = 8000) -> bool:
        """
        Start the LangGraph Studio server.
        
        Args:
            port: Port number for the Studio server
            
        Returns:
            bool: True if server started successfully, False otherwise
        """
        if not self.studio_available:
            print("❌ LangGraph Studio is not available. Please install it first.")
            return False
        
        try:
            print(f"🚀 Starting LangGraph Studio server on port {port}...")
            print(f"📁 Project root: {self.project_root}")
            print(f"🔧 Config file: {self.studio_config_path}")
            
            # Start Studio server
            cmd = [
                "uv", "run", "langgraph-studio", 
                "--port", str(port),
                "--project-root", str(self.project_root)
            ]
            
            print(f"💻 Command: {' '.join(cmd)}")
            print("🌐 Studio will be available at: http://localhost:8000")
            print("📝 Press Ctrl+C to stop the server")
            
            # Note: In a real implementation, this would start the server
            # For demo purposes, we'll just show what would happen
            print("✅ Studio server would start here (demo mode)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Studio server: {e}")
            return False
    
    def import_graph_to_studio(self, graph_name: str, graph_module: str) -> bool:
        """
        Import a graph from code into Studio for visualization.
        
        Args:
            graph_name: Name of the graph to import
            graph_module: Python module containing the graph
            
        Returns:
            bool: True if import successful, False otherwise
        """
        try:
            print(f"📥 Importing graph '{graph_name}' from {graph_module}...")
            
            # Load the graph configuration
            if not self.studio_config_path.exists():
                print("❌ Studio config file not found")
                return False
            
            with open(self.studio_config_path, 'r') as f:
                config = json.load(f)
            
            if graph_name not in config.get("graphs", {}):
                print(f"❌ Graph '{graph_name}' not found in config")
                return False
            
            graph_config = config["graphs"][graph_name]
            
            print(f"✅ Graph '{graph_name}' configuration loaded:")
            print(f"   📋 Description: {graph_config.get('description', 'N/A')}")
            print(f"   🔗 Entry point: {graph_config.get('entry_point', 'N/A')}")
            print(f"   🎯 Finish points: {graph_config.get('finish_points', [])}")
            print(f"   🔧 Nodes: {graph_config.get('nodes', [])}")
            
            # In a real implementation, this would import the graph into Studio
            print("✅ Graph would be imported into Studio for visualization (demo mode)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to import graph: {e}")
            return False
    
    def export_graph_from_studio(self, graph_name: str, output_path: str) -> bool:
        """
        Export a graph from Studio back to code.
        
        Args:
            graph_name: Name of the graph to export
            output_path: Path where to save the exported code
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            print(f"📤 Exporting graph '{graph_name}' from Studio to {output_path}...")
            
            # In a real implementation, this would export the graph from Studio
            # For demo purposes, we'll create a sample export
            
            export_content = f'''"""
Exported graph from LangGraph Studio: {graph_name}
Generated on: {__import__('datetime').datetime.now().isoformat()}
"""

from typing import TypedDict
from langgraph.graph import StateGraph


class GraphState(TypedDict):
    """State schema for {graph_name}"""
    message: str
    response: str


def process_message(state: GraphState) -> GraphState:
    """Process message node - exported from Studio"""
    message = state.get("message", "")
    response = f"Processed in Studio: {{message}}"
    return {{"message": message, "response": response}}


def create_{graph_name}():
    """Create the {graph_name} graph - exported from Studio"""
    graph = StateGraph(GraphState)
    graph.add_node("process_message", process_message)
    graph.set_entry_point("process_message")
    graph.set_finish_point("process_message")
    return graph.compile()


if __name__ == "__main__":
    app = create_{graph_name}()
    result = app.invoke({{"message": "Hello from Studio!", "response": ""}})
    print(result)
'''
            
            # Write the exported code
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(export_content)
            
            print(f"✅ Graph exported successfully to: {output_path}")
            print(f"📄 File size: {output_file.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export graph: {e}")
            return False
    
    def list_available_graphs(self) -> List[str]:
        """
        List all graphs available for Studio integration.
        
        Returns:
            list: List of graph names
        """
        try:
            if not self.studio_config_path.exists():
                return []
            
            with open(self.studio_config_path, 'r') as f:
                config = json.load(f)
            
            return list(config.get("graphs", {}).keys())
            
        except Exception:
            return []
    
    def create_studio_demo(self) -> bool:
        """
        Create a comprehensive demo of Studio integration.
        
        Returns:
            bool: True if demo created successfully, False otherwise
        """
        try:
            print("🎬 Creating LangGraph Studio Integration Demo...")
            print("=" * 60)
            
            # 1. Show Studio status
            print("\n1️⃣ Studio Status Check:")
            status = self.get_studio_status()
            for key, value in status.items():
                print(f"   {key}: {value}")
            
            # 2. List available graphs
            print("\n2️⃣ Available Graphs:")
            graphs = self.list_available_graphs()
            if graphs:
                for graph in graphs:
                    print(f"   📊 {graph}")
            else:
                print("   ❌ No graphs configured")
            
            # 3. Demo graph import
            if graphs:
                print(f"\n3️⃣ Importing Graph to Studio:")
                self.import_graph_to_studio(graphs[0], "simple_graph")
            
            # 4. Demo graph export
            print(f"\n4️⃣ Exporting Graph from Studio:")
            export_path = self.project_root / "demo_exported_graph.py"
            self.export_graph_from_studio("simple_graph", str(export_path))
            
            # 5. Show Studio server startup
            print(f"\n5️⃣ Starting Studio Server:")
            self.start_studio_server()
            
            print("\n" + "=" * 60)
            print("🎉 Studio Integration Demo Complete!")
            print("💡 In a real implementation, Studio would provide:")
            print("   🎨 Visual graph editor")
            print("   🔍 Real-time debugging")
            print("   📊 Execution monitoring")
            print("   🔄 Live state inspection")
            print("   📈 Performance analytics")
            
            return True
            
        except Exception as e:
            print(f"❌ Demo creation failed: {e}")
            return False


def main():
    """Main function to run Studio integration demo."""
    print("🚀 LangGraph Studio Integration Demo")
    print("=" * 50)
    
    # Initialize Studio integration
    studio = StudioIntegration()
    
    # Run the demo
    success = studio.create_studio_demo()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("🔗 Next steps:")
        print("   1. Install langgraph-studio: uv add langgraph-studio")
        print("   2. Start Studio server: uv run langgraph-studio")
        print("   3. Open browser to: http://localhost:8000")
        print("   4. Import your graphs and start visual development!")
    else:
        print("\n❌ Demo failed. Please check the configuration.")


if __name__ == "__main__":
    main()
