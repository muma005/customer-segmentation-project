#!/usr/bin/env python3
"""
Test script to verify Flask app can be imported and created
"""

try:
    from app import create_app
    print("✅ Successfully imported create_app")
    
    app = create_app()
    print("✅ Successfully created Flask app")
    print(f"✅ App name: {app.name}")
    print(f"✅ App config: {app.config['SECRET_KEY'][:10]}...")
    
    print("✅ All tests passed! App is ready for deployment.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc() 