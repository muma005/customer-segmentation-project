#!/usr/bin/env python3
"""
Script to check and install required dependencies for Janah Segmentation
"""

import subprocess
import sys
import importlib

def check_package(package_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔍 Checking dependencies for Janah Customer Segmentation...")
    print("=" * 60)
    
    # Core dependencies
    dependencies = [
        "flask",
        "werkzeug", 
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "streamlit",
        "requests",
        "openpyxl",
        "xlrd"
    ]
    
    missing_packages = []
    
    for package in dependencies:
        if check_package(package):
            print(f"✅ {package} - Installed")
        else:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        print("=" * 60)
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
        
        print("\n🔄 Re-checking dependencies...")
        print("=" * 60)
        
        for package in dependencies:
            if check_package(package):
                print(f"✅ {package} - Available")
            else:
                print(f"❌ {package} - Still missing")
    else:
        print("\n🎉 All dependencies are installed!")
    
    print("\n📋 Next steps:")
    print("1. Run: python download_dataset.py")
    print("2. Run: python run.py")
    print("3. Visit: http://localhost:5000")

if __name__ == "__main__":
    main() 