#!/usr/bin/env python
"""
Production runner for the MNIST Web Application
This script is used to run the application in production environments
like Render and Heroku.
"""

import sys
import os
from pathlib import Path

# 添加详细日志输出
print("Starting run_production.py...")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))
print(f"Added project root to path: {str(project_root)}")

# Set environment variable to preload data
os.environ['MNIST_PRELOAD_DATA'] = '1'

# Get PORT environment variable with improved error handling
try:
    port_env = os.environ.get('PORT')
    if port_env:
        try:
            port = int(port_env)
            print(f"Using PORT from environment variable: {port}")
        except ValueError:
            print(f"Warning: Invalid PORT value '{port_env}', using default 5000")
            port = 5000
    else:
        port = 5000
        print(f"No PORT environment variable found, using default: {port}")
except Exception as e:
    print(f"Error getting PORT environment variable: {e}")
    port = 5000

print(f"Final PORT value: {port}")
print(f"All environment variables: {dict(os.environ)}")

# 尝试导入常用库，检查依赖安装情况
try:
    print("Attempting to import essential libraries...")
    
    # 首先尝试导入基础库
    print("Importing numpy...")
    import numpy as np
    print(f"NumPy imported successfully: version {np.__version__}")
    
    print("Importing Flask...")
    from flask import Flask
    
    # 其他科学计算库
    print("Importing other scientific libraries...")
    import scipy
    print(f"SciPy imported successfully: version {scipy.__version__}")
    
    import sklearn
    print(f"Scikit-learn imported successfully: version {sklearn.__version__}")
    
    from PIL import Image
    print("PIL/Pillow imported successfully")
    
    print("All essential libraries imported successfully!")
except ImportError as e:
    print(f"ERROR: Failed to import a required library: {e}")
    print("Please ensure all dependencies are installed.")
    sys.exit(1)

# Apply MarkupSafe fix
try:
    from fix_markupsafe import soft_unicode
    print("MarkupSafe fix applied successfully")
except Exception as e:
    print(f"Warning: Failed to apply MarkupSafe fix: {e}")

# Import the Flask app
try:
    print("Importing Flask app...")
    from mnist_web.app import app
    print("Flask app imported successfully")
except Exception as e:
    print(f"ERROR: Failed to import Flask app: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

if __name__ == '__main__':
    print(f"Starting app on host='0.0.0.0', port={port}")
    print("This script will bind to the PORT environment variable provided by Render")
    
    try:
        # Run the application
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"ERROR: Failed to start the application: {e}")
        # 尝试检查端口是否已经被占用
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('0.0.0.0', port))
            print(f"Port {port} is available")
        except socket.error as e:
            print(f"Port {port} is already in use or not available: {e}")
        finally:
            s.close()
        sys.exit(1) 