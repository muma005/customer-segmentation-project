# Janah Customer Segmentation Web Application

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
3. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
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
