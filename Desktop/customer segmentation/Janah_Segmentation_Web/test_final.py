#!/usr/bin/env python3
"""
Final Test Script for Janah Customer Segmentation
Comprehensive testing before presentation
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime

def test_environment():
    """Test Python environment and dependencies"""
    print("🔍 Testing Python Environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Compatible")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Requires Python 3.8+")
        return False
    
    # Check required packages
    required_packages = [
        'flask', 'pandas', 'numpy', 'sklearn', 'matplotlib', 
        'seaborn', 'streamlit', 'requests', 'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        'run.py',
        'requirements.txt',
        'README.md',
        'app/__init__.py',
        'app/routes.py',
        'app/templates/base.html',
        'app/templates/home.html',
        'app/templates/segmentation.html',
        'app/templates/results.html',
        'app/static/css/style.css',
        'app/static/js/script.js',
        'streamlit/segmentation.py',
        'streamlit/requirements.txt',
        'data/',
        'data/processed/',
        'data/uploads/'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False
    
    return True

def test_dataset():
    """Test if dataset is available"""
    print("\n📊 Testing Dataset...")
    
    dataset_path = 'data/online_retail.csv'
    if os.path.exists(dataset_path):
        file_size = os.path.getsize(dataset_path)
        if file_size > 1000000:  # > 1MB
            print(f"✅ Dataset found ({file_size:,} bytes)")
            return True
        else:
            print(f"⚠️  Dataset too small ({file_size:,} bytes)")
            return False
    else:
        print("❌ Dataset not found")
        print("💡 Run: python download_dataset.py")
        return False

def test_flask_app():
    """Test Flask application startup"""
    print("\n🚀 Testing Flask Application...")
    
    try:
        # Test import
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test routes
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home route working")
            else:
                print(f"❌ Home route failed: {response.status_code}")
                return False
            
            # Test segmentation route
            response = client.get('/segmentation')
            if response.status_code == 200:
                print("✅ Segmentation route working")
            else:
                print(f"❌ Segmentation route failed: {response.status_code}")
                return False
            
            # Test results route
            response = client.get('/results')
            if response.status_code == 200:
                print("✅ Results route working")
            else:
                print(f"❌ Results route failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {str(e)}")
        return False

def test_streamlit_module():
    """Test Streamlit segmentation module"""
    print("\n📈 Testing Streamlit Module...")
    
    try:
        # Test import
        sys.path.append('streamlit')
        from segmentation import load_and_clean_data, calculate_rfm, perform_clustering
        
        print("✅ Streamlit functions imported successfully")
        
        # Test with sample data
        import pandas as pd
        
        # Create sample data
        sample_data = pd.DataFrame({
            'CustomerID': [1, 2, 3],
            'InvoiceDate': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'InvoiceNo': ['INV001', 'INV002', 'INV003'],
            'Quantity': [5, 3, 2],
            'UnitPrice': [10.0, 15.0, 20.0]
        })
        
        # Test RFM calculation
        rfm_data = calculate_rfm(sample_data)
        if len(rfm_data) > 0:
            print("✅ RFM calculation working")
        else:
            print("❌ RFM calculation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit module test failed: {str(e)}")
        return False

def test_deployment_files():
    """Test deployment configuration files"""
    print("\n🚀 Testing Deployment Files...")
    
    deployment_files = [
        'Procfile',
        'runtime.txt',
        'app.json'
    ]
    
    missing_files = []
    for file_path in deployment_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing deployment files: {missing_files}")
        return False
    
    return True

def test_local_server():
    """Test if application can start locally"""
    print("\n🌐 Testing Local Server...")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'run.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        import time
        time.sleep(3)
        
        # Test if server is responding
        try:
            response = requests.get('http://localhost:5000', timeout=5)
            if response.status_code == 200:
                print("✅ Local server responding")
                process.terminate()
                return True
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.RequestException:
            print("❌ Server not responding")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Local server test failed: {str(e)}")
        return False

def generate_test_report(results):
    """Generate test report"""
    print("\n📋 Generating Test Report...")
    
    report = f"""
JANAH SEGMENTATION - FINAL TEST REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TEST RESULTS:
============
"""
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        report += f"{test_name}: {status}\n"
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    report += f"""
SUMMARY:
========
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {failed_tests}
Success Rate: {(passed_tests/total_tests)*100:.1f}%

RECOMMENDATIONS:
===============
"""
    
    if failed_tests == 0:
        report += "🎉 All tests passed! Ready for presentation.\n"
    else:
        report += "⚠️  Some tests failed. Please fix issues before presentation.\n"
    
    # Save report
    with open('test_report.txt', 'w') as f:
        f.write(report)
    
    print("✅ Test report saved to test_report.txt")

def main():
    """Main test function"""
    print("🧪 Janah Customer Segmentation - Final Testing")
    print("=" * 60)
    
    results = {}
    
    # Run all tests
    results['Environment'] = test_environment()
    results['File Structure'] = test_file_structure()
    results['Dataset'] = test_dataset()
    results['Flask App'] = test_flask_app()
    results['Streamlit Module'] = test_streamlit_module()
    results['Deployment Files'] = test_deployment_files()
    results['Local Server'] = test_local_server()
    
    # Generate report
    generate_test_report(results)
    
    # Summary
    print("\n" + "=" * 60)
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ready for presentation!")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed")
        print("❌ Please fix issues before presentation")
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
    
    print("\n🚀 Next Steps:")
    if passed_tests == total_tests:
        print("1. ✅ Run presentation preparation: python presentation_prep.py")
        print("2. ✅ Practice demo flow")
        print("3. ✅ Deploy to preferred platform")
        print("4. ✅ Present with confidence!")
    else:
        print("1. ❌ Fix failed tests")
        print("2. ❌ Re-run tests")
        print("3. ❌ Ensure everything works before presentation")

if __name__ == "__main__":
    main() 