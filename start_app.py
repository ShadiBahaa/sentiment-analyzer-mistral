#!/usr/bin/env python3
"""
Startup script for the Sentiment Analyzer application
Handles starting both backend and frontend services
"""

import subprocess
import sys
import time
import signal
import os
import platform
from pathlib import Path

class AppStarter:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print("\n🛑 Shutting down services...")
        self.running = False
        self.stop_services()
        sys.exit(0)

    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown."""
        if platform.system() != "Windows":
            # Unix-like systems
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
        else:
            # Windows
            signal.signal(signal.SIGINT, self.signal_handler)
            # SIGTERM is not available on Windows

    def check_requirements(self):
        """Check if all requirements are met."""
        print("🔍 Checking requirements...")
        
        # Check if we're in the right directory
        if not Path("backend/main.py").exists() or not Path("frontend/app.py").exists():
            print("❌ Please run this script from the project root directory")
            print("   Expected files: backend/main.py, frontend/app.py")
            return False
        
        # Check Python packages
        try:
            import fastapi, uvicorn, streamlit, requests
            print("✅ Python packages installed")
        except ImportError as e:
            print(f"❌ Missing Python package: {e}")
            print("   Run: pip install -r requirements.txt")
            return False
        
        # Check Ollama
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                print("✅ Ollama is running")
                
                # Check Mistral model
                models = response.json()
                mistral_found = any("mistral" in model["name"].lower() 
                                  for model in models.get("models", []))
                
                if mistral_found:
                    print("✅ Mistral model available")
                else:
                    print("⚠️  Mistral model not found")
                    print("   Run: ollama pull mistral")
                    response = input("   Continue anyway? (y/N): ")
                    if response.lower() != 'y':
                        return False
            else:
                print("❌ Ollama is not responding properly")
                return False
                
        except Exception:
            print("❌ Cannot connect to Ollama")
            print("   Make sure Ollama is running: ollama serve")
            response = input("   Continue anyway? (y/N): ")
            if response.lower() != 'y':
                return False
        
        return True

    def start_backend(self):
        """Start the FastAPI backend."""
        print("🚀 Starting FastAPI backend...")
        try:
            # Use Python executable from current environment
            python_exe = sys.executable
            
            # For Windows, we might need to handle the path differently
            if platform.system() == "Windows":
                # Use CREATE_NEW_PROCESS_GROUP for Windows
                creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                self.backend_process = subprocess.Popen([
                    python_exe, "-m", "uvicorn", 
                    "backend.main:app", 
                    "--reload",
                    "--host", "0.0.0.0",
                    "--port", "8000"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                creationflags=creation_flags)
            else:
                # Unix-like systems
                self.backend_process = subprocess.Popen([
                    python_exe, "-m", "uvicorn", 
                    "backend.main:app", 
                    "--reload",
                    "--host", "0.0.0.0",
                    "--port", "8000"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment and check if it started
            time.sleep(3)
            if self.backend_process.poll() is None:
                print("✅ Backend started on http://localhost:8000")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend failed to start")
                print(f"Error: {stderr.decode() if stderr else 'No error output'}")
                return False
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the Streamlit frontend."""
        print("🎨 Starting Streamlit frontend...")
        try:
            # Set environment variables for Streamlit
            env = os.environ.copy()
            env['STREAMLIT_SERVER_HEADLESS'] = 'true'
            env['STREAMLIT_SERVER_PORT'] = '8501'
            
            python_exe = sys.executable
            
            if platform.system() == "Windows":
                # Windows-specific handling
                creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
                self.frontend_process = subprocess.Popen([
                    python_exe, "-m", "streamlit", "run", 
                    "frontend/app.py",
                    "--server.port", "8501",
                    "--server.headless", "true"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                env=env, creationflags=creation_flags)
            else:
                # Unix-like systems
                self.frontend_process = subprocess.Popen([
                    python_exe, "-m", "streamlit", "run", 
                    "frontend/app.py",
                    "--server.port", "8501",
                    "--server.headless", "true"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            
            # Wait a moment and check if it started
            time.sleep(4)
            if self.frontend_process.poll() is None:
                print("✅ Frontend started on http://localhost:8501")
                return True
            else:
                stdout, stderr = self.frontend_process.communicate()
                print(f"❌ Frontend failed to start")
                print(f"Error: {stderr.decode() if stderr else 'No error output'}")
                return False
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False

    def wait_for_backend(self):
        """Wait for backend to be ready."""
        print("⏳ Waiting for backend to be ready...")
        import requests
        
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8000/", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is ready")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("❌ Backend is not responding after 30 seconds")
        return False

    def stop_services(self):
        """Stop both services."""
        if self.backend_process:
            print("🛑 Stopping backend...")
            try:
                if platform.system() == "Windows":
                    # On Windows, use CTRL_BREAK_EVENT for graceful shutdown
                    self.backend_process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    # On Unix-like systems, use SIGTERM
                    self.backend_process.terminate()
                
                try:
                    self.backend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("⚠️  Backend didn't stop gracefully, forcing...")
                    self.backend_process.kill()
                    self.backend_process.wait()
            except Exception as e:
                print(f"⚠️  Error stopping backend: {e}")
                try:
                    self.backend_process.kill()
                except:
                    pass
        
        if self.frontend_process:
            print("🛑 Stopping frontend...")
            try:
                if platform.system() == "Windows":
                    # On Windows, use CTRL_BREAK_EVENT for graceful shutdown
                    self.frontend_process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    # On Unix-like systems, use SIGTERM
                    self.frontend_process.terminate()
                
                try:
                    self.frontend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("⚠️  Frontend didn't stop gracefully, forcing...")
                    self.frontend_process.kill()
                    self.frontend_process.wait()
            except Exception as e:
                print(f"⚠️  Error stopping frontend: {e}")
                try:
                    self.frontend_process.kill()
                except:
                    pass

    def run(self):
        """Main run method."""
        print("🎭 Sentiment Analyzer Startup Script")
        print("=" * 40)
        
        # Set up signal handlers
        self.setup_signal_handlers()
        
        # Check requirements
        if not self.check_requirements():
            print("❌ Requirements check failed. Exiting.")
            return False
        
        print("\n🚀 Starting services...")
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend. Exiting.")
            return False
        
        # Wait for backend to be ready
        if not self.wait_for_backend():
            print("❌ Backend is not ready. Exiting.")
            self.stop_services()
            return False
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend. Stopping backend.")
            self.stop_services()
            return False
        
        print("\n🎉 Application is running!")
        print("=" * 40)
        print("🌐 Frontend: http://localhost:8501")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("=" * 40)
        print("Press Ctrl+C to stop both services")
        
        # Keep running until interrupted
        try:
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died unexpectedly")
                    break
                    
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend process died unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            pass
        
        self.stop_services()
        print("🛑 Services stopped")
        return True

def main():
    """Main entry point."""
    app = AppStarter()
    success = app.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()