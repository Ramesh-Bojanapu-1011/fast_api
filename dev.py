#!/usr/bin/env python3
"""
Development helper script for running common tasks.
Usage: python dev.py [command]

Commands:
  test        - Run all tests
  test-basic  - Run basic API tests
  test-pytest - Run comprehensive pytest tests
  install     - Install all dependencies
  serve       - Start the development server
  help        - Show this help message
"""

import sys
import subprocess

def run_command(command, description):
    """Run a command and print the description"""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"✅ {description} completed successfully!")
    else:
        print(f"❌ {description} failed!")
    return result.returncode

def main():
    """Main function to handle commands"""
    if len(sys.argv) < 2:
        command = "help"
    else:
        command = sys.argv[1]
    
    # Get Python executable path
    python_exe = '"C:/lovely ram/Work/pappu\'s/fast_api/.venv/Scripts/python.exe"'
    
    if command == "test" or command == "test-all":
        print("🧪 Running all tests...")
        run_command(f"{python_exe} test_api.py", "Basic API tests")
        run_command(f"{python_exe} -m pytest test_main.py -v", "Comprehensive pytest tests")
    
    elif command == "test-basic":
        run_command(f"{python_exe} test_api.py", "Basic API tests")
    
    elif command == "test-pytest":
        run_command(f"{python_exe} -m pytest test_main.py -v", "Comprehensive pytest tests")
    
    elif command == "install":
        run_command(f"{python_exe} -m pip install -r requirements.txt", "Installing dependencies")
    
    elif command == "serve" or command == "start":
        print("🚀 Starting development server...")
        print("Server will be available at: http://127.0.0.1:8000")
        print("API Documentation: http://127.0.0.1:8000/docs")
        print("Press Ctrl+C to stop the server")
        subprocess.run(f"{python_exe} -m uvicorn main:app --reload", shell=True)
    
    elif command == "help" or command == "--help" or command == "-h":
        print(__doc__)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python dev.py help' for available commands")
        sys.exit(1)

if __name__ == "__main__":
    main()