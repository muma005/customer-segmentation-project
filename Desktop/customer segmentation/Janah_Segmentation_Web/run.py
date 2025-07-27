#!/usr/bin/env python3
"""
Main application runner for Janah Customer Segmentation Web App
"""

from app import create_app

# Create the Flask app instance for Railway
app = create_app()

def main():
    """Start the Flask application"""
    print("🚀 Starting Janah Customer Segmentation Web App...")
    print("📊 Visit: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

if __name__ == '__main__':
    main()
