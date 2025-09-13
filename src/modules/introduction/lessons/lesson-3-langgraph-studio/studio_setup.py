"""
LangGraph Studio Setup and Configuration

This module handles the setup and configuration of LangGraph Studio,
including environment setup, API key management, and project initialization.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any


class StudioSetup:
    """
    Handles setup and configuration of LangGraph Studio.
    
    Provides methods for:
    - Installing Studio dependencies
    - Configuring environment variables
    - Setting up API keys
    - Initializing Studio projects
    - Validating configurations
    """
    
    def __init__(self, project_root: str = None):
        """
        Initialize Studio setup.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.env_file = self.project_root / ".env"
        self.studio_config_path = self.project_root / "studio_config.json"
        
    def check_prerequisites(self) -> Dict[str, bool]:
        """
        Check if all prerequisites for Studio are met.
        
        Returns:
            dict: Status of each prerequisite
        """
        prerequisites = {
            "python_version": self._check_python_version(),
            "uv_available": self._check_uv_available(),
            "project_structure": self._check_project_structure(),
            "env_file_exists": self.env_file.exists(),
            "studio_config_exists": self.studio_config_path.exists()
        }
        
        return prerequisites
    
    def _check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        try:
            version = sys.version_info
            return version.major == 3 and version.minor >= 11
        except Exception:
            return False
    
    def _check_uv_available(self) -> bool:
        """Check if uv package manager is available."""
        try:
            result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def _check_project_structure(self) -> bool:
        """Check if project has the expected structure."""
        required_dirs = ["src", "tests"]
        required_files = ["pyproject.toml"]
        
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                return False
        
        for file_name in required_files:
            if not (self.project_root / file_name).exists():
                return False
        
        return True
    
    def install_studio_dependencies(self) -> bool:
        """
        Install LangGraph Studio and related dependencies.
        
        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            print("📦 Installing LangGraph Studio dependencies...")
            
            # Install langgraph-studio
            cmd = ["uv", "add", "langgraph-studio"]
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to install langgraph-studio: {result.stderr}")
                return False
            
            print("✅ LangGraph Studio installed successfully")
            
            # Install additional dependencies if needed
            additional_deps = ["fastapi", "uvicorn", "websockets"]
            for dep in additional_deps:
                cmd = ["uv", "add", dep]
                result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dep} installed")
                else:
                    print(f"⚠️  {dep} installation failed (may already be installed)")
            
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def setup_environment_variables(self) -> bool:
        """
        Set up environment variables for Studio.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            print("🔧 Setting up environment variables...")
            
            # Check if .env file exists
            if not self.env_file.exists():
                print("📝 Creating .env file...")
                self.env_file.touch()
            
            # Read existing .env content
            existing_content = ""
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    existing_content = f.read()
            
            # Required environment variables for Studio
            required_vars = {
                "GOOGLE_API_KEY": "Your Google Gemini API key",
                "LANGCHAIN_TRACING_V2": "true",
                "LANGCHAIN_ENDPOINT": "https://api.smith.langchain.com",
                "LANGCHAIN_API_KEY": "Your LangChain API key (optional)",
                "LANGGRAPH_STUDIO_PORT": "8000",
                "LANGGRAPH_STUDIO_HOST": "localhost"
            }
            
            # Check which variables are missing
            missing_vars = []
            for var_name in required_vars.keys():
                if f"{var_name}=" not in existing_content:
                    missing_vars.append(var_name)
            
            if missing_vars:
                print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
                print("📝 Please add these to your .env file:")
                print()
                
                for var_name in missing_vars:
                    description = required_vars[var_name]
                    print(f"# {description}")
                    print(f"{var_name}=your_value_here")
                    print()
                
                print("💡 You can copy from env.example and update with your actual values")
                return False
            else:
                print("✅ All required environment variables are configured")
                return True
                
        except Exception as e:
            print(f"❌ Environment setup failed: {e}")
            return False
    
    def create_studio_config(self) -> bool:
        """
        Create or update the Studio configuration file.
        
        Returns:
            bool: True if config created successfully, False otherwise
        """
        try:
            print("📋 Creating Studio configuration...")
            
            # Default Studio configuration
            config = {
                "version": "1.0.0",
                "project_name": "langgraph-intro",
                "description": "LangGraph Introduction Course - Studio Integration",
                "graphs": {
                    "simple_graph": {
                        "name": "simple_graph",
                        "description": "Simple message processing graph from lesson 2",
                        "state_schema": "GraphState",
                        "entry_point": "process_message",
                        "finish_points": ["process_message"],
                        "nodes": ["process_message"],
                        "conditional_edges": [],
                        "module_path": "src.modules.introduction.lessons.lesson_2_simple_graph.simple_graph"
                    }
                },
                "state_schemas": {
                    "GraphState": {
                        "fields": ["message", "response"],
                        "description": "Basic state schema for simple graphs"
                    }
                },
                "studio_settings": {
                    "port": 8000,
                    "host": "localhost",
                    "auto_reload": True,
                    "debug_mode": True,
                    "enable_monitoring": True
                },
                "deployment": {
                    "export_format": "python",
                    "include_tests": True,
                    "include_docs": True
                }
            }
            
            # Write configuration to file
            with open(self.studio_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Studio configuration created: {self.studio_config_path}")
            return True
            
        except Exception as e:
            print(f"❌ Configuration creation failed: {e}")
            return False
    
    def validate_setup(self) -> Dict[str, Any]:
        """
        Validate the complete Studio setup.
        
        Returns:
            dict: Validation results
        """
        validation_results = {
            "prerequisites": self.check_prerequisites(),
            "studio_import": self._test_studio_import(),
            "config_valid": self._validate_config(),
            "environment_ready": self._check_environment()
        }
        
        # Calculate overall status
        all_prereqs_met = all(validation_results["prerequisites"].values())
        studio_works = validation_results["studio_import"]
        config_ok = validation_results["config_valid"]
        env_ok = validation_results["environment_ready"]
        
        validation_results["overall_status"] = all_prereqs_met and studio_works and config_ok and env_ok
        
        return validation_results
    
    def _test_studio_import(self) -> bool:
        """Test if Studio can be imported."""
        try:
            result = subprocess.run(
                ["uv", "run", "python", "-c", "import langgraph_studio; print('Studio import successful')"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _validate_config(self) -> bool:
        """Validate the Studio configuration file."""
        try:
            if not self.studio_config_path.exists():
                return False
            
            with open(self.studio_config_path, 'r') as f:
                config = json.load(f)
            
            # Check required fields
            required_fields = ["version", "project_name", "graphs", "studio_settings"]
            for field in required_fields:
                if field not in config:
                    return False
            
            return True
        except Exception:
            return False
    
    def _check_environment(self) -> bool:
        """Check if environment is properly configured."""
        try:
            if not self.env_file.exists():
                return False
            
            with open(self.env_file, 'r') as f:
                content = f.read()
            
            # Check for required variables
            required_vars = ["GOOGLE_API_KEY", "LANGCHAIN_TRACING_V2"]
            for var in required_vars:
                if f"{var}=" not in content:
                    return False
            
            return True
        except Exception:
            return False
    
    def run_complete_setup(self) -> bool:
        """
        Run the complete Studio setup process.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        print("🚀 Starting LangGraph Studio Setup...")
        print("=" * 50)
        
        # Step 1: Check prerequisites
        print("\n1️⃣ Checking Prerequisites...")
        prereqs = self.check_prerequisites()
        for check, status in prereqs.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {check}: {status}")
        
        if not all(prereqs.values()):
            print("❌ Prerequisites not met. Please fix the issues above.")
            return False
        
        # Step 2: Install dependencies
        print("\n2️⃣ Installing Dependencies...")
        if not self.install_studio_dependencies():
            print("❌ Dependency installation failed.")
            return False
        
        # Step 3: Setup environment
        print("\n3️⃣ Setting up Environment...")
        if not self.setup_environment_variables():
            print("❌ Environment setup failed.")
            return False
        
        # Step 4: Create configuration
        print("\n4️⃣ Creating Configuration...")
        if not self.create_studio_config():
            print("❌ Configuration creation failed.")
            return False
        
        # Step 5: Validate setup
        print("\n5️⃣ Validating Setup...")
        validation = self.validate_setup()
        
        print("\n📊 Setup Validation Results:")
        for check, result in validation.items():
            if isinstance(result, dict):
                print(f"   {check}:")
                for sub_check, sub_result in result.items():
                    status_icon = "✅" if sub_result else "❌"
                    print(f"     {status_icon} {sub_check}: {sub_result}")
            else:
                status_icon = "✅" if result else "❌"
                print(f"   {status_icon} {check}: {result}")
        
        if validation["overall_status"]:
            print("\n🎉 Studio setup completed successfully!")
            print("\n🚀 Next steps:")
            print("   1. Start Studio: uv run langgraph-studio")
            print("   2. Open browser: http://localhost:8000")
            print("   3. Import your graphs and start visual development!")
            return True
        else:
            print("\n❌ Setup validation failed. Please check the issues above.")
            return False


def main():
    """Main function to run Studio setup."""
    print("🔧 LangGraph Studio Setup")
    print("=" * 30)
    
    # Initialize setup
    setup = StudioSetup()
    
    # Run complete setup
    success = setup.run_complete_setup()
    
    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")


if __name__ == "__main__":
    main()
