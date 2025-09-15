#!/usr/bin/env python3
"""
Ocean Hazard Platform Setup Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run shell command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return None

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}")
    
    # Check Node.js
    node_check = run_command("node --version")
    if not node_check:
        print("❌ Node.js not found. Please install Node.js 18+")
        return False
    print(f"✅ Node.js {node_check.strip()}")
    
    # Check Yarn
    yarn_check = run_command("yarn --version")
    if not yarn_check:
        print("❌ Yarn not found. Installing yarn...")
        npm_install = run_command("npm install -g yarn")
        if not npm_install:
            print("❌ Failed to install Yarn")
            return False
    print(f"✅ Yarn {yarn_check.strip() if yarn_check else 'installed'}")
    
    return True

def setup_backend():
    """Set up backend environment"""
    print("\n🐍 Setting up backend...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print(f"❌ Backend directory '{backend_dir}' not found")
        return False
    
    # Create virtual environment
    venv_command = "python -m venv venv"
    if platform.system() == "Windows":
        activate_command = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
    else:
        activate_command = "source venv/bin/activate"
        pip_command = "venv/bin/pip"
    
    print("Creating virtual environment...")
    if not run_command(venv_command, cwd=backend_dir):
        return False
    
    # Install requirements
    print("Installing Python dependencies...")
    install_command = f"{pip_command} install -r requirements.txt"
    if not run_command(install_command, cwd=backend_dir):
        return False
    
    # Install emergentintegrations
    print("Installing Emergent integrations...")
    emergent_command = f"{pip_command} install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/"
    run_command(emergent_command, cwd=backend_dir)
    
    # Setup environment file
    env_file = os.path.join(backend_dir, ".env")
    env_example = os.path.join(backend_dir, ".env.example")
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print("Creating .env file from example...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ Created .env file")
    
    return True

def setup_frontend():
    """Set up frontend environment"""
    print("\n⚛️ Setting up frontend...")
    
    frontend_dir = "frontend"
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory '{frontend_dir}' not found")
        return False
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    if not run_command("yarn install", cwd=frontend_dir):
        return False
    
    # Setup environment file
    env_file = os.path.join(frontend_dir, ".env")
    env_example = os.path.join(frontend_dir, ".env.example")
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print("Creating .env file from example...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ Created .env file")
    
    return True

def print_startup_instructions():
    """Print instructions for starting the application"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 To start the application:")
    print("\n1. Start the backend:")
    if platform.system() == "Windows":
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload")
    else:
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload")
    
    print("\n2. Start the frontend (in a new terminal):")
    print("   cd frontend")
    print("   yarn start")
    
    print("\n3. Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8001")
    print("   API Docs: http://localhost:8001/docs")
    
    print("\n🔧 Optional: Start MongoDB locally")
    print("   mongod --dbpath /path/to/your/db")
    print("\n🌊 Enjoy building the Ocean Hazard Platform!")

def main():
    """Main setup function"""
    print("🌊 Ocean Hazard Platform Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install missing requirements.")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed.")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
    
    # Print startup instructions
    print_startup_instructions()

if __name__ == "__main__":
    main()
