#!/usr/bin/env python3
"""
Setup script for Sentiment Analyzer project
Automates the project setup process
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor} detected")

def check_ollama():
    """Check if Ollama is installed and running."""
    print("🔄 Checking Ollama installation...")
    result = run_command("ollama --version", "Checking Ollama version")
    if not result:
        print("❌ Ollama is not installed. Please install it from https://ollama.ai/")
        return False
    
    print("🔄 Checking if Ollama is running...")
    result = run_command("ollama list", "Checking Ollama service")
    if not result:
        print("⚠️  Ollama service might not be running. Try: ollama serve")
        return False
    
    return True

def setup_project():
    """Set up the complete project structure."""
    print("🚀 Setting up Sentiment Analyzer project...")
    
    # Check Python version
    check_python_version()
    
    # Create project directory structure
    print("📁 Creating project structure...")
    os.makedirs("sentiment-analyzer-mistral/backend", exist_ok=True)
    os.makedirs("sentiment-analyzer-mistral/frontend", exist_ok=True)
    
    # Change to project directory
    os.chdir("sentiment-analyzer-mistral")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Determine activation command based on OS
    if sys.platform.startswith('win'):
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install fastapi uvicorn streamlit requests python-multipart", 
                      "Installing Python packages"):
        return False
    
    # Check Ollama
    if check_ollama():
        # Pull Mistral model
        run_command("ollama pull mistral", "Pulling Mistral model")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Navigate to the project directory:")
    print("   cd sentiment-analyzer-mistral")
    print("\n2. Activate the virtual environment:")
    if sys.platform.startswith('win'):
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("\n3. Start the backend (in one terminal):")
    print("   uvicorn backend.main:app --reload")
    print("\n4. Start the frontend (in another terminal):")
    print("   streamlit run frontend/app.py")
    print("\n5. Open your browser to http://localhost:8501")
    
    return True

if __name__ == "__main__":
    setup_project()