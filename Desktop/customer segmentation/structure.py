#!/usr/bin/env python3
"""
Setup script to create the Janah Customer Segmentation Web project structure
"""

import os

def create_directory(path):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Created directory: {path}")

def create_file(path):
    """Create an empty file if it doesn't exist"""
    if not os.path.exists(path):
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Create empty file
        with open(path, 'w') as f:
            pass
        print(f"✅ Created file: {path}")

def setup_project():
    """Create the complete project structure"""
    
    # Base project directory
    base_dir = "Janah_Segmentation_Web"
    create_directory(base_dir)
    
    # Create directories
    directories = [
        f"{base_dir}/app",
        f"{base_dir}/app/templates",
        f"{base_dir}/app/static",
        f"{base_dir}/app/static/css",
        f"{base_dir}/app/static/js",
        f"{base_dir}/app/static/images",
        f"{base_dir}/streamlit",
        f"{base_dir}/data",
        f"{base_dir}/data/uploads",
        f"{base_dir}/venv"
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Create files
    files = [
        f"{base_dir}/app/__init__.py",
        f"{base_dir}/app/routes.py",
        f"{base_dir}/app/templates/base.html",
        f"{base_dir}/app/templates/home.html",
        f"{base_dir}/app/templates/segmentation.html",
        f"{base_dir}/app/templates/results.html",
        f"{base_dir}/app/static/css/style.css",
        f"{base_dir}/app/static/js/script.js",
        f"{base_dir}/streamlit/segmentation.py",
        f"{base_dir}/streamlit/requirements.txt",
        f"{base_dir}/data/online_retail.csv",
        f"{base_dir}/.gitignore",
        f"{base_dir}/README.md",
        f"{base_dir}/run.py"
    ]
    
    for file_path in files:
        create_file(file_path)
    
    print("\n" + "="*50)
    print("✅ Project structure created successfully!")
    print("="*50)
    print(f"📁 Base directory: {base_dir}")
    print("\n📋 Project structure:")
    print("Janah_Segmentation_Web/")
    print("├── app/")
    print("│   ├── __init__.py")
    print("│   ├── routes.py")
    print("│   ├── templates/")
    print("│   │   ├── base.html")
    print("│   │   ├── home.html")
    print("│   │   ├── segmentation.html")
    print("│   │   └── results.html")
    print("│   ├── static/")
    print("│   │   ├── css/style.css")
    print("│   │   ├── js/script.js")
    print("│   │   └── images/")
    print("├── streamlit/")
    print("│   ├── segmentation.py")
    print("│   └── requirements.txt")
    print("├── data/")
    print("│   ├── online_retail.csv")
    print("│   └── uploads/")
    print("├── venv/")
    print("├── .gitignore")
    print("├── README.md")
    print("└── run.py")

if __name__ == "__main__":
    setup_project()
