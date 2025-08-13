#!/usr/bin/env python3
"""
InfluenceOS Backend Startup Script
Enhanced with Local LLM Models and OpenRouter API
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'torch',
        'transformers',
        'aiohttp'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ Dependencies installed successfully!")
    else:
        print("✅ All dependencies are installed!")

def check_gpu():
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🚀 GPU Available: {gpu_name} ({gpu_count} device(s))")
            return True
        else:
            print("💻 Using CPU (GPU not available)")
            return False
    except ImportError:
        print("⚠️ PyTorch not available")
        return False

def main():
    """Main startup function"""
    print("🤖 InfluenceOS Backend Starting...")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Check GPU
    has_gpu = check_gpu()
    
    # Set environment variables
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
    
    print("\n🔧 Configuration:")
    print(f"   • Local Models: Mistral 7B, Qwen")
    print(f"   • OpenRouter API: Configured")
    print(f"   • Device: {'GPU' if has_gpu else 'CPU'}")
    print(f"   • Port: 8000")
    
    print("\n🚀 Starting server...")
    print("   • Frontend: http://localhost:8080")
    print("   • Backend: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    
    # Start the server
    try:
        from simple_server import app
        import uvicorn
        
        uvicorn.run(
            "simple_server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
