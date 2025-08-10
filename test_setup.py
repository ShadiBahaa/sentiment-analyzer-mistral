#!/usr/bin/env python3
"""
Test script to verify the sentiment analyzer setup
"""

import requests
import subprocess
import sys
import time
import os
import platform

def test_python_imports():
    """Test if all required Python packages can be imported."""
    print("🔍 Testing Python package imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__}")
    except ImportError:
        print("❌ Requests not installed")
        return False
    
    return True

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    print("\n🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running")
            
            # Check for Mistral model
            mistral_found = False
            for model in models.get("models", []):
                if "mistral" in model.get("name", "").lower():
                    print(f"✅ Mistral model found: {model['name']}")
                    mistral_found = True
                    break
            
            if not mistral_found:
                print("⚠️  Mistral model not found. Run: ollama pull mistral")
                return False
            
            return True
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        "backend/main.py",
        "frontend/app.py",
        "requirements.txt",
        "README.md"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_files_exist = False
    
    return all_files_exist

def test_fastapi_startup():
    """Test if FastAPI can start without errors."""
    print("\n🔍 Testing FastAPI startup...")
    
    try:
        # Try to import and create the FastAPI app
        sys.path.append("backend")
        from main import app
        print("✅ FastAPI app imports successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI import failed: {e}")
        return False

def test_streamlit_startup():
    """Test if Streamlit app can be loaded without errors."""
    print("\n🔍 Testing Streamlit app...")
    
    try:
        # Basic syntax check
        with open("frontend/app.py", "r") as f:
            code = f.read()
            compile(code, "frontend/app.py", "exec")
        print("✅ Streamlit app syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Streamlit app syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking Streamlit app: {e}")
        return False

def run_integration_test():
    """Test the actual API endpoint if FastAPI is running."""
    print("\n🔍 Testing API integration...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            
            # Test analyze endpoint
            test_data = {"text": "This is a test message"}
            response = requests.post("http://localhost:8000/analyze/", 
                                   data=test_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis endpoint working. Result: {result.get('sentiment', 'Unknown')}")
                return True
            else:
                print(f"⚠️  Analysis endpoint returned status {response.status_code}")
                return False
        else:
            print("⚠️  FastAPI server not running on port 8000")
            return False
    
    except requests.exceptions.ConnectionError:
        print("⚠️  FastAPI server not running. Start with: uvicorn backend.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Sentiment Analyzer Setup Test\n")
    
    tests = [
        ("Python Imports", test_python_imports),
        ("File Structure", test_file_structure),
        ("FastAPI Startup", test_fastapi_startup),
        ("Streamlit App", test_streamlit_startup),
        ("Ollama Connection", test_ollama_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Optional integration test
    print("\n" + "="*50)
    print("🚀 Optional Integration Test")
    print("(Only runs if FastAPI server is already running)")
    run_integration_test()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start backend: uvicorn backend.main:app --reload")
        print("2. Start frontend: streamlit run frontend/app.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)