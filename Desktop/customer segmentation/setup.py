#!/usr/bin/env python3
"""
Setup script to create the Janah Customer Segmentation Web project structure
"""

import os
import shutil

# Define the main project structure
project_folders = [
    "app", "streamlit", "data", "models", "utils", "config", "tests"
]

# Define subfolders for each main folder
subfolder_structure = {
    "app": ["templates", "static", "static/css", "static/js", "static/images"],
    "data": ["uploads", "processed", "raw"],
    "models": ["clustering", "preprocessing"],
    "utils": ["data_processing", "visualization"],
    "config": [],
    "tests": ["unit", "integration"],
    "streamlit": ["pages", "components"]
}

# Define files to create with their content
project_files = {
    # App files
    "app/__init__.py": """from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
""",
    
    "app/routes.py": """from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/segmentation')
def segmentation():
    return render_template('segmentation.html')

@main.route('/results')
def results():
    return render_template('results.html')
""",

    # Template files
    "app/templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Janah Customer Segmentation{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.home') }}">Janah Segmentation</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('main.home') }}">Home</a>
                <a class="nav-link" href="{{ url_for('main.segmentation') }}">Segmentation</a>
                <a class="nav-link" href="{{ url_for('main.results') }}">Results</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",

    "app/templates/home.html": """{% extends "base.html" %}

{% block title %}Home - Janah Customer Segmentation{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1>Welcome to Janah Customer Segmentation</h1>
        <p class="lead">Analyze and segment your customers with advanced machine learning techniques.</p>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Upload Data</h5>
                        <p class="card-text">Upload your customer data for analysis.</p>
                        <a href="{{ url_for('main.segmentation') }}" class="btn btn-primary">Get Started</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">View Results</h5>
                        <p class="card-text">View your segmentation results and insights.</p>
                        <a href="{{ url_for('main.results') }}" class="btn btn-outline-primary">View Results</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    # Static files
    "app/static/css/style.css": """/* Custom styles for Janah Segmentation */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: 1px solid rgba(0, 0, 0, 0.125);
    margin-bottom: 1rem;
}

.card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}
""",

    "app/static/js/script.js": """// JavaScript for Janah Customer Segmentation
document.addEventListener('DOMContentLoaded', function() {
    console.log('Janah Segmentation App Loaded');
});
""",

    # Streamlit files
    "streamlit/main.py": """import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Janah Customer Segmentation",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Janah Customer Segmentation Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="Upload your customer data in CSV format"
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        st.subheader("Data Preview")
        st.dataframe(df.head())
    else:
        st.info("Please upload a CSV file to begin segmentation analysis")

if __name__ == "__main__":
    main()
""",

    # Utils files
    "utils/data_processing/__init__.py": "",
    "utils/data_processing/cleaner.py": """import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self):
        pass
    
    def clean_data(self, df):
        \"\"\"Clean and preprocess customer data\"\"\"
        # Remove duplicates
        df_clean = df.drop_duplicates()
        
        # Handle missing values
        df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        
        return df_clean
""",

    "utils/visualization/__init__.py": "",
    "utils/visualization/plots.py": """import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class SegmentationPlotter:
    def __init__(self):
        pass
    
    def plot_clusters(self, df, x_col, y_col, cluster_col):
        \"\"\"Create cluster visualization\"\"\"
        fig = px.scatter(df, x=x_col, y=y_col, color=cluster_col)
        return fig
""",

    # Models files
    "models/__init__.py": "",
    "models/clustering/__init__.py": "",
    "models/clustering/kmeans.py": """from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

class CustomerSegmentation:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
    
    def fit_predict(self, data):
        \"\"\"Fit the model and predict clusters\"\"\"
        scaled_data = self.scaler.fit_transform(data)
        clusters = self.kmeans.fit_predict(scaled_data)
        return clusters
""",

    # Config files
    "config/__init__.py": "",
    "config/settings.py": """# Configuration settings for Janah Customer Segmentation

# Flask settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Data settings
UPLOAD_FOLDER = 'data/uploads'
PROCESSED_FOLDER = 'data/processed'

# Model settings
DEFAULT_CLUSTERS = 4
RANDOM_STATE = 42
""",

    # Main run file
    "run.py": """#!/usr/bin/env python3
\"\"\"
Main application runner for Janah Customer Segmentation Web App
\"\"\"

from app import create_app

def main():
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
""",

    # Requirements
    "requirements.txt": """Flask>=2.3.0
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
Werkzeug>=2.3.0
Jinja2>=3.1.0
""",

    # Keep files
    "data/uploads/.gitkeep": "",
    "data/processed/.gitkeep": "",
    "data/raw/.gitkeep": "",

    # Gitignore
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data files
*.csv
*.xlsx
*.json
data/uploads/*
!data/uploads/.gitkeep

# Logs
*.log

# Environment variables
.env

# Streamlit
.streamlit/
""",

    # README
    "README.md": """# Janah Customer Segmentation Web Application

A comprehensive web application for customer segmentation analysis using Flask and Streamlit.

## Features

- Web-based customer segmentation analysis
- Interactive Streamlit dashboard
- Data upload and processing capabilities
- Multiple segmentation algorithms
- Visualization and reporting

## Installation

1. Clone/create the project structure
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\\Scripts\\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install requirements: `pip install -r requirements.txt`

## Usage

### Flask Web Application
```bash
python run.py
```

### Streamlit Dashboard
```bash
streamlit run streamlit/main.py
```

## Project Structure

```
Janah_Segmentation_Web/
├── app/                    # Flask application
├── streamlit/              # Streamlit components  
├── models/                 # ML models
├── utils/                  # Utility functions
├── data/                   # Data files
├── config/                 # Configuration
├── tests/                  # Test files
└── requirements.txt
```
"""
}

def create_project_structure():
    """Create the Janah Customer Segmentation project structure"""
    
    # Step 1: Create main project directory
    project_name = "Janah_Segmentation_Web"
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"✅ Created '{project_name}/' project directory.")
    
    # Step 2: Create main folders
    for folder in project_folders:
        folder_path = os.path.join(project_name, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"✅ Created '{folder}/' directory")
        else:
            print(f"⚠️ Directory '{folder}/' already exists")
    
    # Step 3: Create subfolders
    for main_folder, subfolders in subfolder_structure.items():
        for subfolder in subfolders:
            subfolder_path = os.path.join(project_name, main_folder, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                print(f"✅ Created '{main_folder}/{subfolder}/' subdirectory")
    
    # Step 4: Create files with content
    for file_path, content in project_files.items():
        full_path = os.path.join(project_name, file_path)
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(full_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        # Create file
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created file '{file_path}'")
        else:
            print(f"⚠️ File '{file_path}' already exists")
    
    # Step 5: Ensure __init__.py exists in all Python packages
    for root, dirs, files in os.walk(project_name):
        # Skip certain directories
        skip_dirs = {'static', 'templates', 'uploads', 'processed', 'raw', '.git', '__pycache__'}
        if any(skip_dir in root for skip_dir in skip_dirs):
            continue
            
        # Add __init__.py to Python package directories
        if any(file.endswith('.py') for file in files) or 'models' in root or 'utils' in root:
            init_file = os.path.join(root, "__init__.py")
            if "__init__.py" not in files:
                with open(init_file, 'w') as f:
                    f.write("")
                print(f"📦 Added '__init__.py' to '{root}'")
    
    print("\\n" + "="*60)
    print("🎉 Janah Customer Segmentation project structure created!")
    print("="*60)
    print(f"📁 Project directory: {project_name}")
    print("\\n📋 Next steps:")
    print(f"1. cd {project_name}")
    print("2. python -m venv venv")
    print("3. venv\\Scripts\\activate  (Windows) or source venv/bin/activate  (Linux/Mac)")
    print("4. pip install -r requirements.txt")
    print("5. python run.py  (for Flask app)")
    print("6. streamlit run streamlit/main.py  (for Streamlit app)")
    print("\\n💡 You can now run: pip install -e . (if you want to install as a package)")

if __name__ == "__main__":
    create_project_structure()
